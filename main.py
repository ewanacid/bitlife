import os, sys, traceback, random
# FORCE SOFTWARE RENDERING (Prevents OpenGL Glitches)
os.environ["KIVY_NO_ARGS"] = "1"

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.list import MDList, OneLineListItem
from kivy.uix.screenmanager import ScreenManager, Screen

# --- CRASH RECORDER ---
def log_crash(e):
    try:
        # Writes error to a file you can actually read on your phone
        path = os.path.join(os.path.expanduser("~"), "crash_log.txt")
        with open(path, "w") as f:
            f.write("CRASH REPORT:\n" + traceback.format_exc())
    except: pass

# --- GAME LOGIC ---
class LifeEngine:
    def __init__(self):
        self.age = 0
        self.money = 0
        self.health = 100
        self.alive = True
        self.job = "Unemployed"
        self.log_history = ["Born into the Bedrock System."]

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")

    def age_up(self):
        if not self.alive: return
        self.age += 1
        if self.job != "Unemployed": self.money += 45000
        
        # Events
        roll = random.random()
        if roll < 0.1:
            self.health -= 10
            self.log("You got sick.")
        elif roll < 0.2:
            self.money += 100
            self.log("Found $100.")
        
        if self.health <= 0:
            self.alive = False
            self.log("You died.")

# --- UI (The Stable Part) ---
class GameScreen(Screen):
    def on_enter(self):
        try:
            self.engine = LifeEngine()
            self.build_ui()
        except Exception as e:
            log_crash(e)

    def build_ui(self):
        self.clear_widgets()
        # Use standard BoxLayout (Rock Solid)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # 1. STATS (Simple Text, No Cards)
        self.lbl_stats = Label(
            text="AGE: 0 | BANK: $0\nJob: Unemployed | Health: 100%", 
            font_size='20sp', 
            color=(0,1,0,1), # Green Text
            size_hint=(1, 0.2),
            halign="center"
        )
        layout.add_widget(self.lbl_stats)

        # 2. SCROLLABLE LOG
        scroll = ScrollView(size_hint=(1, 0.5))
        self.log_list = MDList()
        # Initial Item
        self.log_list.add_widget(OneLineListItem(text="System Initialized."))
        scroll.add_widget(self.log_list)
        layout.add_widget(scroll)

        # 3. ACTION BUTTONS
        btns = BoxLayout(size_hint=(1, 0.1), spacing=10)
        btns.add_widget(MDRectangleFlatButton(text="GET JOB", size_hint=(0.5, 1), on_release=self.get_job))
        btns.add_widget(MDRectangleFlatButton(text="CRIME", size_hint=(0.5, 1), on_release=self.crime))
        layout.add_widget(btns)

        # 4. AGE UP
        layout.add_widget(MDFillRoundFlatButton(text="AGE UP (+1 Year)", size_hint=(1, 0.15), on_release=self.do_age))

        self.add_widget(layout)

    def update_ui(self):
        e = self.engine
        self.lbl_stats.text = f"AGE: {e.age} | BANK: ${e.money:,}\nJob: {e.job} | Health: {e.health}%"
        
        self.log_list.clear_widgets()
        for txt in e.log_history[:20]:
            self.log_list.add_widget(OneLineListItem(text=txt))

    def do_age(self, *args):
        if self.engine.alive:
            self.engine.age_up()
            self.update_ui()

    def get_job(self, *args):
        if self.engine.age >= 18:
            self.engine.job = "Developer"
            self.engine.log("Hired as Dev!")
            self.update_ui()
    
    def crime(self, *args):
        if random.random() < 0.5:
            self.engine.money += 1000
            self.engine.log("Stole $1000.")
        else:
            self.engine.log("Police chase!")
        self.update_ui()

class BedrockApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        sm = ScreenManager()
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == "__main__":
    try:
        BedrockApp().run()
    except Exception as e:
        log_crash(e)
