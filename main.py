import os, sys, random, json, traceback
# FORCE STABILITY
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
# HAPTIC FEEDBACK
from plyer import vibrator

# --- ASSET LIBRARY ---
SPRITES = {
    "Male": "👨", "Female": "👩", "Baby": "👶", "Dead": "💀",
    "Money": "💰", "Job": "💼", "School": "📚", "Love": "❤️",
    "House": "🏠", "Car": "🚗", "Jail": "🔒", "Happy": "😃",
    "Sad": "😢", "Sick": "🤢", "Smart": "🧠", "Cool": "😎",
    "Crime": "🔫", "Casino": "🎰", "Gym": "🏋️", "Doc": "⚕️"
}

JOBS = {
    "Janitor": {"sal": 18000, "req": 16, "icon": "🧹", "stress": 10},
    "Soldier": {"sal": 35000, "req": 18, "icon": "🪖", "stress": 60},
    "Teacher": {"sal": 45000, "req": 22, "icon": "🍎", "stress": 40},
    "Engineer": {"sal": 85000, "req": 22, "icon": "📐", "stress": 50},
    "Doctor": {"sal": 180000, "req": 26, "icon": "🩺", "stress": 80},
    "CEO": {"sal": 1000000, "req": 35, "icon": "🏢", "stress": 90}
}

ASSETS = [
    ("Used Sedan", 5000, "Car"), ("Sports Car", 50000, "Car"), ("Supercar", 250000, "Car"),
    ("Trailer", 20000, "House"), ("Condo", 150000, "House"), ("Mansion", 2500000, "House")
]

# --- DEEP SIMULATION ENGINE ---
class SimEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.name = f"{random.choice(['Liam','Noah','Oliver','James','Emma','Ava'])} {random.choice(['Smith','Jones','Brown','Garcia'])}"
        self.gender = random.choice(["Male", "Female"])
        self.face = SPRITES[self.gender]
        self.age = 0
        self.money = 0
        self.career = "Unemployed"
        self.education = "None"
        
        # CORE STATS
        self.hap = 90
        self.hlt = 100
        self.smrt = random.randint(20, 90)
        self.look = random.randint(20, 90)
        
        self.alive = True
        self.jail = 0
        self.assets = []
        self.relations = [{"name": "Mom", "rel": 100}, {"name": "Dad", "rel": 100}]
        self.log_history = [f"{SPRITES['Baby']} Born a {self.gender} in the Year 3000."]
        self.scenario = None

    def log(self, text, icon=""):
        self.log_history.insert(0, f"Age {self.age}: {icon} {text}")

    def age_up(self):
        if not self.alive: return
        self.age += 1
        
        # 1. JAIL LOGIC
        if self.jail > 0:
            self.jail -= 1
            self.hap -= 10
            self.log(f"Serving time ({self.jail} yrs left).", SPRITES['Jail'])
            if self.jail == 0: self.log("Released from prison!", "🔓")
            return

        # 2. EDUCATION & CAREER
        if self.age < 18:
            self.education = "High School"
            self.smrt += random.randint(0, 3)
        elif self.career != "Unemployed":
            sal = JOBS.get(self.career, {'sal':0})['sal']
            tax_rate = 0.3 if sal > 100000 else 0.15
            net = int(sal * (1 - tax_rate))
            self.money += net
            if random.random() < 0.1: self.log("Got a raise!", SPRITES['Money'])
        
        # 3. ASSET SIMULATION
        for a in self.assets:
            if a['type'] == 'House': a['val'] = int(a['val']*1.04) # 4% Appreciation
            if a['type'] == 'Car': a['val'] = int(a['val']*0.88)   # 12% Depreciation

        # 4. RANDOM EVENTS
        self.run_random_events()

        # 5. DEATH CHECK
        death_chance = 0.0
        if self.age > 80: death_chance = 0.1 + ((self.age - 80) * 0.02)
        if self.hlt <= 0 or random.random() < death_chance:
            self.alive = False
            self.face = SPRITES['Dead']
            self.log(f"Died. Net Worth: ${self.get_net_worth():,}", SPRITES['Dead'])
            self.buzz(1.0) # Long vibration on death

    def run_random_events(self):
        roll = random.random()
        if roll < 0.05:
            self.hlt -= 10; self.log("Contracted a virus.", SPRITES['Sick'])
            self.buzz(0.2)
        elif roll < 0.10:
            self.hap -= 15; self.log("Feeling depressed.", SPRITES['Sad'])
        elif roll < 0.15:
            prize = random.randint(100, 1000)
            self.money += prize; self.log(f"Found ${prize}.", SPRITES['Money'])
            self.buzz(0.05)
        elif roll < 0.20:
            self.scenario = "wallet" # Trigger Popup

    def get_net_worth(self):
        return self.money + sum(a['val'] for a in self.assets)
    
    def buzz(self, duration):
        try: vibrator.vibrate(duration)
        except: pass

