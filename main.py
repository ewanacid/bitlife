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
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, DictProperty, ListProperty
from kivy.clock import Clock
# HAPTIC FEEDBACK
from plyer import vibrator

# --- ASSET LIBRARY ---
SPRITES = {
    "Male": "👨", "Female": "👩", "Baby": "👶", "Dead": "💀",
    "Money": "💰", "Job": "💼", "School": "📚", "Love": "❤️",
    "House": "🏠", "Car": "🚗", "Jail": "🔒", "Happy": "😃",
    "Sad": "😢", "Sick": "🤢", "Smart": "🧠", "Cool": "😎",
    "Crime": "🔫", "Casino": "🎰", "Gym": "🏋️", "Doc": "⚕️",
    "Karma": "⚖️", "Stress": "🤯", "Energy": "⚡", "Fame": "🌟",
    "Study": "📖", "Meditate": "🧘", "Volunteer": "🫶", "Travel": "✈️",
    "Degree": "🎓", "Promotion": "⬆️", "Demotion": "⬇️", "Layoff": "❌",
    "Marriage": "💍", "Child": "👶", "Pet": "🐾", "Skill": "💡",
    "Bank": "🏦", "Stocks": "📈", "Crypto": "₿", "Business": "🏭"
}

JOBS = {
    "Janitor": {"sal": 18000, "req_age": 16, "req_smrt": 10, "req_skills": {}, "icon": "🧹", "stress": 10, "promo_chance": 0.05, "layoff_chance": 0.02},
    "Soldier": {"sal": 35000, "req_age": 18, "req_smrt": 20, "req_skills": {}, "icon": "🪖", "stress": 60, "promo_chance": 0.08, "layoff_chance": 0.05},
    "Teacher": {"sal": 45000, "req_age": 22, "req_smrt": 50, "req_skills": {"Teaching":1}, "icon": "🍎", "stress": 40, "promo_chance": 0.10, "layoff_chance": 0.03},
    "Engineer": {"sal": 85000, "req_age": 22, "req_smrt": 70, "req_skills": {"Coding":2}, "icon": "📐", "stress": 50, "promo_chance": 0.12, "layoff_chance": 0.04},
    "Doctor": {"sal": 180000, "req_age": 26, "req_smrt": 85, "req_skills": {"Medicine":3}, "icon": "🩺", "stress": 80, "promo_chance": 0.15, "layoff_chance": 0.02},
    "CEO": {"sal": 1000000, "req_age": 35, "req_smrt": 95, "req_skills": {"Leadership":5}, "icon": "🏢", "stress": 90, "promo_chance": 0.01, "layoff_chance": 0.10}
}

ASSETS = [
    ("Used Sedan", 5000, "Car", {"upkeep": 500, "depreciation": 0.12}),
    ("Sports Car", 50000, "Car", {"upkeep": 2000, "depreciation": 0.15}),
    ("Supercar", 250000, "Car", {"upkeep": 5000, "depreciation": 0.20}),
    ("Trailer", 20000, "House", {"upkeep": 200, "appreciation": 0.02}),
    ("Condo", 150000, "House", {"upkeep": 1000, "appreciation": 0.04}),
    ("Mansion", 2500000, "House", {"upkeep": 10000, "appreciation": 0.06}),
    ("Index Fund", 1000, "Stocks", {"upkeep": 0, "appreciation": 0.08, "volatility": 0.1}),
    ("Startup Equity", 10000, "Stocks", {"upkeep": 0, "appreciation": 0.20, "volatility": 0.5}),
    ("Crypto Portfolio", 5000, "Crypto", {"upkeep": 0, "appreciation": 0.15, "volatility": 0.8})
]

EDUCATION_PROGRAMS = {
    "High School": {"cost": 0, "smrt_gain": 5, "min_age": 14, "duration": 4},
    "University (Bachelors)": {"cost": 50000, "smrt_gain": 20, "min_age": 18, "duration": 4, "degree": "Bachelors"},
    "Medical School (MD)": {"cost": 200000, "smrt_gain": 30, "min_age": 22, "duration": 4, "degree": "Doctorate", "req_smrt": 80},
    "Law School (JD)": {"cost": 150000, "smrt_gain": 25, "min_age": 22, "duration": 3, "degree": "Doctorate", "req_smrt": 75}
}

SKILLS_LEARN = {
    "Coding": {"cost": 1000, "smrt_req": 20, "effect": {"smrt": 2, "skill_level": 1}},
    "Teaching": {"cost": 500, "smrt_req": 15, "effect": {"hap": 5, "skill_level": 1}},
    "Medicine": {"cost": 5000, "smrt_req": 70, "effect": {"hlt": 2, "skill_level": 1}},
    "Leadership": {"cost": 2000, "smrt_req": 50, "effect": {"fame": 5, "skill_level": 1}},
    "Art": {"cost": 300, "smrt_req": 10, "effect": {"hap": 3, "skill_level": 1}},
    "Music": {"cost": 300, "smrt_req": 10, "effect": {"hap": 3, "skill_level": 1}},
}


