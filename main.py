import os, sys, random, traceback
os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.progressbar import MDProgressBar

# --- CORE LOGIC ---
class LifeEngine:
    def __init__(self):
        self.name = "Bit Player"
        self.age = 0
        self.money = 0
        self.career = "Unemployed"
        # The Big 4 Stats
        self.happiness = 90
        self.health = 100
        self.smarts = random.randint(30, 90)
        self.looks = random.randint(30, 90)
        self.alive = True
        self.log_history = ["You were born into a simulation."]
        self.parents = [{"name": "Mom", "rel": 100}, {"name": "Dad", "rel": 100}]

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")

    def age_up(self):
        if not self.alive: return
        self.age += 1
        
        # Salary
        if self.career != "Unemployed":
            pay = 50000 if "Developer" in self.career else 20000
            self.money += pay
            
        # Random Life Events
        roll = random.random()
        if roll < 0.15:
            self.happiness -= 10
            self.log("You felt depressed.")
        elif roll < 0.30:
            self.health -= 5
            self.log("Contracted a minor illness.")
        elif roll < 0.40:
             self.log("Parents argued all night.")

        if self.health <= 0:
            self.alive = False
            self.log("DIED.")

# --- UI COMPONENTS ---
class StatBar(MDBoxLayout):
    def __init__(self, label, value, color, **kwargs):
        super().__init__(orientation='vertical', size_hint_x=0.25, **kwargs)
        self.add_widget(MDLabel(text=f"{label}: {value}%", halign="center", font_style="Caption", theme_text_color="Custom", text_color=color))
        self.bar = MDProgressBar(value=value, color=color, size_hint_y=None, height="4dp")
        self.add_widget(self.bar)

# --- MAIN SCREEN (THE BITLIFE LOOK) ---
class MainGame(Screen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        # ROOT: Vertical Layout
        root = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. TOP HEADER (Name | Wealth | Career)
        header = MDBoxLayout(orientation='vertical', size_hint=(1, 0.15))
        self.lbl_name = MDLabel(text=f"{self.engine.name}", font_style="H5", halign="center")
        self.lbl_sub = MDLabel(text=f"Wealth: ${self.engine.money:,} | {self.engine.career}", font_style="Subtitle1", halign="center", theme_text_color="Secondary")
        header.add_widget(self.lbl_name)
        header.add_widget(self.lbl_sub)
        root.add_widget(header)

        # 2. THE LOG (The Main BitLife Area)
        # White text on dark bg, scrollable
        scroll = MDScrollView(size_hint=(1, 0.5))
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        root.add_widget(scroll)

        # 3. AGE BUTTON (Massive Center Button)
        mid_box = MDBoxLayout(padding=[40, 10], size_hint=(1, 0.15))
        btn_age = MDFillRoundFlatButton(
            text=f"AGE UP\n(+1 Year)", 
            font_size=24,
            size_hint=(1, 1),
            md_bg_color=(0, 0.7, 0, 1), # BitLife Green
            on_release=self.do_age
        )
        mid_box.add_widget(btn_age)
        root.add_widget(mid_box)

        # 4. THE 4 BARS (Hap, Hlth, Smrt, Look)
        stats_box = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=5)
        self.bar_hap = StatBar("Hap", self.engine.happiness, (0,1,0,1))   # Green
        self.bar_hlt = StatBar("Hlth", self.engine.health, (1,0,0,1))     # Red
        self.bar_smr = StatBar("Smrt", self.engine.smarts, (0,0,1,1))     # Blue
        self.bar_lok = StatBar("Look", self.engine.looks, (1,0.6,0,1))    # Orange
        stats_box.add_widget(self.bar_hap)
        stats_box.add_widget(self.bar_hlt)
        stats_box.add_widget(self.bar_smr)
        stats_box.add_widget(self.bar_lok)
        root.add_widget(stats_box)

        # 5. BOTTOM NAV (Assets | Relat | Activities)
        nav_box = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=2)
        nav_box.add_widget(MDRectangleFlatButton(text="ASSETS", size_hint=(0.33, 1), on_release=lambda x: self.open_menu("assets")))
        nav_box.add_widget(MDRectangleFlatButton(text="RELATION", size_hint=(0.33, 1), on_release=lambda x: self.open_menu("relation")))
        nav_box.add_widget(MDRectangleFlatButton(text="ACTIVITY", size_hint=(0.33, 1), on_release=lambda x: self.open_menu("activity")))
        root.add_widget(nav_box)

        self.add_widget(root)
        self.update_display()

    def update_display(self):
        e = self.engine
        self.lbl_name.text = f"{e.name} ({e.age})"
        self.lbl_sub.text = f"Bank: ${e.money:,} | Job: {e.career}"
        
        # Update Bars
        self.bar_hap.children[1].value = e.happiness
        self.bar_hlt.children[1].value = e.health
        self.bar_smr.children[1].value = e.smarts
        self.bar_lok.children[1].value = e.looks

        # Update Log
        self.log_list.clear_widgets()
        for txt in e.log_history[:30]:
            self.log_list.add_widget(TwoLineListItem(text=txt, secondary_text=""))

    def do_age(self, *args):
        self.engine.age_up()
        self.update_display()

    def open_menu(self, menu_type):
        self.manager.current = menu_type

