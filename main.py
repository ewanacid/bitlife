import os, sys, random, traceback, json
os.environ["KIVY_NO_ARGS"] = "1"

from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.list import MDList, TwoLineListItem, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog

# --- DATA BANKS (THE CONTENT) ---
JOBS = {
    "Jr. Janitor": {"sal": 15000, "req": 0},
    "Apprentice Chef": {"sal": 25000, "req": 0},
    "Soldier": {"sal": 30000, "req": 18},
    "Teacher": {"sal": 45000, "req": 22}, # Needs Uni
    "App Developer": {"sal": 70000, "req": 22},
    "Brain Surgeon": {"sal": 250000, "req": 26}, # Needs Med School
}

HOUSES = [
    ("Trailer", 15000), ("Studio", 80000), ("Condo", 200000), 
    ("Mansion", 2000000), ("Private Island", 10000000)
]

CARS = [
    ("Rusty Sedan", 2000), ("Used Honda", 5000), ("New Tesla", 50000), 
    ("Ferrari", 250000), ("Bugatti", 2000000)
]

# --- CORE ENGINE ---
class LifeEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.name = "Bit Player"
        self.age = 0
        self.money = 0
        self.career = "Unemployed"
        self.education = "None" # High School, BS, MD
        self.happiness = 90
        self.health = 100
        self.smarts = random.randint(20, 90)
        self.looks = random.randint(20, 90)
        self.alive = True
        self.parents = {"Mom": 100, "Dad": 100}
        self.assets = []
        self.log_history = ["You were born."]
        self.partner = None # {name, rel}

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")

    def check_death(self):
        if self.health <= 0:
            self.alive = False
            self.log("You have DIED.")
            return True
        return False

    def age_up(self):
        if not self.alive: return
        self.age += 1
        
        # 1. LIFE STAGES
        if self.age < 6:
            self.run_baby_events()
        elif self.age < 18:
            self.run_school_events()
        else:
            self.run_adult_events()

        # 2. RANDOM CHAOS
        if random.random() < 0.05:
            self.health -= 10
            self.log("You contracted a disease.")
        
        self.check_death()

    def run_baby_events(self):
        events = ["Cried all night.", "Said your first word.", "Ate some dirt.", "Bit your brother."]
        self.log(random.choice(events))

    def run_school_events(self):
        self.smarts += random.randint(1, 5)
        if random.random() < 0.2:
            self.happiness -= 10
            self.log("A bully stole your lunch.")
        else:
            self.log("You studied hard at school.")

    def run_adult_events(self):
        # INCOME
        if self.career != "Unemployed":
            sal = JOBS.get(self.career, {"sal":0})["sal"]
            # Raises
            if random.random() < 0.1:
                sal = int(sal * 1.1)
                self.log(f"You got a raise! New salary: ${sal}")
            self.money += sal
            self.log(f"Earned ${sal} from your job.")
        
        # BILLS
        if self.age > 20:
            tax = int(self.money * 0.15)
            self.money -= tax
            self.log(f"Paid ${tax} in taxes.")

