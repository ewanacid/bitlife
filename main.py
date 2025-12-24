from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
import random

# --- GAME ENGINE ---
class LifeEngine:
    def __init__(self):
        self.age = 0
        self.money = 0
        self.happiness = 100
        self.health = 100
        self.job = "Unemployed"
        self.salary = 0
        self.assets = []
        self.alive = True

    def age_up(self):
        self.age += 1
        self.money += self.salary
        
        # Age-based events
        event = ""
        if self.age < 5:
            event = random.choice(["Learned to walk.", "Said first word.", "Cried all night.", "Ate dirt."])
        elif self.age < 18:
            event = random.choice(["Got an A in math.", "Bullied at school.", "First kiss!", "Skipped class."])
        elif self.age > 60:
            self.health -= random.randint(5, 15)
            event = random.choice(["Back pain started.", "Retired from bingo.", "Forgot where keys are.", "Grandkids visited."])
        else:
            # Adult events
            if self.job == "Unemployed":
                event = random.choice(["Looked for work.", "Watched TV all day.", "Went to the park."])
            else:
                event = random.choice([f"Worked hard as a {self.job}.", "Boss yelled at you.", "Got a small raise!", "Boring day at work."])

        # Random Chaos
        if random.random() < 0.1:
            chaos = random.choice([("Won the lottery!", 5000), ("Got robbed!", -500), ("Found $20", 20)])
            event += f" AND {chaos[0]}"
            self.money += chaos[1]

        return event

# --- UI SCREENS ---
class MenuScreen(MDScreen):
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=40, spacing=20, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        title = MDLabel(text="BITLIFE ELITE", halign="center", font_style="H3", theme_text_color="Primary")
        layout.add_widget(title)
        
        btn = MDFillRoundFlatButton(
            text="START NEW LIFE",
            font_size=24,
            pos_hint={'center_x': 0.5},
            on_release=self.start_game
        )
        layout.add_widget(btn)
        self.add_widget(layout)

    def start_game(self, instance):
        self.manager.current = 'game'

class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = LifeEngine()
        self.dialog = None

    def on_enter(self):
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        # 1. DASHBOARD CARD (Stats)
        card = MDCard(orientation='vertical', size_hint=(1, 0.25), padding=10, radius=[15])
        self.age_lbl = MDLabel(text="AGE: 0", halign="center", font_style="H5")
        self.money_lbl = MDLabel(text="BANK: $0", halign="center", theme_text_color="Custom", text_color=(0,1,0,1))
        self.job_lbl = MDLabel(text="JOB: Unemployed", halign="center", font_style="Caption")
        
        stats_box = MDBoxLayout(orientation='horizontal')
        self.hap_lbl = MDLabel(text="Hap: 100%", halign="center")
        self.hlt_lbl = MDLabel(text="Hlt: 100%", halign="center")
        stats_box.add_widget(self.hap_lbl)
        stats_box.add_widget(self.hlt_lbl)

        card.add_widget(self.age_lbl)
        card.add_widget(self.money_lbl)
        card.add_widget(self.job_lbl)
        card.add_widget(stats_box)
        main_layout.add_widget(card)

        # 2. EVENT LOG
        scroll = MDScrollView(size_hint=(1, 0.5))
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        main_layout.add_widget(scroll)

        # 3. ACTION BUTTONS
        actions = MDBoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        
        job_btn = MDRectangleFlatButton(text="JOBS", size_hint=(0.3, 1), on_release=self.show_jobs)
        buy_btn = MDRectangleFlatButton(text="SHOP", size_hint=(0.3, 1), on_release=self.show_shop)
        actions.add_widget(job_btn)
        actions.add_widget(buy_btn)
        main_layout.add_widget(actions)

        # 4. AGE UP BUTTON (BIG)
        age_btn = MDFillRoundFlatButton(text="AGE UP (+1 Year)", size_hint=(1, 0.15), font_size=20, on_release=self.age_up)
        main_layout.add_widget(age_btn)

        self.add_widget(main_layout)
        self.log("You were born.")

    def update_display(self):
        self.age_lbl.text = f"AGE: {self.engine.age}"
        self.money_lbl.text = f"BANK: ${self.engine.money}"
        self.job_lbl.text = f"JOB: {self.engine.job} (${self.engine.salary}/yr)"
        self.hap_lbl.text = f"Hap: {self.engine.happiness}%"
        self.hlt_lbl.text = f"Hlt: {self.engine.health}%"

    def log(self, text):
        item = TwoLineListItem(text=f"Age {self.engine.age}", secondary_text=text)
        self.log_list.add_widget(item, index=0) # Add to top

    def age_up(self, instance):
        if not self.engine.alive: return
        event = self.engine.age_up()
        self.log(event)
        self.update_display()
        
        if self.engine.health <= 0:
            self.engine.alive = False
            self.log("YOU HAVE DIED.")
            instance.text = "GAME OVER"
            instance.disabled = True

    # --- POPUPS ---
    def show_jobs(self, instance):
        if self.engine.age < 18:
            self.log("Too young to work!"); return
        
        self.close_dialog()
        # Simple job list
        jobs = [("Janitor", 15000), ("Developer", 60000), ("Doctor", 120000)]
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height=200)
        
        for name, salary in jobs:
            b = MDRectangleFlatButton(text=f"{name} (${salary})", on_release=lambda x, n=name, s=salary: self.apply_job(n, s))
            content.add_widget(b)

        self.dialog = MDDialog(title="Job Listings", type="custom", content_cls=content)
        self.dialog.open()

    def apply_job(self, name, salary):
        self.engine.job = name
        self.engine.salary = salary
        self.log(f"Hired as {name}!")
        self.update_display()
        self.close_dialog()

    def show_shop(self, instance):
        self.close_dialog()
        items = [("Used Car", 5000), ("House", 100000), ("Fancy Suit", 1000)]
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height=200)
        
        for name, price in items:
            b = MDRectangleFlatButton(text=f"{name} (${price})", on_release=lambda x, n=name, p=price: self.buy_item(n, p))
            content.add_widget(b)

        self.dialog = MDDialog(title="Marketplace", type="custom", content_cls=content)
        self.dialog.open()

    def buy_item(self, name, price):
        if self.engine.money >= price:
            self.engine.money -= price
            self.engine.assets.append(name)
            self.log(f"Bought a {name}!")
        else:
            self.log(f"Can't afford {name}.")
        self.update_display()
        self.close_dialog()

    def close_dialog(self, *args):
        if self.dialog: self.dialog.dismiss()

class BitLifeApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        
        sm = MDScreenManager()
        
        menu = MenuScreen(name='menu')
        menu.build_ui()
        sm.add_widget(menu)
        
        game = GameScreen(name='game')
        sm.add_widget(game)
        
        return sm

if __name__ == "__main__":
    BitLifeApp().run()