# --- MENU SCREEN (Activities, Relations, Assets) ---
class MenuScreen(Screen):
    def __init__(self, name, title, items, **kwargs):
        super().__init__(name=name, **kwargs)
        self.title = title
        self.items = items # List of (Label, Callback)

    def on_enter(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=20)
        
        # Header
        layout.add_widget(MDLabel(text=self.title, font_style="H4", halign="center", size_hint=(1, 0.15)))
        
        # Scrollable List
        scroll = MDScrollView()
        lst = MDList()
        
        for text, func in self.items:
            lst.add_widget(MDRectangleFlatButton(
                text=text, 
                size_hint=(1, None), 
                height="60dp",
                on_release=func
            ))
            
        scroll.add_widget(lst)
        layout.add_widget(scroll)
        
        # Back Button
        layout.add_widget(MDFillRoundFlatButton(text="CLOSE", size_hint=(1, 0.1), on_release=self.go_back))
        self.add_widget(layout)

    def go_back(self, *args):
        self.manager.current = 'game'

class CloneApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.engine = LifeEngine()
        
        sm = ScreenManager(transition=NoTransition())
        
        # 1. Main Game
        sm.add_widget(MainGame(name='game'))
        
        # 2. Activity Menu
        act_items = [
            ("Mind & Body (Gym, Meditate)", self.do_gym),
            ("Love (Date, Hookup)", self.do_love),
            ("Crime (Rob, Murder)", self.do_crime),
            ("Doctor (Cure Disease)", self.do_doc),
            ("Jobs (Apply, Quit)", self.do_job),
            ("Emigrate (Move Country)", self.do_move)
        ]
        sm.add_widget(MenuScreen("activity", "Activities", act_items))

        # 3. Relationship Menu
        rel_items = [
            ("Mother (Interact)", self.interact_mom),
            ("Father (Interact)", self.interact_dad)
        ]
        sm.add_widget(MenuScreen("relation", "Relationships", rel_items))

        # 4. Assets Menu
        asset_items = [
            ("Go Shopping (Cars, Jewelry)", self.do_shop),
            ("Real Estate (Houses)", self.do_realestate)
        ]
        sm.add_widget(MenuScreen("assets", "Assets", asset_items))
        
        return sm

    # --- ACTIONS ---
    def log(self, t): self.engine.log(t)
    
    def do_gym(self, *x):
        self.engine.health = min(100, self.engine.health + 5)
        self.engine.looks = min(100, self.engine.looks + 2)
        self.log("You went to the gym.")
        self.root.current = 'game'

    def do_love(self, *x):
        self.log("You went on a date. It went okay.")
        self.root.current = 'game'

    def do_crime(self, *x):
        if random.random() > 0.5:
            self.engine.money += 1000
            self.log("You robbed a house! (+$1000)")
        else:
            self.engine.happiness -= 20
            self.log("Police caught you! You hired a lawyer.")
        self.root.current = 'game'
        
    def do_doc(self, *x):
        self.engine.money -= 100
        self.engine.health = 100
        self.log("Dr. Mario cured you. (-$100)")
        self.root.current = 'game'

    def do_job(self, *x):
        self.engine.career = "App Developer"
        self.log("You were hired as an App Developer!")
        self.root.current = 'game'

    def do_move(self, *x): self.log("You moved to Canada."); self.root.current = 'game'
    def interact_mom(self, *x): self.log("You gave your mom a hug."); self.root.current = 'game'
    def interact_dad(self, *x): self.log("Your dad gave you $50."); self.engine.money += 50; self.root.current = 'game'
    def do_shop(self, *x): self.log("You bought a fake Rolex."); self.engine.money -= 200; self.root.current = 'game'
    def do_realestate(self, *x): self.log("You can't afford a house yet."); self.root.current = 'game'

if __name__ == "__main__":
    try:
        CloneApp().run()
    except Exception as e:
        with open("crash.txt", "w") as f: f.write(traceback.format_exc())