# --- DEEP SIMULATION ENGINE ---
class SimEngine:
    def __init__(self):
        self.reset()
        self.dialog_queue = []

    def reset(self):
        self.name = f"{random.choice(['Liam','Noah','Oliver','James','Emma','Ava'])} {random.choice(['Smith','Jones','Brown','Garcia'])}"
        self.gender = random.choice(["Male", "Female"])
        self.face = SPRITES[self.gender]
        self.age = 0
        self.money = 0
        self.career = "Unemployed"
        self.education = "None"
        self.current_education = None # Stores current ongoing education program
        self.education_years_left = 0
        
        # CORE STATS
        self.hap = 90 # Happiness
        self.hlt = 100 # Health
        self.smrt = random.randint(20, 90) # Smartness
        self.look = random.randint(20, 90) # Looks
        self.karma = 0 # Karma (-100 to 100)
        self.stress = 20 # Stress (0 to 100, impacts hap/hlt)
        self.energy = 100 # Energy (0 to 100, impacts actions)
        self.fame = 0 # Fame (-100 to 100)
        
        self.alive = True
        self.jail = 0
        self.assets = [] # List of {"name": "Car", "val": 5000, "type": "Car", "props": {...}}
        self.relations = [{"name": "Mom", "rel": 100, "type": "Family"}, {"name": "Dad", "rel": 100, "type": "Family"}]
        self.married_to = None
        self.children = []
        self.skills = {} # {"Coding": 1, "Teaching": 0}
        
        self.log_history = [f"{SPRITES['Baby']} Born a {self.gender} in the Year 3000."]
        self.scenario = None
        self.game_over_reason = None

    def log(self, text, icon=""):
        self.log_history.insert(0, f"Age {self.age}: {icon} {text}")
        
    def buzz(self, duration=0.05):
        try: vibrator.vibrate(duration)
        except: pass

    def adjust_stat(self, stat_name, amount, min_val=0, max_val=100, allow_below_min=False):
        current_val = getattr(self, stat_name)
        new_val = current_val + amount
        
        if not allow_below_min and new_val < min_val: new_val = min_val
        if new_val > max_val: new_val = max_val
        
        setattr(self, stat_name, new_val)
        return new_val

    def age_up(self):
        if not self.alive: return
        
        self.age += 1
        self.buzz(0.03) # Subtle haptic feedback for aging

        # 1. JAIL LOGIC
        if self.jail > 0:
            self.jail -= 1
            self.adjust_stat("hap", -15)
            self.adjust_stat("stress", 20)
            self.log(f"Serving time ({self.jail} yrs left).", SPRITES['Jail'])
            if self.jail == 0: self.log("Released from prison!", "🔓"); self.adjust_stat("stress", -30)
            self.check_death() # Can die in jail
            return

        # 2. EDUCATION PROGRESS
        if self.current_education:
            self.education_years_left -= 1
            self.adjust_stat("smrt", self.current_education['smrt_gain'] / self.current_education['duration'])
            self.adjust_stat("stress", 10)
            self.adjust_stat("money", -self.current_education['cost'] / self.current_education['duration'])
            self.log(f"Studying for {self.current_education['degree']} ({self.education_years_left} yrs left).", SPRITES['Study'])
            if self.education_years_left <= 0:
                self.education = self.current_education['degree']
                self.log(f"Graduated with a {self.education}!", SPRITES['Degree'])
                self.current_education = None
                self.adjust_stat("smrt", 10) # Bonus for completion
                self.adjust_stat("stress", -20)
        
        # 3. CAREER PROGRESS & INCOME
        if self.career != "Unemployed" and not self.current_education: # Can't work full-time while studying
            job_data = JOBS.get(self.career)
            if job_data:
                sal_factor = 1 + (self.skills.get("Leadership", 0) * 0.05) + (self.smrt / 200) # Skills & Smrt boost salary
                base_sal = job_data['sal'] * sal_factor
                tax_rate = 0.3 if base_sal > 100000 else 0.15
                net = int(base_sal * (1 - tax_rate))
                self.money += net
                self.adjust_stat("stress", job_data['stress'] / 10)
                
                self.log(f"Earned ${net:,} from {self.career}.", SPRITES['Money'])

                # Promotion/Layoff Chance
                if random.random() < job_data['promo_chance']:
                    self.log(f"Got a promotion at {self.career}!", SPRITES['Promotion'])
                    self.adjust_stat("money", 5000); self.adjust_stat("hap", 10); self.adjust_stat("fame", 5); self.adjust_stat("stress", -10)
                elif random.random() < job_data['layoff_chance']:
                    self.log(f"Laid off from {self.career}!", SPRITES['Layoff'])
                    self.career = "Unemployed"; self.adjust_stat("hap", -20); self.adjust_stat("stress", 30); self.adjust_stat("fame", -5)
        
        # 4. ASSET SIMULATION & UPKEEP
        assets_to_remove = []
        for i, asset in enumerate(self.assets):
            props = asset['props']
            if asset['type'] == 'House':
                asset['val'] = int(asset['val'] * (1 + props.get('appreciation', 0.0)))
                self.money -= props.get('upkeep', 0)
                if props.get('upkeep', 0) > 0: self.log(f"Paid ${props['upkeep']:,} upkeep for {asset['name']}.", SPRITES['Money'])
            elif asset['type'] == 'Car':
                asset['val'] = int(asset['val'] * (1 - props.get('depreciation', 0.0)))
                self.money -= props.get('upkeep', 0)
                if props.get('upkeep', 0) > 0: self.log(f"Paid ${props['upkeep']:,} for {asset['name']} maintenance.", SPRITES['Money'])
                if asset['val'] < 1000 and random.random() < 0.2: # Old car breaks down
                    self.log(f"{asset['name']} broke down and sold for scrap.", SPRITES['Sad'])
                    self.money += 200 # Scrap value
                    assets_to_remove.append(i)
            elif asset['type'] in ['Stocks', 'Crypto']:
                change = (random.random() * 2 - 1) * props.get('volatility', 0) * asset['val']
                asset['val'] += int(change)
                asset['val'] = max(1, asset['val']) # Cannot go below 1
                if change > 0: self.log(f"{asset['name']} gained ${int(change):,}.", SPRITES['Stocks'])
                else: self.log(f"{asset['name']} lost ${int(abs(change)):,}.", "📉")

        for i in reversed(assets_to_remove):
            self.assets.pop(i)

        # 5. CORE STAT DECAY / REGENERATION
        self.adjust_stat("energy", -random.randint(5, 15), allow_below_min=True)
        self.adjust_stat("energy", 30) # Sleep
        self.adjust_stat("stress", -random.randint(5, 10)) # Passive stress relief
        
        if self.stress > 70: self.adjust_stat("hap", -10); self.adjust_stat("hlt", -5); self.log("High stress impacting health & mood.", SPRITES['Stress'])
        if self.energy < 20: self.adjust_stat("hap", -5); self.adjust_stat("hlt", -5); self.log("Low energy makes you feel sluggish.", SPRITES['Energy'])
        if self.hap < 30: self.adjust_stat("stress", 10); self.log("Unhappiness causing more stress.", SPRITES['Sad'])

        # 6. RELATIONSHIPS & FAMILY
        for r in self.relations:
            if r['type'] == 'Family' or r['type'] == 'Spouse':
                self.adjust_stat("hap", r['rel'] / 200) # Passive happiness from good relations
                if random.random() < 0.02: # Small chance of relationship decay
                    r['rel'] = max(0, r['rel'] - 5)
                    self.log(f"Relationship with {r['name']} declined slightly.", SPRITES['Sad'])
        
        # Children age up
        for child in self.children:
            child['age'] += 1
            if child['age'] % 5 == 0: self.log(f"Your child {child['name']} is now {child['age']}!", SPRITES['Child'])

        # 7. RANDOM EVENTS
        self.run_random_events()

        # 8. DEATH CHECK
        self.check_death()

    def check_death(self):
        if not self.alive: return

        death_chance = 0.0
        death_reason = ""

        # Age-related death
        if self.age > 80:
            death_chance += (self.age - 80) * 0.03
            death_reason = "old age"
        
        # Health-related death
        if self.hlt <= 0:
            death_chance += 1.0 # Guaranteed death
            death_reason = "poor health"
        elif self.hlt < 20:
            death_chance += 0.1
            death_reason = "critical health"
        
        # Stress-related death (e.g., heart attack)
        if self.stress >= 95 and random.random() < 0.1:
            death_chance += 0.5
            death_reason = "stress-induced complications"

        # Jail death
        if self.jail > 0 and random.random() < 0.08: # Higher chance to die in jail
            death_chance += 0.3
            death_reason = "prison incident"
            
        # Random unexpected death (always a small chance)
        if random.random() < 0.005:
            death_chance += 0.2
            death_reason = random.choice(["freak accident", "sudden illness"])

        if random.random() < death_chance:
            self.alive = False
            self.face = SPRITES['Dead']
            self.game_over_reason = death_reason
            self.log(f"Died from {death_reason}. Net Worth: ${self.get_net_worth():,}", SPRITES['Dead'])
            self.buzz(1.0) # Long vibration on death
            self.dialog_queue.append(("Game Over!", f"You died at age {self.age} from {death_reason}. Your final net worth was ${self.get_net_worth():,}.", [("New Game", self.reset_game)]))


    def run_random_events(self):
        roll = random.random()
        if roll < 0.05 and self.hlt > 20: # Sickness
            self.adjust_stat("hlt", -random.randint(10, 25))
            self.log("Contracted a virus. Feeling unwell.", SPRITES['Sick'])
            self.buzz(0.2)
        elif roll < 0.10 and self.hap > 20: # Depression
            self.adjust_stat("hap", -random.randint(10, 20))
            self.adjust_stat("stress", 15)
            self.log("Feeling depressed and demotivated.", SPRITES['Sad'])
        elif roll < 0.15: # Found money
            prize = random.randint(100, 1000)
            self.money += prize
            self.log(f"Found ${prize} on the street.", SPRITES['Money'])
            self.buzz(0.05)
        elif roll < 0.18: # Lost money
            if self.money > 200:
                lost = random.randint(50, 200)
                self.money -= lost
                self.log(f"Lost ${lost} from a scam.", "💸")
                self.adjust_stat("hap", -5)
            else: self.log("Luckily, you had no money to lose to a scam.", "😅")
        elif roll < 0.22 and self.age >= 18: # Wallet scenario
            self.scenario = "wallet" # Trigger Popup
        elif roll < 0.25 and self.career == "Unemployed" and self.age >= 18: # Temp Job Offer
            self.log("Got a temporary job offer, but it pays low. (+500)", SPRITES['Job'])
            self.money += 500
            self.adjust_stat("hap", 5)
        elif roll < 0.28 and self.married_to: # Spouse gift
            gift_val = random.randint(100, 1000)
            self.money += gift_val
            self.adjust_stat("hap", 5)
            self.log(f"Your spouse {self.married_to} bought you a gift worth ${gift_val}.", SPRITES['Love'])
        elif roll < 0.30 and self.age > 60 and self.hlt < 80: # Health scare
            self.log("Experienced a minor health scare. Should see a doctor soon.", SPRITES['Doc'])
            self.adjust_stat("stress", 10)

    def get_net_worth(self):
        return self.money + sum(a['val'] for a in self.assets)
    
    def get_skill_level(self, skill_name):
        return self.skills.get(skill_name, 0)

    def reset_game(self):
        MDApp.get_running_app().engine.reset()
        MDApp.get_running_app().root.get_screen('game').build_ui() # Rebuild UI for new game state
        MDApp.get_running_app().root.get_screen('game').update()
        MDApp.get_running_app().root.current = 'game' # Ensure we are on game screen


