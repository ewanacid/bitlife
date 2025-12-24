import random, json, os, traceback
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog

# --- SAVE SYSTEM ---
SAVE_FILE = "bitlife_save.json"

class LifeEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.age = 0
        self.money = 0
        self.happiness = 100
        self.health = 100
        self.alive = True
        self.job = None # {title, salary}
        self.assets = [] # list of strings
        self.children = [] # list of {name, age, relation}
        self.criminal = False
        self.log_history = ["Born into a new life."]

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")

    def age_up(self):
        if not self.alive: return
        self.age += 1
        
        # 1. INCOME
        if self.job:
            self.money += self.job['salary']
            if random.random() < 0.1:
                raise_amt = int(self.job['salary'] * 0.1)
                self.job['salary'] += raise_amt
                self.log(f"Promotion! New salary: ${self.job['salary']}")

        # 2. CHILDREN AGING
        if self.children:
            for child in self.children:
                child['age'] += 1
                if child['age'] == 18:
                    self.log(f"{child['name']} moved out.")
            # Random child event
            if random.random() < 0.2:
                kid = random.choice(self.children)
                self.log(f"{kid['name']} (Age {kid['age']}) drew you a picture.")

        # 3. RANDOM EVENTS
        roll = random.random()
        if roll < 0.05:
            self.money += 100; self.log("Found $100 on the street.")
        elif roll < 0.10:
            self.health -= 10; self.log("Contracted the flu.")
        elif roll < 0.12:
            self.happiness -= 10; self.log("Stepped in gum.")

        # 4. DEATH CHECK
        if self.age > 80 and random.random() < 0.15: self.health = 0
        if self.health <= 0:
            self.alive = False
            self.log("DIED of natural causes.")

    def save(self):
        data = {
            "age": self.age, "money": self.money, "health": self.health,
            "job": self.job, "children": self.children, "log": self.log_history
        }
        with open(SAVE_FILE, "w") as f: json.dump(data, f)

    def load(self):
        if not os.path.exists(SAVE_FILE): return False
        try:
            with open(SAVE_FILE, "r") as f: data = json.load(f)
            self.age = data["age"]
            self.money = data["money"]
            self.health = data["health"]
            self.job = data["job"]
            self.children = data["children"]
            self.log_history = data["log"]
            return True
        except: return False

class GameScreen(MDScreen):
    def on_enter(self):
        self.engine = LifeEngine()
        # Auto-load if exists
        if self.engine.load():
            self.engine.log("Game Loaded.")
        self.dialog = None
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=15)
        
        # STATS CARD
        card = MDCard(orientation='vertical', size_hint=(1, 0.25), padding=10, md_bg_color=(0.1,0.1,0.1,1))
        self.lbl_main = MDLabel(text="AGE: 0 | BANK: $0", halign="center", font_style="H6", theme_text_color="Custom", text_color=(0,1,0,1))
        self.lbl_sub = MDLabel(text="Job: Unemployed | Health: 100%", halign="center", theme_text_color="Secondary")
        self.lbl_kids = MDLabel(text="Children: 0", halign="center", font_style="Caption")
        card.add_widget(self.lbl_main)
        card.add_widget(self.lbl_sub)
        card.add_widget(self.lbl_kids)
        layout.add_widget(card)

        # LOG
        scroll = MDScrollView()
        self.list = MDList()
        scroll.add_widget(self.list)
        layout.add_widget(scroll)

        # BUTTON GRID
        grid = MDBoxLayout(spacing=10, size_hint_y=None, height=50)
        grid.add_widget(MDRectangleFlatButton(text="JOB", on_release=self.menu_job))
        grid.add_widget(MDRectangleFlatButton(text="CRIME", on_release=self.menu_crime))
        grid.add_widget(MDRectangleFlatButton(text="LOVE", on_release=self.menu_love))
        layout.add_widget(grid)

        # AGE BUTTON
        layout.add_widget(MDFillRoundFlatButton(text="AGE UP (+1 Year)", size_hint=(1, 0.1), on_release=self.do_age))
        
        self.add_widget(layout)
        self.update_ui()

    def update_ui(self):
        e = self.engine
        self.lbl_main.text = f"AGE: {e.age} | BANK: ${e.money:,}"
        job_title = e.job['title'] if e.job else "Unemployed"
        self.lbl_sub.text = f"Job: {job_title} | Health: {e.health}%"
        self.lbl_kids.text = f"Children: {len(e.children)}"
        
        self.list.clear_widgets()
        for txt in e.log_history[:30]:
            self.list.add_widget(TwoLineListItem(text=txt, secondary_text=""))

    def do_age(self, *args):
        if self.engine.alive:
            self.engine.age_up()
            self.engine.save() # Auto-save
            self.update_ui()

    def menu_job(self, *args):
        if self.engine.age < 18:
            self.engine.log("Too young to work.")
        else:
            self.engine.job = {"title": "Developer", "salary": 60000}
            self.engine.log("Hired as Developer ($60k/yr)")
        self.update_ui()

    def menu_crime(self, *args):
        if random.random() < 0.6:
            self.engine.money += 5000
            self.engine.log("Robbed a bank! (+$5000)")
        else:
            self.engine.happiness -= 20
            self.engine.log("Almost got caught by police!")
        self.update_ui()

    def menu_love(self, *args):
        if self.engine.age < 18: return
        # Simple "Have Kid" Mechanic
        name = random.choice(["Liam", "Olivia", "Noah", "Emma", "James"])
        self.engine.children.append({"name": name, "age": 0})
        self.engine.log(f"You had a baby named {name}!")
        self.update_ui()

class Gen4App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        try:
            return GameScreen()
        except:
            return MDLabel(text="CRASH: " + traceback.format_exc())

if __name__ == "__main__":
    Gen4App().run()
