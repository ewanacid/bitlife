import os, random, json, traceback
os.environ["KIVY_NO_ARGS"] = "1" # Force stability

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView

# --- CORE ENGINE ---
class LifeEngine:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.age = 0
        self.money = 0
        self.health = 100
        self.happiness = 100
        self.alive = True
        self.job = "Unemployed"
        self.salary = 0
        self.assets = []
        self.relationships = [] # {name, type, stats}
        self.log_history = ["Born into the Titan System."]

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")

    def age_up(self):
        if not self.alive: return
        self.age += 1
        self.money += self.salary
        
        # Random Life Events
        roll = random.random()
        if roll < 0.1:
            self.health -= 10; self.log("You felt sick (-10 Hlth)")
        elif roll < 0.2:
            self.happiness += 10; self.log("Had a great birthday party!")
        elif roll < 0.25:
            self.money += 500; self.log("Won a scratch-off ticket (+$500)")

        if self.age > 80 and random.random() < 0.2:
            self.alive = False; self.log("Died of natural causes.")

    def save_game(self):
        data = self.__dict__.copy()
        try:
            with open("titan_save.json", "w") as f: json.dump(data, f)
        except: pass

    def load_game(self):
        if os.path.exists("titan_save.json"):
            try:
                with open("titan_save.json", "r") as f:
                    data = json.load(f)
                    self.__dict__.update(data)
                return True
            except: pass
        return False

# --- UI: DASHBOARD (Safe, No Crashes) ---
class DashScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        self.engine = app.engine
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        # HEADER (Simple Text, No Cards to Crash)
        self.lbl_stats = MDLabel(
            text="Initializing...", 
            halign="center", 
            theme_text_color="Custom", 
            text_color=(0,1,0,1),
            font_style="H5",
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.lbl_stats)

        # LOG (Scrollable)
        scroll = MDScrollView(size_hint=(1, 0.5))
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        layout.add_widget(scroll)

        # MENU BUTTONS (Grid)
        row1 = MDBoxLayout(spacing=10, size_hint=(1, 0.1))
        row1.add_widget(MDRectangleFlatButton(text="CAREER", size_hint=(0.5, 1), on_release=lambda x: self.goto("career")))
        row1.add_widget(MDRectangleFlatButton(text="CRIME", size_hint=(0.5, 1), on_release=lambda x: self.goto("crime")))
        layout.add_widget(row1)

        row2 = MDBoxLayout(spacing=10, size_hint=(1, 0.1))
        row2.add_widget(MDRectangleFlatButton(text="ASSETS", size_hint=(0.5, 1), on_release=lambda x: self.goto("assets")))
        row2.add_widget(MDRectangleFlatButton(text="LOVE", size_hint=(0.5, 1), on_release=lambda x: self.goto("love")))
        layout.add_widget(row2)

        # AGE UP
        layout.add_widget(MDFillRoundFlatButton(text="AGE UP (+1 Year)", size_hint=(1, 0.15), on_release=self.do_age))

        self.add_widget(layout)
        self.update_display()

    def update_display(self):
        e = self.engine
        self.lbl_stats.text = f"AGE: {e.age} | ${e.money:,}\nJob: {e.job} | Hap: {e.happiness}%"
        self.log_list.clear_widgets()
        for txt in e.log_history[:20]:
            self.log_list.add_widget(TwoLineListItem(text=txt, secondary_text=""))

    def do_age(self, *args):
        self.engine.age_up()
        self.engine.save_game()
        self.update_display()

    def goto(self, name):
        self.manager.current = name