# --- UI COMPONENTS ---
class StatBar(MDBoxLayout):
    def __init__(self, label, value, color, **kwargs):
        super().__init__(orientation='vertical', size_hint_x=0.25, **kwargs)
        self.lbl = MDLabel(text=f"{label}: {value}%", halign="center", font_style="Caption", theme_text_color="Custom", text_color=color)
        self.add_widget(self.lbl)
        self.bar = MDProgressBar(value=value, color=color, size_hint_y=None, height="6dp")
        self.add_widget(self.bar)
    def update(self, val):
        self.lbl.text = f"{self.lbl.text.split(':')[0]}: {val}%"
        self.bar.value = val

# --- MAIN SCREEN ---
class GameScreen(Screen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(orientation='vertical', padding=10, spacing=5)

        # IDENTITY HEADER
        head = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        self.lbl_face = MDLabel(text=self.engine.face, font_style="H2", size_hint_x=0.2, halign="center")
        info = MDBoxLayout(orientation='vertical')
        self.lbl_name = MDLabel(text="Name", font_style="H6", bold=True)
        self.lbl_job = MDLabel(text="Job", theme_text_color="Secondary")
        self.lbl_bank = MDLabel(text="$$$", theme_text_color="Custom", text_color=(0,1,0,1))
        info.add_widget(self.lbl_name); info.add_widget(self.lbl_job); info.add_widget(self.lbl_bank)
        head.add_widget(self.lbl_face); head.add_widget(info)
        root.add_widget(head)

        # SCROLLABLE LOG
        scroll = MDScrollView(size_hint=(1, 0.45))
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        root.add_widget(scroll)

        # AGE BUTTON
        age_box = MDBoxLayout(padding=[30, 5], size_hint=(1, 0.12))
        btn = MDFillRoundFlatButton(text="AGE UP +", font_size=26, size_hint=(1, 1), md_bg_color=(0, 0.7, 0, 1), on_release=self.do_age)
        age_box.add_widget(btn)
        root.add_widget(age_box)

        # STAT BARS
        stats = MDBoxLayout(size_hint=(1, 0.1), spacing=5)
        self.s_hap = StatBar("Hap", 100, (0,1,0,1))
        self.s_hlt = StatBar("Hlt", 100, (1,0,0,1))
        self.s_smr = StatBar("Smrt", 100, (0,0,1,1))
        self.s_lok = StatBar("Look", 100, (1,0.5,0,1))
        stats.add_widget(self.s_hap); stats.add_widget(self.s_hlt)
        stats.add_widget(self.s_smr); stats.add_widget(self.s_lok)
        root.add_widget(stats)

        # MENU TABS
        nav = MDBoxLayout(size_hint=(1, 0.1), spacing=2)
        nav.add_widget(MDRectangleFlatButton(text="JOB", size_hint=(0.25, 1), on_release=lambda x: self.menu("job")))
        nav.add_widget(MDRectangleFlatButton(text="ASSET", size_hint=(0.25, 1), on_release=lambda x: self.menu("asset")))
        nav.add_widget(MDRectangleFlatButton(text="RELATION", size_hint=(0.25, 1), on_release=lambda x: self.menu("rel")))
        nav.add_widget(MDRectangleFlatButton(text="ACT", size_hint=(0.25, 1), on_release=lambda x: self.menu("act")))
        root.add_widget(nav)

        self.add_widget(root)
        self.update()

    def update(self):
        e = self.engine
        self.lbl_face.text = e.face
        self.lbl_name.text = f"{e.name} ({e.age})"
        self.lbl_job.text = f"{e.career} | {e.education}"
        self.lbl_bank.text = f"Bank: ${e.money:,} | Net: ${e.get_net_worth():,}"
        
        self.s_hap.update(e.hap); self.s_hlt.update(e.hlt)
        self.s_smr.update(e.smrt); self.s_lok.update(e.look)
        
        self.log_list.clear_widgets()
        for txt in e.log_history[:50]: self.log_list.add_widget(OneLineListItem(text=txt))

        # NEURAL THEME ENGINE
        if e.hlt < 40: self.app.theme_cls.primary_palette = "Red"     # Danger
        elif e.money > 1000000: self.app.theme_cls.primary_palette = "Amber" # Rich
        elif e.jail > 0: self.app.theme_cls.primary_palette = "BlueGray"     # Jail
        else: self.app.theme_cls.primary_palette = "DeepPurple"       # Normal

    def do_age(self, *x):
        self.engine.buzz(0.05) # Haptic Click
        self.engine.age_up()
        self.update()
        if self.engine.scenario == "wallet":
            self.show_popup("Found Wallet", "You found a wallet with $500.", [("Keep", self.scen_keep), ("Return", self.scen_ret)])
            self.engine.scenario = None

    def show_popup(self, title, text, opts):
        btns = [MDRectangleFlatButton(text=o[0], on_release=lambda x, f=o[1]: self.run_scen(f)) for o in opts]
        self.dialog = MDDialog(title=title, text=text, buttons=btns)
        self.dialog.open()

    def run_scen(self, func):
        self.dialog.dismiss()
        func()
        self.update()

    def scen_keep(self): self.engine.money+=500; self.engine.hap+=10; self.engine.log("Kept wallet.", SPRITES['Money'])
    def scen_ret(self): self.engine.hap+=20; self.engine.log("Returned wallet.", SPRITES['Happy'])
    def menu(self, m): self.manager.current = m

# --- GENERIC MENU SCREEN ---
class MenuScreen(Screen):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self.build_ui()
    def back(self, *x): self.manager.current = 'game'
    
    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=15)
        layout.add_widget(MDLabel(text=self.name.upper(), font_style="H5", halign="center", size_hint=(1, 0.1)))
        scroll = MDScrollView()
        lst = MDList()
        
        # DYNAMIC CONTENT BUILDER
        if self.name == "job":
            if self.engine.age < 16: lst.add_widget(OneLineListItem(text="Child Labor Laws Active."))
            else:
                for t, d in JOBS.items():
                    lst.add_widget(TwoLineListItem(text=f"{d['icon']} {t}", secondary_text=f"${d['sal']:,}/yr (Req Age: {d['req']})", on_release=lambda x,t=t:self.get_job(t)))
        
        elif self.name == "asset":
            if self.engine.age < 18: lst.add_widget(OneLineListItem(text="Must be 18+."))
            else:
                for n, p, t in ASSETS:
                    lst.add_widget(TwoLineListItem(text=f"{SPRITES[t]} {n}", secondary_text=f"${p:,}", on_release=lambda x,n=n,p=p,t=t:self.buy(n,p,t)))
        
        elif self.name == "act":
            opts = [("🏥 Doctor ($100)", self.doc), ("🏋️ Gym ($50)", self.gym), ("🎰 Casino", self.casino), ("🔫 Crime", self.crime), ("❤️ Dating App", self.date)]
            for t, f in opts: lst.add_widget(OneLineListItem(text=t, on_release=f))
            
        elif self.name == "rel":
            for r in self.engine.relations: lst.add_widget(TwoLineListItem(text=r['name'], secondary_text=f"Relationship: {r['rel']}%"))

        scroll.add_widget(lst); layout.add_widget(scroll)
        layout.add_widget(MDFillRoundFlatButton(text="BACK", size_hint=(1, 0.1), on_release=self.back))
        self.add_widget(layout)

    # ACTIONS
    def get_job(self, t):
        if self.engine.age >= JOBS[t]['req']: self.engine.career = t; self.engine.log(f"HIRED as {t}!", JOBS[t]['icon'])
        else: self.engine.log(f"Rejected from {t} (Age req).", SPRITES['Sad'])
        self.back()

    def buy(self, n, p, t):
        if self.engine.money >= p: 
            self.engine.money -= p; self.engine.assets.append({"name": n, "val": p, "type": t})
            self.engine.log(f"Bought {n}!", SPRITES[t])
        else: self.engine.log("Insufficient funds.", SPRITES['Sad'])
        self.back()

    def doc(self, *x): 
        if self.engine.money>=100: self.engine.money-=100; self.engine.hlt=100; self.engine.log("Cured!", SPRITES['Doc']); self.back()
    
    def gym(self, *x):
        if self.engine.money>=50: self.engine.money-=50; self.engine.hlt+=5; self.engine.log("Worked out.", SPRITES['Gym']); self.back()
    
    def crime(self, *x):
        if random.random()>0.5: 
            self.engine.money+=1000; self.engine.log("Stole loot!", SPRITES['Money'])
            self.engine.buzz(0.1)
        else: 
            self.engine.jail=3; self.engine.log("ARRESTED! (3 yrs)", SPRITES['Jail'])
            self.engine.buzz(0.5)
        self.back()
    
    def casino(self, *x):
        if self.engine.money>=100:
            self.engine.money-=100
            if random.random()>0.5: self.engine.money+=200; self.engine.log("Won Blackjack!", SPRITES['Casino'])
            else: self.engine.log("Lost $100.", "💸")
        self.back()
    
    def date(self, *x):
        n = random.choice(["Ashley","Jessica","Mike","Chris"]); self.engine.relations.append({"name": n, "rel": 50}); self.engine.log(f"Started dating {n}!", SPRITES['Love']); self.back()

# --- APP BOOTSTRAP ---
class Year3000App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.engine = SimEngine()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(GameScreen(name='game'))
        for m in ['job', 'asset', 'act', 'rel']: sm.add_widget(MenuScreen(name=m))
        return sm

if __name__ == "__main__":
    try: Year3000App().run()
    except Exception as e:
        with open("crash.txt", "w") as f: f.write(traceback.format_exc())
