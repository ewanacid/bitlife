import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineListItem, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

# --- CORE LOGIC ENGINE ---
class LifeEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.age = 0
        self.money = 0
        self.happiness = 100
        self.health = 100
        self.smarts = random.randint(30, 90)
        self.looks = random.randint(30, 90)
        self.alive = True
        self.job = None # {title, salary, years}
        self.education = "None"
        self.criminal_record = False
        self.jail_years = 0
        self.assets = []
        self.relationships = [] # {name, relation, stats}
        self.log = ["You were born into a chaotic world."]

    def add_log(self, text):
        self.log.insert(0, f"Age {self.age}: {text}")

    def age_up(self):
        if not self.alive: return
        self.age += 1
        
        # 1. JAIL CHECK
        if self.jail_years > 0:
            self.jail_years -= 1
            self.happiness -= 10
            self.add_log(f"Stuck in prison. {self.jail_years} years left.")
            if self.jail_years == 0:
                self.add_log("RELEASED FROM PRISON!")
            return

        # 2. JOB LOGIC
        if self.job:
            self.money += self.job['salary']
            self.job['years'] += 1
            # Raise / Promotion Chance
            if random.random() < 0.15:
                raise_amt = int(self.job['salary'] * 0.1)
                self.job['salary'] += raise_amt
                self.add_log(f"Got a raise! New salary: ${self.job['salary']}")
        
        # 3. HEALTH DECAY
        if self.age > 50: self.health -= random.randint(0, 5)
        if self.health <= 0:
            self.alive = False
            self.add_log("DIED of natural causes.")
            return

        # 4. RANDOM EVENTS ( The Fun Stuff )
        roll = random.random()
        if roll < 0.05:
            self.money += 100
            self.add_log("Found a wallet on the street!")
        elif roll < 0.10:
            self.health -= 10
            self.add_log("Contracted a weird virus.")
        elif roll < 0.15 and self.age > 18:
            self.add_log("Met someone special at a bar.")
            self.relationships.append({"name": "Partner", "relation": "Dating", "love": 50})