# --- UI COMPONENTS ---
class StatBar(MDBoxLayout):
    lbl_text = StringProperty("")
    bar_value = NumericProperty(0)
    bar_color = ListProperty([0, 0, 0, 1])

    def __init__(self, label, value, color, **kwargs):
        super().__init__(orientation='vertical', size_hint_x=0.25, **kwargs)
        self.lbl_text = f"{label}: {value}%"
        self.bar_value = value
        self.bar_color = color
        
        self.lbl = MDLabel(text=self.lbl_text, halign="center", font_style="Caption", theme_text_color="Custom", text_color=color)
        self.add_widget(self.lbl)
        self.bar = MDProgressBar(value=self.bar_value, color=self.bar_color, size_hint_y=None, height="6dp")
        self.add_widget(self.bar)

    def update(self, val):
        if val > 100: val = 100
        if val < 0 and self.lbl.text.split(':')[0] not in ["Karma", "Fame"]: val = 0 # Karma/Fame can be negative

        self.lbl.text = f"{self.lbl.text.split(':')[0]}: {val}%"
        self.bar.value = val

# --- MAIN SCREEN ---
class GameScreen(Screen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self._current_dialog = None # Initialize dialog state for safer checking
        self.build_ui()
        Clock.schedule_interval(self.check_dialog_queue, 0.5)

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(orientation='vertical', padding=[10, 5], spacing=5)

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
        self.age_button = MDFillRoundFlatButton(text="AGE UP +", font_size=26, size_hint=(1, 1), md_bg_color=(0, 0.7, 0, 1), on_release=self.do_age)
        age_box.add_widget(self.age_button)
        root.add_widget(age_box)

        # STAT BARS (2 rows for more stats)
        stats_row1 = MDBoxLayout(size_hint=(1, 0.08), spacing=5)
        self.s_hap = StatBar("Hap", 100, (0,1,0,1))
        self.s_hlt = StatBar("Hlt", 100, (1,0,0,1))
        self.s_smrt = StatBar("Smrt", 100, (0,0,1,1))
        self.s_lok = StatBar("Look", 100, (1,0.5,0,1))
        stats_row1.add_widget(self.s_hap); stats_row1.add_widget(self.s_hlt)
        stats_row1.add_widget(self.s_smrt); stats_row1.add_widget(self.s_lok)
        root.add_widget(stats_row1)
        
        stats_row2 = MDBoxLayout(size_hint=(1, 0.08), spacing=5)
        self.s_karma = StatBar("Karma", 0, (0.5, 0, 0.5, 1)) # Purple
        self.s_stress = StatBar("Stress", 20, (0.8, 0.4, 0, 1)) # Orange
        self.s_energy = StatBar("Energy", 100, (0, 0.8, 0.8, 1)) # Cyan
        self.s_fame = StatBar("Fame", 0, (1, 0.8, 0, 1)) # Gold
        stats_row2.add_widget(self.s_karma); stats_row2.add_widget(self.s_stress)
        stats_row2.add_widget(self.s_energy); stats_row2.add_widget(self.s_fame)
        root.add_widget(stats_row2)

        # MENU TABS
        nav = MDBoxLayout(size_hint=(1, 0.08), spacing=2)
        nav.add_widget(MDRectangleFlatButton(text="JOB", size_hint=(0.25, 1), on_release=lambda x: self.menu("job")))
        nav.add_widget(MDRectangleFlatButton(text="ASSET", size_hint=(0.25, 1), on_release=lambda x: self.menu("asset")))
        nav.add_widget(MDRectangleFlatButton(text="RELATION", size_hint=(0.25, 1), on_release=lambda x: self.menu("rel")))
        nav.add_widget(MDRectangleFlatButton(text="ACT", size_hint=(0.25, 1), on_release=lambda x: self.menu("act")))
        root.add_widget(nav)

        self.add_widget(root)
        self.update()

    def update(self, *args):
        e = self.engine
        
        # Disable age button if dead
        self.age_button.disabled = not e.alive
        if not e.alive:
            self.age_button.text = "GAME OVER!"
            self.age_button.md_bg_color = (0.5, 0, 0, 1)

        self.lbl_face.text = e.face
        self.lbl_name.text = f"{e.name} ({e.age}) {e.gender}"
        job_display = e.career
        if e.current_education:
            job_display += f" ({e.current_education['degree']} student)"
        self.lbl_job.text = f"{job_display} | {e.education}"
        self.lbl_bank.text = f"Bank: ${e.money:,} | Net: ${e.get_net_worth():,}"
        
        self.s_hap.update(e.hap); self.s_hlt.update(e.hlt)
        self.s_smrt.update(e.smrt); self.s_lok.update(e.look)
        self.s_karma.update(e.karma); self.s_stress.update(e.stress)
        self.s_energy.update(e.energy); self.s_fame.update(e.fame)
        
        self.log_list.clear_widgets()
        for txt in e.log_history[:50]: self.log_list.add_widget(OneLineListItem(text=txt))

        # NEURAL THEME ENGINE - More complex states
        if e.hlt < 30 or e.stress > 80: self.app.theme_cls.primary_palette = "Red"     # Critical Health/Stress
        elif e.jail > 0: self.app.theme_cls.primary_palette = "BlueGray"     # Jail
        elif e.hap < 30: self.app.theme_cls.primary_palette = "Grey" # Unhappy
        elif e.money > 5000000: self.app.theme_cls.primary_palette = "Amber" # Very Rich
        elif e.fame > 50: self.app.theme_cls.primary_palette = "Yellow" # Famous
        else: self.app.theme_cls.primary_palette = "DeepPurple"       # Normal

        # Process dialog queue
        if e.dialog_queue and (self._current_dialog is None or not self._current_dialog.is_open):
            title, text, opts = e.dialog_queue.pop(0)
            self.show_popup(title, text, opts)

    def check_dialog_queue(self, dt):
        self.update() # Update to ensure latest game state is reflected

    def do_age(self, *x):
        self.engine.age_up()
        self.update()
        if self.engine.scenario == "wallet":
            self.show_popup("Found Wallet", "You found a wallet with $500. What do you do?", [("Keep (Karma-)", self.scen_keep), ("Return (Karma+)", self.scen_ret)])
            self.engine.scenario = None
        elif self.engine.game_over_reason and (self._current_dialog is None or not self._current_dialog.is_open):
            # Game Over dialog should be handled by engine.dialog_queue now
            pass
        
    def show_popup(self, title, text, opts):
        btns = []
        for o_text, o_func in opts:
            btn = MDRectangleFlatButton(text=o_text, on_release=lambda x, f=o_func: self.run_scen(f))
            btns.append(btn)
        
        self._current_dialog = MDDialog(title=title, text=text, buttons=btns, auto_dismiss=False)
        self._current_dialog.open()

    def run_scen(self, func):
        if self._current_dialog: # Ensure dialog exists before dismissing
            self._current_dialog.dismiss()
            self._current_dialog = None # Clear reference safely
        func()
        self.update() # Refresh after choice

    def scen_keep(self): 
        self.engine.money+=500; self.engine.adjust_stat("hap", 10); self.engine.adjust_stat("karma", -10, min_val=-100); 
        self.engine.log("Kept wallet (Karma -10).", SPRITES['Money'])
    def scen_ret(self): 
        self.engine.adjust_stat("hap", 20); self.engine.adjust_stat("karma", 10, max_val=100); 
        self.engine.log("Returned wallet (Karma +10).", SPRITES['Happy'])
    
    def menu(self, m): 
        self.manager.current = m

# --- GENERIC MENU SCREEN ---
class MenuScreen(Screen):
    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self.dialog = None # Initialize dialog state for MenuScreen as well

    def on_enter(self):
        self.engine = self.app.engine # Ensure engine is updated on screen entry
        self.build_ui()
    
    def back(self, *x): 
        self.manager.current = 'game'

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=15, spacing=10)
        layout.add_widget(MDLabel(text=self.name.upper(), font_style="H5", halign="center", size_hint_y=0.1))
        
        scroll = MDScrollView()
        lst = MDList()
        
        # DYNAMIC CONTENT BUILDER
        if self.name == "job":
            if self.engine.age < 16: lst.add_widget(OneLineListItem(text="Child Labor Laws Active."))
            elif self.engine.current_education: lst.add_widget(OneLineListItem(text="Cannot take a job while studying full-time."))
            else:
                if self.engine.career != "Unemployed":
                    lst.add_widget(OneLineListItem(text=f"Current: {self.engine.career}", disabled=True))
                    lst.add_widget(MDFillRoundFlatButton(text="QUIT JOB", on_release=self.quit_job, size_hint_y=None, height="48dp", md_bg_color=(0.8,0,0,1)))
                    lst.add_widget(OneLineListItem(text="--- Available Jobs ---", disabled=True))

                for t, d in JOBS.items():
                    can_apply = self.engine.age >= d['req_age'] and self.engine.smrt >= d['req_smrt']
                    for skill, level in d['req_skills'].items():
                        if self.engine.get_skill_level(skill) < level: can_apply = False
                    
                    sec_text = f"Salary: ${d['sal']:,}/yr | Age: {d['req_age']} | Smrt: {d['req_smrt']}"
                    if d['req_skills']:
                        req_skills_str = ", ".join([f"{s} Lv.{l}" for s, l in d['req_skills'].items()])
                        sec_text += f" | Skills: {req_skills_str}"

                    if can_apply:
                        lst.add_widget(TwoLineListItem(text=f"{d['icon']} {t}", secondary_text=sec_text, on_release=lambda x,t=t:self.get_job(t)))
                    else:
                        lst.add_widget(TwoLineListItem(text=f"{d['icon']} {t} [color=808080](Requirements not met)[/color]", secondary_text=sec_text, disabled=True))
        
        elif self.name == "asset":
            if self.engine.age < 18: lst.add_widget(OneLineListItem(text="Must be 18+ to buy assets."))
            else:
                lst.add_widget(OneLineListItem(text="--- Your Assets ---", disabled=True))
                if not self.engine.assets: lst.add_widget(OneLineListItem(text="No assets owned."))
                for i, a in enumerate(self.engine.assets):
                    asset_info = f"{SPRITES[a['type']]} {a['name']} (Value: ${a['val']:,})"
                    upkeep_cost = a['props'].get('upkeep', 0)
                    if upkeep_cost > 0: asset_info += f" | Upkeep: ${upkeep_cost:,}/yr"
                    lst.add_widget(TwoLineListItem(text=asset_info, secondary_text="Click to Sell", on_release=lambda x, idx=i: self.sell_asset_dialog(idx)))
                
                lst.add_widget(OneLineListItem(text="--- Available to Buy ---", disabled=True))
                for n, p, t, props in ASSETS:
                    lst.add_widget(TwoLineListItem(text=f"{SPRITES[t]} {n}", secondary_text=f"Cost: ${p:,} | Upkeep: ${props.get('upkeep', 0):,}/yr", on_release=lambda x,n=n,p=p,t=t,props=props:self.buy_asset(n,p,t,props)))
        
        elif self.name == "act":
            lst.add_widget(OneLineListItem(text="--- Health & Mind ---", disabled=True))
            opts = [("🏥 Visit Doctor ($100)", self.doc), ("🏋️ Go to Gym ($50)", self.gym), ("🧘 Meditate (Free)", self.meditate), ("🧠 Study (Improve Smrt/Skills, $200)", self.study)]
            for t, f in opts: lst.add_widget(OneLineListItem(text=t, on_release=f))
            
            lst.add_widget(OneLineListItem(text="--- Education ---", disabled=True))
            for program_name, data in EDUCATION_PROGRAMS.items():
                if program_name == self.engine.education:
                     lst.add_widget(OneLineListItem(text=f"{SPRITES['Degree']} {program_name} (Completed)", disabled=True))
                     continue
                if self.engine.current_education and self.engine.current_education['degree'] == data.get('degree'):
                    lst.add_widget(OneLineListItem(text=f"{SPRITES['Degree']} Currently enrolled in {program_name} ({self.engine.education_years_left} yrs left)", disabled=True))
                    continue

                can_enroll = self.engine.age >= data['min_age'] and self.engine.money >= data['cost']
                if data.get('req_smrt', 0) > self.engine.smrt: can_enroll = False

                if can_enroll:
                    lst.add_widget(TwoLineListItem(text=f"{SPRITES['School']} {program_name}", secondary_text=f"Cost: ${data['cost']:,} | Duration: {data['duration']} yrs", on_release=lambda x, p=program_name, d=data: self.enroll_education(p, d)))
                else:
                    sec_text = f"Cost: ${data['cost']:,} | Duration: {data['duration']} yrs"
                    if data.get('req_smrt', 0) > self.engine.smrt: sec_text += f" (Req. Smrt: {data['req_smrt']})"
                    lst.add_widget(TwoLineListItem(text=f"{SPRITES['School']} {program_name} [color=808080](Cannot Enroll)[/color]", secondary_text=sec_text, disabled=True))


            lst.add_widget(OneLineListItem(text="--- Social & Entertainment ---", disabled=True))
            opts = [("🎰 Go to Casino ($100)", self.casino), ("✈️ Travel (Varies)", self.travel), ("🧑‍🤝‍🧑 Volunteer (Free)", self.volunteer), ("❤️ Dating App", self.date)]
            for t, f in opts: lst.add_widget(OneLineListItem(text=t, on_release=f))

            lst.add_widget(OneLineListItem(text="--- Illegal ---", disabled=True))
            opts = [("🔫 Commit Crime", self.crime)]
            for t, f in opts: lst.add_widget(OneLineListItem(text=t, on_release=f))
            
        elif self.name == "rel":
            lst.add_widget(OneLineListItem(text="--- Family & Friends ---", disabled=True))
            for r in self.engine.relations:
                action_text = ""
                if r['type'] == 'Spouse':
                    action_text = " (Married)"
                elif r['type'] == 'Partner':
                    action_text = " (Partner)"
                    
                lst.add_widget(TwoLineListItem(text=f"{r['name']} ({r['type']})", secondary_text=f"Relationship: {r['rel']}% {action_text}", on_release=lambda x, rel_obj=r: self.interact_relation(rel_obj)))
            
            if self.engine.married_to:
                lst.add_widget(MDFillRoundFlatButton(text="HAVE A CHILD", on_release=self.have_child, size_hint_y=None, height="48dp", md_bg_color=(0,0.7,0,1)))
            
            lst.add_widget(OneLineListItem(text="--- Your Children ---", disabled=True))
            if not self.engine.children: lst.add_widget(OneLineListItem(text="No children yet."))
            for child in self.engine.children:
                lst.add_widget(OneLineListItem(text=f"{SPRITES['Child']} {child['name']} (Age: {child['age']})"))

            lst.add_widget(OneLineListItem(text="--- Your Skills ---", disabled=True))
            if not self.engine.skills: lst.add_widget(OneLineListItem(text="No skills acquired yet."))
            for skill, level in self.engine.skills.items():
                lst.add_widget(OneLineListItem(text=f"{SPRITES['Skill']} {skill} (Level: {level})"))
            lst.add_widget(OneLineListItem(text="--- Learn New Skills ---", disabled=True))
            for skill_name, data in SKILLS_LEARN.items():
                current_level = self.engine.get_skill_level(skill_name)
                req_smrt = data.get('smrt_req', 0)
                can_learn = self.engine.money >= data['cost'] and self.engine.smrt >= req_smrt
                
                sec_text = f"Cost: ${data['cost']:,} | Smrt Req: {req_smrt} | Current Lv: {current_level}"
                if can_learn:
                    lst.add_widget(TwoLineListItem(text=f"{SPRITES['Skill']} Learn {skill_name}", secondary_text=sec_text, on_release=lambda x, s_name=skill_name, s_data=data: self.learn_skill(s_name, s_data)))
                else:
                    lst.add_widget(TwoLineListItem(text=f"{SPRITES['Skill']} Learn {skill_name} [color=808080](Requirements not met)[/color]", secondary_text=sec_text, disabled=True))

        scroll.add_widget(lst); layout.add_widget(scroll)
        layout.add_widget(MDFillRoundFlatButton(text="BACK", size_hint=(1, 0.08), on_release=self.back))
        self.add_widget(layout)

    # ACTIONS
    def get_job(self, job_name):
        job_data = JOBS[job_name]
        if self.engine.age >= job_data['req_age'] and self.engine.smrt >= job_data['req_smrt']:
            can_apply = True
            for skill, level in job_data['req_skills'].items():
                if self.engine.get_skill_level(skill) < level:
                    can_apply = False
                    break
            if can_apply:
                self.engine.career = job_name
                self.engine.log(f"HIRED as {job_name}!", job_data['icon'])
                self.engine.adjust_stat("hap", 15); self.engine.adjust_stat("stress", -10)
            else:
                self.engine.log(f"Rejected from {job_name} (Skill req).", SPRITES['Sad'])
                self.engine.adjust_stat("hap", -5)
        else:
            self.engine.log(f"Rejected from {job_name} (Age/Smrt req).", SPRITES['Sad'])
            self.engine.adjust_stat("hap", -5)
        self.back()
    
    def quit_job(self, *x):
        self.engine.log(f"Quit job as {self.engine.career}.", "🚶")
        self.engine.career = "Unemployed"
        self.engine.adjust_stat("hap", -10); self.engine.adjust_stat("stress", -15)
        self.back()

    def buy_asset(self, n, p, t, props):
        if self.engine.money >= p: 
            self.engine.money -= p
            self.engine.assets.append({"name": n, "val": p, "type": t, "props": props})
            self.engine.log(f"Bought {n}!", SPRITES[t])
            self.engine.adjust_stat("hap", 10)
            self.engine.buzz(0.1)
        else: 
            self.engine.log("Insufficient funds.", SPRITES['Sad'])
            self.engine.buzz(0.2)
        self.back()

    def sell_asset_dialog(self, idx):
        asset = self.engine.assets[idx]
        def sell_confirmed(*args):
            self.sell_asset(idx)
            if self.dialog: # Ensure dialog exists before dismissing
                self.dialog.dismiss()
                self.dialog = None
        
        self.dialog = MDDialog(
            title="Sell Asset?",
            text=f"Are you sure you want to sell your {asset['name']} for ${asset['val']:,}?",
            buttons=[
                MDRectangleFlatButton(text="CANCEL", on_release=lambda x: (self.dialog.dismiss(), setattr(self, 'dialog', None))),
                MDFillRoundFlatButton(text="SELL", md_bg_color=(0.8,0,0,1), on_release=sell_confirmed)
            ]
        )
        self.dialog.open()

    def sell_asset(self, idx):
        asset = self.engine.assets.pop(idx)
        self.engine.money += asset['val']
        self.engine.log(f"Sold {asset['name']} for ${asset['val']:,}.", SPRITES['Money'])
        self.engine.adjust_stat("hap", 5)
        self.back()

    def doc(self, *x): 
        if self.engine.money>=100:
            self.engine.money-=100; self.engine.adjust_stat("hlt", 100-self.engine.hlt + 10); # Heal to 100 + a bit extra if already low
            self.engine.adjust_stat("stress", -20)
            self.engine.log("Visited Doctor. Feeling much better!", SPRITES['Doc'])
            self.engine.buzz(0.05)
        else: self.engine.log("Need $100 for doctor's visit.", SPRITES['Sad'])
        self.back()
    
    def gym(self, *x):
        if self.engine.money>=50:
            self.engine.money-=50
            self.engine.adjust_stat("hlt", random.randint(5, 15))
            self.engine.adjust_stat("energy", -random.randint(10, 20))
            self.engine.adjust_stat("stress", -5)
            self.engine.log("Worked out at the gym. Feeling stronger!", SPRITES['Gym'])
            self.engine.buzz(0.05)
        else: self.engine.log("Need $50 for the gym.", SPRITES['Sad'])
        self.back()

    def meditate(self, *x):
        self.engine.adjust_stat("stress", -random.randint(10, 25))
        self.engine.adjust_stat("hap", random.randint(5, 10))
        self.engine.adjust_stat("energy", random.randint(5, 10))
        self.engine.log("Meditated. Feeling calm and refreshed.", SPRITES['Meditate'])
        self.engine.buzz(0.05)
        self.back()

    def study(self, *x):
        if self.engine.money >= 200:
            self.engine.money -= 200
            self.engine.adjust_stat("smrt", random.randint(3, 8))
            self.engine.adjust_stat("stress", 5)
            self.engine.adjust_stat("energy", -random.randint(5, 10))
            self.engine.log("Studied hard. Brain power increased!", SPRITES['Study'])
            self.engine.buzz(0.05)
        else:
            self.engine.log("Need $200 for study materials.", SPRITES['Sad'])
        self.back()

    def enroll_education(self, program_name, data):
        if self.engine.money >= data['cost']:
            self.engine.money -= data['cost'] # Initial cost deduction
            self.engine.current_education = data
            self.engine.education_years_left = data['duration']
            self.engine.log(f"Enrolled in {program_name}! Costs spread over {data['duration']} years.", SPRITES['Degree'])
            self.engine.buzz(0.1)
        else:
            self.engine.log(f"Insufficient funds to enroll in {program_name}.", SPRITES['Sad'])
            self.engine.buzz(0.2)
        self.back()
    
    def learn_skill(self, skill_name, data):
        if self.engine.money >= data['cost'] and self.engine.smrt >= data['smrt_req']:
            self.engine.money -= data['cost']
            self.engine.skills[skill_name] = self.engine.skills.get(skill_name, 0) + data['effect'].get("skill_level", 1)
            self.engine.adjust_stat("smrt", data['effect'].get("smrt", 0))
            self.engine.adjust_stat("hap", data['effect'].get("hap", 0))
            self.engine.adjust_stat("hlt", data['effect'].get("hlt", 0))
            self.engine.adjust_stat("fame", data['effect'].get("fame", 0))
            self.engine.log(f"Improved {skill_name} skill to Level {self.engine.skills[skill_name]}!", SPRITES['Skill'])
            self.engine.buzz(0.08)
        else:
            self.engine.log(f"Cannot learn {skill_name}. Check funds or smartness.", SPRITES['Sad'])
            self.engine.buzz(0.2)
        self.back()

    def crime(self, *x):
        self.engine.adjust_stat("energy", -random.randint(10, 20))
        if random.random() > 0.6: # 40% chance of success
            loot = random.randint(500, 5000)
            self.engine.money += loot
            self.engine.adjust_stat("karma", -random.randint(5, 15), min_val=-100)
            self.engine.adjust_stat("hap", 5)
            self.engine.log(f"Successfully committed crime, gained ${loot:,}!", SPRITES['Money'])
            self.engine.buzz(0.1)
        else: 
            jail_time = random.randint(2, 5)
            self.engine.jail = jail_time
            self.engine.adjust_stat("karma", -random.randint(10, 25), min_val=-100)
            self.engine.adjust_stat("hap", -20)
            self.engine.adjust_stat("fame", -10)
            self.engine.log(f"ARRESTED! Serving {jail_time} years.", SPRITES['Jail'])
            self.engine.buzz(0.5) # Longer vibration for negative event
        self.back()
    
    def casino(self, *x):
        if self.engine.money >= 100:
            self.engine.money -= 100
            self.engine.adjust_stat("energy", -5)
            if random.random() > 0.55: # 45% chance to win
                winnings = random.randint(150, 500)
                self.engine.money += winnings
                self.engine.adjust_stat("hap", 10)
                self.engine.log(f"Won ${winnings:,} at the casino!", SPRITES['Casino'])
            else:
                self.engine.adjust_stat("hap", -5)
                self.engine.log("Lost $100 at the casino.", "💸")
            self.engine.buzz(0.05)
        else: self.engine.log("Need $100 to gamble.", SPRITES['Sad'])
        self.back()

    def travel(self, *x):
        if self.engine.money >= 1000:
            self.engine.money -= 1000
            self.engine.adjust_stat("hap", 20)
            self.engine.adjust_stat("stress", -20)
            self.engine.adjust_stat("fame", random.randint(0, 5))
            self.engine.log("Traveled to an exotic location! Feeling rejuvenated.", SPRITES['Travel'])
            self.engine.buzz(0.08)
        else: self.engine.log("Need $1000 to travel.", SPRITES['Sad'])
        self.back()
    
    def volunteer(self, *x):
        self.engine.adjust_stat("hap", 15)
        self.engine.adjust_stat("karma", 10, max_val=100)
        self.engine.adjust_stat("stress", -10)
        self.engine.log("Volunteered for a good cause! Boosted karma.", SPRITES['Volunteer'])
        self.engine.buzz(0.05)
        self.back()

    def date(self, *x):
        if self.engine.age < 18:
            self.engine.log("Too young to date.", SPRITES['Sad'])
            self.back()
            return

        if self.engine.married_to:
            self.engine.log("Already married! Consider other relationship actions.", SPRITES['Love'])
            self.back()
            return

        n = random.choice(["Ashley","Jessica","Mike","Chris"])
        rel_exists = False
        for r in self.engine.relations:
            if r['name'] == n and r['type'] == 'Partner':
                self.engine.log(f"Already dating {n}!", SPRITES['Love'])
                rel_exists = True
                break
        if not rel_exists:
            self.engine.relations.append({"name": n, "rel": 50, "type": "Partner"})
            self.engine.log(f"Started dating {n}!", SPRITES['Love'])
            self.engine.adjust_stat("hap", 10)
        self.back()

    def interact_relation(self, rel_obj):
        def offer_marriage_confirmed(*args):
            if self.dialog: # Ensure dialog exists before dismissing
                self.dialog.dismiss()
                self.dialog = None
            if self.engine.married_to:
                self.engine.log(f"You are already married to {self.engine.married_to}.", SPRITES['Sad'])
                self.back()
                return
            if random.random() < rel_obj['rel'] / 100.0 * 0.8: # Higher chance with better relationship
                self.engine.married_to = rel_obj['name']
                rel_obj['type'] = 'Spouse' # Update type in relations list
                self.engine.log(f"You married {rel_obj['name']}! Congratulations!", SPRITES['Marriage'])
                self.engine.adjust_stat("hap", 30); self.engine.adjust_stat("fame", 10)
            else:
                self.engine.log(f"{rel_obj['name']} rejected your proposal. Relationship declined.", SPRITES['Sad'])
                rel_obj['rel'] = max(0, rel_obj['rel'] - 20)
                self.engine.adjust_stat("hap", -15); self.engine.adjust_stat("stress", 10)
            self.back()

        def try_improve_relationship_confirmed(*args):
            if self.dialog: # Ensure dialog exists before dismissing
                self.dialog.dismiss()
                self.dialog = None
            cost = random.randint(50, 200)
            if self.engine.money >= cost:
                self.engine.money -= cost
                gain = random.randint(5, 20) * (1 if self.engine.look > 50 else 0.5)
                rel_obj['rel'] = min(100, rel_obj['rel'] + gain)
                self.engine.log(f"Improved relationship with {rel_obj['name']} by {int(gain)}%. Spent ${cost}.", SPRITES['Love'])
                self.engine.adjust_stat("hap", 5)
            else:
                self.engine.log(f"Couldn't afford to interact with {rel_obj['name']}. Need ${cost}.", SPRITES['Sad'])
            self.back()

        buttons = []
        if rel_obj['type'] == 'Partner' and not self.engine.married_to:
            buttons.append(MDRectangleFlatButton(text="Propose Marriage", on_release=offer_marriage_confirmed))
        
        buttons.append(MDRectangleFlatButton(text="Improve Relationship", on_release=try_improve_relationship_confirmed))
        buttons.append(MDRectangleFlatButton(text="Back", on_release=lambda x: (self.dialog.dismiss(), setattr(self, 'dialog', None))))

        self.dialog = MDDialog(
            title=f"Interact with {rel_obj['name']}",
            text=f"Relationship: {rel_obj['rel']}%",
            buttons=buttons
        )
        self.dialog.open()

    def have_child(self, *x):
        if not self.engine.married_to:
            self.engine.log("Must be married to have a child.", SPRITES['Sad'])
            self.back()
            return
        
        if random.random() < 0.7: # 70% chance to conceive
            child_name = random.choice(['Max','Leo','Zoe','Lily'])
            self.engine.children.append({"name": child_name, "age": 0})
            self.engine.log(f"Congratulations! You had a child named {child_name}!", SPRITES['Baby'])
            self.engine.adjust_stat("hap", 25); self.engine.adjust_stat("stress", 15)
        else:
            self.engine.log("Could not conceive a child this year.", SPRITES['Sad'])
            self.engine.adjust_stat("hap", -5); self.engine.adjust_stat("stress", 5)
        self.back()

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