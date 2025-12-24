
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.scrollview import MDScrollView
import random

class LifeEngine:
    def __init__(self):
        self.age = 0
        self.money = 0
        self.health = 100
        self.smarts = random.randint(20, 90)
        self.job = None
        self.alive = True
        self.log_history = ["Born into a digital world."]

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")

    def age_up(self):
        self.age += 1
        if self.job:
            self.money += self.job['salary']
            if random.random() < 0.1:
                raise_amt = int(self.job['salary'] * 0.1)
                self.job['salary'] += raise_amt
                self.log(f"Got a raise! Salary: ${self.job['salary']}")
        
        # Random Events
        roll = random.random()
        if roll < 0.05:
            self.money += 100
            self.log("Found $100 on the street.")
        elif roll < 0.10:
            self.health -= 10
            self.log("Caught the flu.")
        
        if self.age > 80 and random.random() < 0.2:
            self.health = 0
        
        if self.health <= 0:
            self.alive = False
            self.log("DIED of natural causes.")

class GameScreen(MDScreen):
    def on_enter(self):
        self.engine = LifeEngine()
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Stats Card
        card = MDCard(orientation='vertical', size_hint=(1, 0.25), padding=15, md_bg_color=(0.1, 0.1, 0.1, 1))
        self.lbl_age = MDLabel(text="AGE: 0", halign="center", font_style="H5", theme_text_color="Custom", text_color=(1,1,1,1))
        self.lbl_money = MDLabel(text="$0", halign="center", font_style="H6", theme_text_color="Custom", text_color=(0,1,0,1))
        self.lbl_job = MDLabel(text="Unemployed", halign="center", theme_text_color="Secondary")
        card.add_widget(self.lbl_age)
        card.add_widget(self.lbl_money)
        card.add_widget(self.lbl_job)
        layout.add_widget(card)

        # Log
        scroll = MDScrollView()
        self.list = MDList()
        scroll.add_widget(self.list)
        layout.add_widget(scroll)

        # Actions
        grid = MDBoxLayout(spacing=10, size_hint_y=None, height=50)
        grid.add_widget(MDRectangleFlatButton(text="JOB", on_release=self.menu_job))
        grid.add_widget(MDRectangleFlatButton(text="CRIME", on_release=self.menu_crime))
        grid.add_widget(MDRectangleFlatButton(text="DOC", on_release=self.menu_doc))
        layout.add_widget(grid)

        # Age Button
        btn = MDFillRoundFlatButton(text="AGE UP", size_hint=(1, 0.1), on_release=self.do_age)
        layout.add_widget(btn)
        
        self.add_widget(layout)
        self.update_ui()

    def update_ui(self):
        e = self.engine
        self.lbl_age.text = f"AGE: {e.age}"
        self.lbl_money.text = f"${e.money:,}"
        self.lbl_job.text = e.job['title'] if e.job else "Unemployed"
        
        self.list.clear_widgets()
        for txt in e.log_history[:20]:
            self.list.add_widget(TwoLineListItem(text=txt, secondary_text=""))

    def do_age(self, *args):
        if not self.engine.alive: return
        self.engine.age_up()
        self.update_ui()

    def menu_job(self, *args):
        if self.engine.age < 18: return
        self.engine.job = {"title": "Developer", "salary": 60000}
        self.engine.log("Hired as Developer!")
        self.update_ui()

    def menu_crime(self, *args):
        if random.random() > 0.5:
            self.engine.money += 5000
            self.engine.log("Robbed a bank! +$5000")
        else:
            self.engine.log("Almost got caught!")
        self.update_ui()

    def menu_doc(self, *args):
        if self.engine.money >= 500:
            self.engine.money -= 500
            self.engine.health = 100
            self.engine.log("Visited doctor. Health restored.")
            self.update_ui()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GameScreen()

if __name__ == "__main__":
    MainApp().run()