# --- UI LAYER ---
class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = LifeEngine()
        self.dialog = None

    def on_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        
        # MAIN NAV LAYOUT
        nav = MDBottomNavigation(selected_color_background="blue", text_color_active="lightblue")

        # TAB 1: DASHBOARD
        screen1 = MDBottomNavigationItem(name='dash', text='Home', icon='home')
        layout1 = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Stats Card
        self.stats_card = MDCard(orientation='vertical', size_hint=(1, 0.35), padding=15, radius=[15], md_bg_color=(0.1,0.1,0.1,1))
        self.lbl_age = MDLabel(text="AGE: 0", font_style="H4", halign="center", theme_text_color="Custom", text_color=(1,1,1,1))
        self.lbl_bank = MDLabel(text="$0", font_style="H5", halign="center", theme_text_color="Custom", text_color=(0,1,0,1))
        self.lbl_bars = MDLabel(text="Hap: 100 | Hlt: 100 | Smrt: 50", halign="center", font_style="Caption")
        self.stats_card.add_widget(self.lbl_age)
        self.stats_card.add_widget(self.lbl_bank)
        self.stats_card.add_widget(self.lbl_bars)
        layout1.add_widget(self.stats_card)

        # Event Log
        scroll = MDScrollView()
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        layout1.add_widget(scroll)

        # AGE UP BUTTON
        self.btn_age = MDFillRoundFlatButton(text="AGE UP (+1 Year)", font_size=22, size_hint=(1, 0.15), on_release=self.do_age_up)
        layout1.add_widget(self.btn_age)
        screen1.add_widget(layout1)

        # TAB 2: ACTIVITIES (Jobs, Crime, Love)
        screen2 = MDBottomNavigationItem(name='act', text='Activities', icon='star')
        layout2 = MDScrollView()
        list2 = MDList()
        
        acts = [
            ("Education", "university", self.menu_edu),
            ("Careers", "briefcase", self.menu_jobs),
            ("Crime", "pistol", self.menu_crime),
            ("Casino", "cards", self.menu_casino),
            ("Assets", "home", self.menu_shop),
            ("Doctor", "hospital", self.visit_doctor)
        ]
        
        for name, icon, func in acts:
            item = OneLineAvatarIconListItem(text=name, on_release=func)
            item.add_widget(IconLeftWidget(icon=icon))
            list2.add_widget(item)
            
        layout2.add_widget(list2)
        screen2.add_widget(layout2)

        nav.add_widget(screen1)
        nav.add_widget(screen2)
        self.add_widget(nav)
        self.update_ui()

    # --- UPDATE LOOPS ---
    def update_ui(self):
        e = self.engine
        self.lbl_age.text = f"AGE: {e.age}"
        self.lbl_bank.text = f"${e.money:,}"
        self.lbl_bars.text = f"Hap: {e.happiness}% | Hlt: {e.health}% | Smrt: {e.smarts}%"
        
        if e.job:
            self.lbl_bank.text += f" ({e.job['title']})"
        elif e.jail_years > 0:
            self.lbl_bank.text += " (IN JAIL)"

        self.log_list.clear_widgets()
        for i in range(min(20, len(e.log))):
            self.log_list.add_widget(TwoLineListItem(text=e.log[i], secondary_text=""))

    def do_age_up(self, *args):
        self.engine.age_up()
        self.update_ui()

    # --- ACTIVITY MENUS ---
    def menu_jobs(self, *args):
        if self.engine.age < 16:
            self.show_popup("Child Labor Laws", "You are too young to work.")
            return
        
        jobs = [("Janitor", 15000), ("Apprentice", 30000), ("Soldier", 40000), ("Brain Surgeon", 250000)]
        self.show_list_popup("Job Board", jobs, self.apply_job)

    def apply_job(self, title, salary):
        # Intelligence Check
        req_smarts = 0
        if title == "Brain Surgeon": req_smarts = 80
        if title == "Apprentice": req_smarts = 40
        
        if self.engine.smarts >= req_smarts:
            self.engine.job = {"title": title, "salary": salary, "years": 0}
            self.engine.add_log(f"Hired as {title}!")
            self.show_popup("Success", f"You are now a {title}.")
        else:
            self.engine.add_log(f"Rejected from {title}.")
            self.show_popup("Rejected", "They said you aren't smart enough.")
        self.update_ui()

    def menu_crime(self, *args):
        crimes = [("Shoplift", 100, 0.1), ("Rob House", 5000, 0.3), ("Bank Heist", 1000000, 0.7)]
        # Passing tuple as data, custom handler needed
        self.show_list_popup("Life of Crime", crimes, self.commit_crime)

    def commit_crime(self, name, reward, risk):
        if random.random() > risk:
            # Success
            self.engine.money += reward
            self.engine.add_log(f"SUCCESS! Committed {name}, stole ${reward}.")
            self.show_popup("Criminal Mastermind", f"You stole ${reward}!")
        else:
            # Jail
            sentence = random.randint(2, 10)
            self.engine.jail_years = sentence
            self.engine.job = None
            self.engine.criminal_record = True
            self.engine.add_log(f"ARRESTED for {name}. Sentenced to {sentence} years.")
            self.show_popup("BUSTED", f"You are going to prison for {sentence} years.")
        self.update_ui()

    def menu_casino(self, *args):
        if self.engine.money < 100:
            self.show_popup("Broke", "You need at least $100.")
            return
        
        # Simple Coin Flip Gamble
        wager = 100
        if random.random() > 0.5:
            self.engine.money += wager
            self.engine.add_log("Won $100 at Blackjack.")
        else:
            self.engine.money -= wager
            self.engine.add_log("Lost $100 at Blackjack.")
        self.update_ui()

    def menu_edu(self, *args):
        self.engine.smarts += random.randint(1, 5)
        self.engine.add_log("Studied hard at the library.")
        self.show_popup("Nerd", "Your smarts increased.")
        self.update_ui()
        
    def visit_doctor(self, *args):
        if self.engine.money < 500:
            self.show_popup("American Healthcare", "You can't afford a doctor ($500).")
            return
        self.engine.money -= 500
        self.engine.health = 100
        self.engine.add_log("Doctor cured all your ailments.")
        self.update_ui()

    def menu_shop(self, *args):
         items = [("Used Car", 5000), ("Luxury Condo", 500000), ("Supercar", 200000)]
         self.show_list_popup("Asset Dealership", items, self.buy_asset)

    def buy_asset(self, name, price):
        if self.engine.money >= price:
            self.engine.money -= price
            self.engine.assets.append(name)
            self.engine.add_log(f"Purchased {name}.")
            self.show_popup("Sweet Ride", f"You bought a {name}!")
        else:
            self.show_popup("Too Poor", "Get a better job.")
        self.update_ui()

    # --- HELPERS ---
    def show_popup(self, title, text):
        if self.dialog: self.dialog.dismiss()
        self.dialog = MDDialog(title=title, text=text, buttons=[MDFillRoundFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())])
        self.dialog.open()

    def show_list_popup(self, title, items, callback):
        if self.dialog: self.dialog.dismiss()
        content = MDBoxLayout(orientation='vertical', size_hint_y=None, height=300)
        
        # Items is list of tuples. If 3 args (Crime), handle differently
        for item in items:
            txt = item[0]
            val1 = item[1]
            # Handle variable arguments for callback
            if len(item) == 3:
                val2 = item[2]
                btn = MDRectangleFlatButton(text=f"{txt}", on_release=lambda x, a=txt, b=val1, c=val2: [callback(a,b,c), self.dialog.dismiss()])
            else:
                btn = MDRectangleFlatButton(text=f"{txt} (${val1})", on_release=lambda x, a=txt, b=val1: [callback(a,b), self.dialog.dismiss()])
            content.add_widget(btn)

        self.dialog = MDDialog(title=title, type="custom", content_cls=content)
        self.dialog.open()

class Gen3App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return GameScreen()

if __name__ == "__main__":
    Gen3App().run()