# --- UI LAYER ---
class MainGame(Screen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(orientation='vertical', padding=10, spacing=5)

        # 1. HEADER
        self.lbl_head = MDLabel(text="", font_style="H5", halign="center", size_hint=(1, 0.1))
        self.lbl_sub = MDLabel(text="", font_style="Subtitle1", halign="center", theme_text_color="Secondary", size_hint=(1, 0.05))
        root.add_widget(self.lbl_head)
        root.add_widget(self.lbl_sub)

        # 2. LOG
        scroll = MDScrollView(size_hint=(1, 0.45))
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        root.add_widget(scroll)

        # 3. AGE BUTTON
        btn_age = MDFillRoundFlatButton(
            text="AGE UP", font_size=26, size_hint=(1, 0.15),
            md_bg_color=(0, 0.7, 0, 1), on_release=self.do_age
        )
        root.add_widget(btn_age)

        # 4. STAT BARS
        stats = MDBoxLayout(size_hint=(1, 0.1), spacing=5)
        self.bar_hap = self.make_bar("Hap", (0,1,0,1))
        self.bar_hlt = self.make_bar("Hlt", (1,0,0,1))
        self.bar_smr = self.make_bar("Smrt", (0,0,1,1))
        self.bar_lok = self.make_bar("Look", (1,0.5,0,1))
        stats.add_widget(self.bar_hap); stats.add_widget(self.bar_hlt)
        stats.add_widget(self.bar_smr); stats.add_widget(self.bar_lok)
        root.add_widget(stats)

        # 5. MENU NAV
        nav = MDBoxLayout(size_hint=(1, 0.1), spacing=2)
        nav.add_widget(MDRectangleFlatButton(text="OCCUPATION", size_hint=(0.33, 1), on_release=lambda x: self.menu("job")))
        nav.add_widget(MDRectangleFlatButton(text="ASSETS", size_hint=(0.33, 1), on_release=lambda x: self.menu("shop")))
        nav.add_widget(MDRectangleFlatButton(text="ACTIVITIES", size_hint=(0.33, 1), on_release=lambda x: self.menu("act")))
        root.add_widget(nav)

        self.add_widget(root)
        self.update_display()

    def make_bar(self, name, color):
        box = MDBoxLayout(orientation='vertical')
        box.add_widget(MDLabel(text=name, halign="center", font_style="Caption", theme_text_color="Custom", text_color=color))
        self.pb = MDProgressBar(value=50, color=color, size_hint_y=None, height="4dp")
        box.add_widget(self.pb)
        return box

    def update_display(self):
        e = self.engine
        self.lbl_head.text = f"{e.name} ({e.age})"
        self.lbl_sub.text = f"${e.money:,} | {e.career}"
        
        # Bars (Hacky access to children, but fast)
        self.bar_hap.children[0].value = e.happiness
        self.bar_hlt.children[0].value = e.health
        self.bar_smr.children[0].value = e.smarts
        self.bar_lok.children[0].value = e.looks

        self.log_list.clear_widgets()
        for txt in e.log_history[:40]:
            self.log_list.add_widget(TwoLineListItem(text=txt, secondary_text=""))

    def do_age(self, *args):
        self.engine.age_up()
        self.update_display()
    
    def menu(self, type):
        self.manager.current = type

# --- MENU SCREENS ---
class Menu(Screen):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
    
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.build_ui()

    def go_home(self, *x): self.manager.current = 'game'

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=20)
        
        scroll = MDScrollView()
        lst = MDList()
        
        # DYNAMIC LOGIC
        if self.name == "job":
            if self.app.engine.age < 18:
                lst.add_widget(OneLineListItem(text="You are too young to work!"))
            else:
                for title, data in JOBS.items():
                    lst.add_widget(MDRectangleFlatButton(
                        text=f"{title} (${data['sal']})", size_hint=(1, None),
                        on_release=lambda x, t=title: self.apply_job(t)
                    ))

        elif self.name == "shop":
            if self.app.engine.age < 18:
                lst.add_widget(OneLineListItem(text="Ask your parents first!"))
            else:
                lst.add_widget(MDLabel(text="--- REAL ESTATE ---"))
                for name, price in HOUSES:
                    lst.add_widget(MDRectangleFlatButton(text=f"{name} (${price:,})", on_release=lambda x, n=name, p=price: self.buy(n,p)))
                lst.add_widget(MDLabel(text="\n--- VEHICLES ---"))
                for name, price in CARS:
                    lst.add_widget(MDRectangleFlatButton(text=f"{name} (${price:,})", on_release=lambda x, n=name, p=price: self.buy(n,p)))

        elif self.name == "act":
            opts = [("Doctor ($100)", self.doc), ("Club ($50)", self.club), ("Study", self.study), ("Crime", self.crime)]
            for txt, func in opts:
                 lst.add_widget(MDRectangleFlatButton(text=txt, size_hint=(1, None), on_release=func))

        scroll.add_widget(lst)
        layout.add_widget(scroll)
        layout.add_widget(MDFillRoundFlatButton(text="BACK", size_hint=(1, 0.1), on_release=self.go_home))
        self.add_widget(layout)

    def apply_job(self, title):
        e = self.app.engine
        req = JOBS[title]["req"]
        if e.age < req:
            e.log(f"Rejected! You need to be {req}+.")
        else:
            e.career = title
            e.log(f"HIRED! You are now a {title}.")
        self.go_home()

    def buy(self, name, price):
        e = self.app.engine
        if e.money >= price:
            e.money -= price
            e.assets.append(name)
            e.happiness = 100
            e.log(f"Bought a {name}!")
        else:
            e.log(f"You can't afford a {name}.")
        self.go_home()

    def doc(self, *x): 
        e = self.app.engine; e.money -= 100; e.health = 100; e.log("Cured."); self.go_home()
    def club(self, *x): 
        e = self.app.engine; e.money -= 50; e.happiness += 20; e.log("Partied hard."); self.go_home()
    def study(self, *x): 
        e = self.app.engine; e.smarts += 5; e.log("Studied."); self.go_home()
    def crime(self, *x): 
        e = self.app.engine; 
        if random.random() > 0.5: e.money += 1000; e.log("Robbed store!") 
        else: e.happiness -= 30; e.log("Jail time!")
        self.go_home()

class GodApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        self.engine = LifeEngine()
        
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(MainGame(name='game'))
        sm.add_widget(Menu(name='job'))
        sm.add_widget(Menu(name='shop'))
        sm.add_widget(Menu(name='act'))
        return sm

if __name__ == "__main__":
    try:
        GodApp().run()
    except Exception as e:
        with open("crash.txt", "w") as f: f.write(traceback.format_exc())