# --- UI: MENUS (Generic for Career, Crime, etc) ---
class MenuScreen(Screen):
    def __init__(self, menu_type, **kwargs):
        super().__init__(**kwargs)
        self.menu_type = menu_type
    
    def on_enter(self):
        self.engine = MDApp.get_running_app().engine
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        layout.add_widget(MDLabel(text=self.menu_type.upper(), halign="center", font_style="H4", size_hint=(1, 0.2)))
        
        scroll = MDScrollView()
        lst = MDList()
        
        # DYNAMIC CONTENT
        items = []
        if self.menu_type == "career":
            items = [("Janitor ($15k)", 15000), ("Chef ($40k)", 40000), ("Developer ($80k)", 80000), ("CEO ($200k)", 200000)]
            for title, sal in items:
                lst.add_widget(MDRectangleFlatButton(text=title, size_hint=(1, None), height=50, 
                    on_release=lambda x, t=title, s=sal: self.do_job(t, s)))
                    
        elif self.menu_type == "crime":
            items = [("Shoplift ($50)", 50, 0.1), ("Rob House ($5k)", 5000, 0.3), ("Bank Heist ($1M)", 1000000, 0.8)]
            for name, val, risk in items:
                lst.add_widget(MDRectangleFlatButton(text=name, size_hint=(1, None), height=50, 
                    on_release=lambda x, n=name, v=val, r=risk: self.do_crime(n, v, r)))

        elif self.menu_type == "assets":
            items = [("Used Car ($5k)", 5000), ("Luxury Car ($80k)", 80000), ("House ($200k)", 200000)]
            for name, cost in items:
                lst.add_widget(MDRectangleFlatButton(text=name, size_hint=(1, None), height=50, 
                    on_release=lambda x, n=name, c=cost: self.do_buy(n, c)))

        elif self.menu_type == "love":
             lst.add_widget(MDRectangleFlatButton(text="Find Partner", size_hint=(1, None), on_release=self.find_love))
             lst.add_widget(MDRectangleFlatButton(text="Have Child", size_hint=(1, None), on_release=self.have_kid))

        scroll.add_widget(lst)
        layout.add_widget(scroll)
        
        layout.add_widget(MDFillRoundFlatButton(text="BACK", size_hint=(1, 0.1), on_release=lambda x: self.go_back()))
        self.add_widget(layout)

    def go_back(self):
        self.manager.current = 'dash'

    def do_job(self, title, salary):
        self.engine.job = title
        self.engine.salary = salary
        self.engine.log(f"Hired as {title}!")
        self.go_back()

    def do_crime(self, name, val, risk):
        if random.random() > risk:
            self.engine.money += val
            self.engine.log(f"SUCCESS: {name} (+${val})")
        else:
            self.engine.happiness -= 20
            self.engine.log(f"FAILED: Caught trying to {name}!")
        self.go_back()

    def do_buy(self, name, cost):
        if self.engine.money >= cost:
            self.engine.money -= cost
            self.engine.assets.append(name)
            self.engine.log(f"Bought {name}!")
        else:
            self.engine.log("Not enough money!")
        self.go_back()

    def find_love(self, *args):
        names = ["Ashley", "Jessica", "Amanda", "Sarah", "Mike", "Chris", "Tom"]
        partner = random.choice(names)
        self.engine.relationships.append(partner)
        self.engine.log(f"Started dating {partner}!")
        self.go_back()

    def have_kid(self, *args):
        names = ["Liam", "Noah", "Emma", "Olivia"]
        kid = random.choice(names)
        self.engine.relationships.append(f"Child: {kid}")
        self.engine.log(f"Had a baby named {kid}!")
        self.go_back()

class TitanApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        self.engine = LifeEngine()
        self.engine.load_game() # Persistence
        
        # NO TRANSITIONS (Prevents graphics crash)
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(DashScreen(name='dash'))
        sm.add_widget(MenuScreen(name='career', menu_type='career'))
        sm.add_widget(MenuScreen(name='crime', menu_type='crime'))
        sm.add_widget(MenuScreen(name='assets', menu_type='assets'))
        sm.add_widget(MenuScreen(name='love', menu_type='love'))
        return sm

if __name__ == "__main__":
    try:
        TitanApp().run()
    except Exception as e:
        # LOG CRASH TO FILE
        with open("crash.log", "w") as f: f.write(traceback.format_exc())
