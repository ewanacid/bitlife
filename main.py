import os, sys, random, json, traceback
# FORCE STABILITY
os.environ["KIVY_NO_ARGS"] = "1"

from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField 
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, DictProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
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
    "Bank": "🏦", "Stocks": "📈", "Crypto": "₿", "Business": "🏭",
    "LifeOrb": "🌟", "Opportunity": "✨", "Wisdom": "🦉", "Charm": "✨",
    "Strength": "💪", "Spirit": "👻"
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
    "High School": {"cost": 0, "smrt_gain": 5, "min_age": 14, "duration": 4, "degree": "High School Diploma"},
    "University (Bachelors)": {"cost": 50000, "smrt_gain": 20, "min_age": 18, "duration": 4, "degree": "Bachelors"},
    "Medical School (MD)": {"cost": 200000, "smrt_gain": 30, "min_age": 22, "duration": 4, "degree": "Doctorate", "req_smrt": 80, "req_degree": "Bachelors"},
    "Law School (JD)": {"cost": 150000, "smrt_gain": 25, "min_age": 22, "duration": 3, "degree": "Doctorate", "req_smrt": 75, "req_degree": "Bachelors"}
}

SKILLS_LEARN = {
    "Coding": {"cost": 1000, "smrt_req": 20, "effect": {"smrt": 2, "skill_level": 1}},
    "Teaching": {"cost": 500, "smrt_req": 15, "effect": {"hap": 5, "skill_level": 1}},
    "Medicine": {"cost": 5000, "smrt_req": 70, "effect": {"hlt": 2, "skill_level": 1}},
    "Leadership": {"cost": 2000, "smrt_req": 50, "effect": {"fame": 5, "skill_level": 1}},
    "Art": {"cost": 300, "smrt_req": 10, "effect": {"hap": 3, "skill_level": 1}},
    "Music": {"cost": 300, "smrt_req": 10, "effect": {"hap": 3, "skill_level": 1}},
}

LIFE_ORBS = {
    "Life Orb": {"icon": SPRITES['LifeOrb'], "effect": {"hlt": 20, "energy": 20}, "description": "Restores health and energy."},
    "Wisdom Orb": {"icon": SPRITES['Wisdom'], "effect": {"smrt": 15}, "description": "Increases smarts."},
    "Charm Orb": {"icon": SPRITES['Charm'], "effect": {"look": 15}, "description": "Increases looks."},
    "Strength Orb": {"icon": SPRITES['Strength'], "effect": {"hlt": 10, "energy": 10}, "description": "Minor health/energy boost."},
    "Spirit Orb": {"icon": SPRITES['Spirit'], "effect": {"hap": 15, "stress": -10}, "description": "Boosts happiness and reduces stress."}
}

# --- DEEP SIMULATION ENGINE ---
class SimEngine:
    def __init__(self):
        self.char_name = ""
        self.char_gender = "Male"
        self.initial_smrt = 0
        self.initial_look = 0
        self.initial_hap = 0
        self.initial_hlt = 0
        self.initial_karma = 0
        self.initial_stress = 0
        self.initial_energy = 0
        self.initial_fame = 0
        self.generate_initial_stats()
        self.reset()
        self.dialog_queue = []
        self.life_orb_locations = []
        self.MAX_LIFE_ORBS = 3

    def generate_initial_stats(self):
        self.initial_smrt = random.randint(20, 90)
        self.initial_look = random.randint(20, 90)
        self.initial_hap = random.randint(70, 100)
        self.initial_hlt = random.randint(80, 100)
        self.initial_karma = random.randint(-10, 10)
        self.initial_stress = random.randint(10, 30)
        self.initial_energy = random.randint(80, 100)
        self.initial_fame = random.randint(-5, 5)

    def set_character_details(self, name, gender):
        self.char_name = name
        self.char_gender = gender

    def reset(self):
        self.name = self.char_name if self.char_name else f"{random.choice(['Liam','Noah','Oliver','James','Emma','Ava'])} {random.choice(['Smith','Jones','Brown','Garcia'])}"
        self.gender = self.char_gender if self.char_gender else random.choice(["Male", "Female"])
        self.face = SPRITES[self.gender]
        self.age = 0
        self.money = 0
        self.career = "Unemployed"
        self.education = "None"
        self.current_education = None
        self.education_years_left = 0
        
        self.hap = self.initial_hap
        self.hlt = self.initial_hlt
        self.smrt = self.initial_smrt
        self.look = self.initial_look
        self.karma = self.initial_karma
        self.stress = self.initial_stress
        self.energy = self.initial_energy
        self.fame = self.initial_fame
        
        self.alive = True
        self.jail = 0
        self.assets = []
        self.relations = [{"name": "Mom", "rel": 100, "type": "Family"}, {"name": "Dad", "rel": 100, "type": "Family"}]
        self.married_to = None
        self.children = []
        self.skills = {}
        self.inventory = {} # For life orbs and other items
        
        self.log_history = [f"{SPRITES['Baby']} Born a {self.gender} in the Year 3000."]
        self.scenario = None
        self.game_over_reason = None
        self.life_orb_locations = [] # Reset orb locations on new game

    def log(self, text, icon=""):
        self.log_history.insert(0, f"Age {self.age}: {icon} {text}")
        
    def buzz(self, duration=0.05):
        try: vibrator.vibrate(duration)
        except: pass

    def adjust_stat(self, stat_name, amount, min_val=0, max_val=100, allow_below_min=False):
        current_val = getattr(self, stat_name)
        new_val = current_val + amount
        
        if not allow_below_min:
            if new_val < min_val: new_val = min_val
        if new_val > max_val: new_val = max_val
        
        setattr(self, stat_name, new_val)
        return new_val

    def age_up(self):
        if not self.alive: return
        self.age += 1
        self.buzz(0.03)

        self.adjust_stat("energy", -5) # natural energy decay
        self.adjust_stat("stress", random.randint(-2, 5)) # random stress changes
        self.adjust_stat("hlt", -1) # natural health decay
        
        if self.jail > 0:
            self.jail -= 1
            self.adjust_stat("hap", -15)
            self.adjust_stat("stress", 20)
            self.log(f"Serving time ({self.jail} yrs left).", SPRITES['Jail'])
            if self.jail == 0: self.log("Released from prison!", "🔓"); self.adjust_stat("stress", -30)
            self.check_death()
            return

        if self.current_education:
            self.education_years_left -= 1
            self.adjust_stat("smrt", self.current_education['smrt_gain'] / self.current_education['duration'])
            self.adjust_stat("stress", 10)
            yearly_cost = self.current_education['cost'] / self.current_education['duration']
            
            if self.money >= yearly_cost:
                self.adjust_stat("money", -yearly_cost, allow_below_min=True)
            else:
                self.log(f"Couldn't afford tuition. Dropped out.", SPRITES['Sad'])
                self.adjust_stat("smrt", -10)
                self.education = "None"
                self.current_education = None
                # Check for required degree for job
                if self.career != "Unemployed":
                    job_data = JOBS.get(self.career)
                    if job_data and job_data.get('req_degree') and self.education != job_data['req_degree']:
                        self.log(f"Lost {self.career} job due to insufficient education.", SPRITES['Layoff'])
                        self.career = "Unemployed"
                return

            self.log(f"Studying for {self.current_education['degree']} ({self.education_years_left} yrs left).", SPRITES['Study'])
            if self.education_years_left <= 0:
                self.education = self.current_education['degree']
                self.log(f"Graduated with a {self.education}!", SPRITES['Degree'])
                self.current_education = None
                self.adjust_stat("smrt", 10)
        
        if self.career != "Unemployed" and not self.current_education:
            job_data = JOBS.get(self.career)
            if job_data:
                sal_factor = 1 + (self.skills.get("Leadership", 0) * 0.05) + (self.smrt / 200)
                base_sal = job_data['sal'] * sal_factor
                tax_rate = 0.3 if base_sal > 100000 else 0.15
                net = int(base_sal * (1 - tax_rate))
                self.money += net
                self.adjust_stat("stress", job_data['stress'] / 10)
                self.adjust_stat("hap", 2) # small happiness boost from working
                self.log(f"Earned ${net:,} from {self.career}.", SPRITES['Money'])

                if random.random() < job_data['promo_chance']:
                    self.log(f"Got a promotion! Salary increased!", SPRITES['Promotion'])
                    job_data['sal'] = int(job_data['sal'] * 1.1) # Small salary increase
                    self.adjust_stat("money", 5000, allow_below_min=True); self.adjust_stat("hap", 10)
                elif random.random() < job_data['layoff_chance']:
                    self.log(f"Laid off from {self.career}!", SPRITES['Layoff'])
                    self.career = "Unemployed"; self.adjust_stat("stress", 30)
        
        assets_to_remove = []
        for i, asset in enumerate(self.assets):
            props = asset['props']
            upkeep = props.get('upkeep', 0)
            
            if self.money >= upkeep: self.money -= upkeep
            else:
                self.log(f"Couldn't afford upkeep for {asset['name']}. Value depreciated.", SPRITES['Sad'])
                asset['val'] = int(asset['val'] * 0.9) # Penalty for not paying upkeep
                self.adjust_stat("stress", 5)

            if asset['type'] == 'House':
                asset['val'] = int(asset['val'] * (1 + props.get('appreciation', 0.0)))
            elif asset['type'] == 'Car':
                asset['val'] = int(asset['val'] * (1 - props.get('depreciation', 0.0)))
                if asset['val'] < 1000 and random.random() < 0.2:
                    self.log(f"{asset['name']} broke down beyond repair.", SPRITES['Sad'])
                    assets_to_remove.append(i)
            elif asset['type'] in ['Stocks', 'Crypto']:
                change = (random.random() * 2 - 1) * props.get('volatility', 0) * asset['val']
                asset['val'] += int(change)
                asset['val'] = max(1, asset['val'])

        for i in reversed(assets_to_remove): self.assets.pop(i)

        self.adjust_stat("energy", 30) # daily energy regeneration
        self.adjust_stat("stress", -5) # passive stress reduction if no major events

        # Negative effects of extreme stats
        if self.stress > 80: self.adjust_stat("hlt", -5); self.adjust_stat("hap", -10); self.log("High stress is taking a toll.", SPRITES['Stress'])
        if self.energy < 10: self.adjust_stat("hlt", -5); self.adjust_stat("stress", 10); self.log("Low energy makes you feel unwell.", SPRITES['Energy'])
        if self.hlt < 20: self.adjust_stat("hap", -10); self.adjust_stat("stress", 10); self.log("Poor health affects your mood.", SPRITES['Sick'])
        if self.hap < 20: self.adjust_stat("stress", 5); self.log("Unhappiness adds to your stress.", SPRITES['Sad'])

        for r in self.relations:
            if r['type'] in ['Family', 'Spouse']:
                self.adjust_stat("hap", r['rel'] / 200) # Small happiness boost from good relations
                if random.random() < 0.03 and r['rel'] > 20: 
                    r['rel'] = max(0, r['rel'] - random.randint(5, 15)) # Small chance of relationship decay
                    self.log(f"Relationship with {r['name']} deteriorated a little.", SPRITES['Sad'])
            elif r['type'] == 'Child':
                if random.random() < 0.05 and r['rel'] > 20: 
                    r['rel'] = max(0, r['rel'] - random.randint(5, 10))
                self.adjust_stat("hap", r['rel'] / 300)

        for child in self.children: child['age'] += 1

        self.run_random_events()
        self.spawn_life_orbs()
        self.check_death()

    def check_death(self):
        if not self.alive: return
        death_chance = 0.0
        death_reason = ""

        if self.age > 80: death_chance += (self.age - 80) * 0.03; death_reason = "old age"
        if self.hlt <= 0: death_chance += 1.0; death_reason = "poor health"
        elif self.hlt < 20: death_chance += 0.1; death_reason = "critical health"
        if self.stress >= 95 and random.random() < 0.1: death_chance += 0.5; death_reason = "stress-induced collapse"
        if self.energy <= 0: death_chance += 0.05; death_reason = "exhaustion"
        
        # Random accidents
        if random.random() < 0.005 and self.age >= 16:
            death_chance += 0.2
            death_reason = random.choice(["car accident", "freak accident", "crime victim"])

        if random.random() < death_chance:
            self.alive = False
            self.face = SPRITES['Dead']
            self.game_over_reason = death_reason
            self.log(f"Died at age {self.age} from {death_reason}.", SPRITES['Dead'])
            self.buzz(1.0)
            self.dialog_queue.append(("Game Over!", f"You died at age {self.age} from {death_reason}. Net Worth: ${self.get_net_worth():,}.", [("New Game", self.reset_game)]))

    def run_random_events(self):
        roll = random.random()
        if roll < 0.03: # Higher chance for sickness
            self.adjust_stat("hlt", -random.randint(10, 25)); self.adjust_stat("energy", -10);
            self.log("Caught a nasty flu.", SPRITES['Sick'])
            if self.age > 60: self.log("The flu is hitting harder due to age.", SPRITES['Sad'])
        elif roll < 0.08: prize = random.randint(100, 1000); self.money += prize; self.log(f"Found ${prize}!", SPRITES['Money'])
        elif roll < 0.10 and self.age >= 18: self.scenario = "wallet" # Scenario with choices
        elif roll < 0.12 and self.age >= 18 and self.career == "Unemployed": # Job Opportunity
            self.scenario = "job_offer"
        elif roll < 0.15 and self.age >= 16: # Relationship event
            if not self.married_to and random.random() < 0.5:
                partner_name = random.choice(["Alex", "Jamie", "Chris", "Taylor"])
                self.relations.append({"name": partner_name, "rel": random.randint(50, 80), "type": "Partner"})
                self.log(f"Met {partner_name}, a potential partner!", SPRITES['Love'])
            elif self.married_to:
                self.adjust_stat("hap", 5)
                self.log(f"Shared a nice moment with {self.married_to}.", SPRITES['Love'])

    def spawn_life_orbs(self):
        if len(self.life_orb_locations) < self.MAX_LIFE_ORBS and random.random() < 0.1: # 10% chance to spawn an orb each year
            orb_type = random.choice(list(LIFE_ORBS.keys()))
            location_options = ["Park", "Old bookstore", "Mountain trail", "Quiet cafe", "City alley"]
            location = random.choice(location_options)
            self.life_orb_locations.append({"type": orb_type, "location": location})
            self.log(f"A {orb_type} has appeared in the {location}!", LIFE_ORBS[orb_type]['icon'])

    def discover_life_orb(self):
        if not self.life_orb_locations:
            self.log("No life orbs currently available to discover.", SPRITES['Sad'])
            return False
        
        orb_found = random.choice(self.life_orb_locations)
        self.life_orb_locations.remove(orb_found)
        
        orb_type = orb_found['type']
        orb_data = LIFE_ORBS[orb_type]
        
        if orb_type not in self.inventory:
            self.inventory[orb_type] = 0
        self.inventory[orb_type] += 1
        
        self.log(f"Discovered a {orb_type} in the {orb_found['location']}!", orb_data['icon'])
        self.dialog_queue.append((f"Found a {orb_type}!", f"You found a {orb_type} at the {orb_found['location']}. It's been added to your inventory.", []))
        return True

    def use_life_orb(self, orb_type):
        if orb_type in self.inventory and self.inventory[orb_type] > 0:
            orb_data = LIFE_ORBS[orb_type]
            for stat, amount in orb_data['effect'].items():
                self.adjust_stat(stat, amount)
            self.inventory[orb_type] -= 1
            self.log(f"Used a {orb_type}. {orb_data['description']}", orb_data['icon'])
            return True
        self.log(f"No {orb_type} in inventory.", SPRITES['Sad'])
        return False


    def get_net_worth(self):
        return self.money + sum(a['val'] for a in self.assets)
    
    def get_skill_level(self, skill_name):
        return self.skills.get(skill_name, 0)

    def reset_game(self):
        self.generate_initial_stats()
        self.char_name = ""
        self.char_gender = "Male"
        self.reset()
        app = MDApp.get_running_app()
        app.root.current = 'char_create'

# --- UI COMPONENTS ---
class LogEntryViewClass(RecycleDataViewBehavior, MDLabel):
    def refresh_view_attrs(self, rv, index, data):
        self.text = data['text']
        self.halign = 'left'
        self.valign = 'middle'
        self.size_hint_y = None
        self.height = dp(32)
        self.theme_text_color = "Primary"
        self.markup = True
        return super().refresh_view_attrs(rv, index, data)

class SelectableTwoLineIconListItem(RecycleDataViewBehavior, ButtonBehavior, MDBoxLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    icon = StringProperty("")
    callback = ObjectProperty(None)
    disabled = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(10), dp(5)]
        self.spacing = dp(2)
        self.size_hint_y = None
        self.height = dp(64)

        self.primary_label = MDLabel(markup=True, font_style="Subtitle1", theme_text_color="Primary", size_hint_y=0.6)
        self.secondary_label = MDLabel(markup=True, font_style="Caption", theme_text_color="Secondary", size_hint_y=0.4)
        self.add_widget(self.primary_label)
        self.add_widget(self.secondary_label)

    def refresh_view_attrs(self, rv, index, data):
        self.text = data['text']
        self.secondary_text = data.get('secondary_text', '')
        self.icon = data.get('icon', '')
        self.callback = data.get('callback', None)
        self.disabled = data.get('disabled', False)

        main_text_content = f"{self.icon} {self.text}" if self.icon else self.text
        if self.disabled:
            self.primary_label.text = f"[color=808080]{main_text_content}[/color]"
            self.secondary_label.text = f"[color=808080]{self.secondary_text}[/color]"
            self.md_bg_color = [0.15, 0.15, 0.15, 1]
        else:
            self.primary_label.text = main_text_content
            self.secondary_label.text = self.secondary_text
            self.md_bg_color = [0.2, 0.2, 0.2, 1]

        return super().refresh_view_attrs(rv, index, data)

    def on_release(self):
        if not self.disabled and self.callback:
            self.callback()

class StatBar(MDBoxLayout):
    lbl_text = StringProperty("")
    bar_value = NumericProperty(0)
    bar_color = ListProperty([0, 0, 0, 1])
    is_percent = BooleanProperty(True)

    def __init__(self, label, value, color, is_percent=True, **kwargs):
        super().__init__(orientation='vertical', size_hint_x=0.25, **kwargs)
        self.is_percent = is_percent
        self.update_label_text(label, value)
        self.bar_value = value
        self.bar_color = color
        self.lbl = MDLabel(text=self.lbl_text, halign="center", font_style="Caption", theme_text_color="Custom", text_color=color)
        self.add_widget(self.lbl)
        self.bar = MDProgressBar(value=self.bar_value, color=self.bar_color, size_hint_y=None, height="6dp")
        self.add_widget(self.bar)

    def update_label_text(self, label_base, value):
        display_val = max(0, min(100, value))
        self.lbl_text = f"{label_base}: {int(display_val)}%" if self.is_percent else f"{label_base}: {int(value)}"
    
    def update(self, val):
        label_base = self.lbl.text.split(':')[0]
        self.update_label_text(label_base, val)
        self.bar.value = max(0, min(100, val))

# --- SCREENS ---
class CharacterCreationScreen(Screen):
    selected_gender = StringProperty("Male")

    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self.engine.generate_initial_stats() # Ensure stats are fresh for display
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        layout.add_widget(MDLabel(text="CREATE YOUR CHARACTER", font_style="H4", halign="center", size_hint_y=0.15))

        self.name_input = MDTextField(hint_text="Enter Name", text=self.engine.char_name, size_hint_y=None, height=dp(48))
        layout.add_widget(self.name_input)

        gender_box = MDBoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        self.btn_male = MDFillRoundFlatButton(text=f"{SPRITES['Male']} Male", on_release=lambda x: self.select_gender("Male"))
        self.btn_female = MDFillRoundFlatButton(text=f"{SPRITES['Female']} Female", on_release=lambda x: self.select_gender("Female"))
        gender_box.add_widget(self.btn_male)
        gender_box.add_widget(self.btn_female)
        layout.add_widget(gender_box)

        # Display initial stats
        stats_grid = MDBoxLayout(orientation='vertical', size_hint_y=0.4, spacing=dp(5))
        stats_grid.add_widget(MDLabel(text=f"Initial Smarts: {self.engine.initial_smrt}%", halign="center"))
        stats_grid.add_widget(MDLabel(text=f"Initial Looks: {self.engine.initial_look}%", halign="center"))
        stats_grid.add_widget(MDLabel(text=f"Initial Happiness: {self.engine.initial_hap}%", halign="center"))
        stats_grid.add_widget(MDLabel(text=f"Initial Health: {self.engine.initial_hlt}%", halign="center"))
        layout.add_widget(stats_grid)

        btn_start = MDFillRoundFlatButton(text="START GAME", on_release=self.start_game, size_hint_y=None, height=dp(50))
        layout.add_widget(btn_start)
        self.add_widget(layout)
        self.select_gender(self.engine.char_gender)

    def select_gender(self, gender):
        self.selected_gender = gender
        self.engine.char_gender = gender
        # Highlight selected gender
        self.btn_male.md_bg_color = self.app.theme_cls.primary_color if gender == "Male" else (0.2, 0.2, 0.2, 1)
        self.btn_female.md_bg_color = self.app.theme_cls.primary_color if gender == "Female" else (0.2, 0.2, 0.2, 1)

    def start_game(self, *args):
        name = self.name_input.text.strip()
        if not name:
            name = f"{random.choice(['Liam','Noah','Oliver','James','Emma','Ava'])} {random.choice(['Smith','Jones','Brown','Garcia'])}"
        self.engine.set_character_details(name, self.selected_gender)
        self.app.engine.reset() # Reset engine with new character details
        # Removed the direct build_ui call for 'game' screen as on_enter handles it for first time entry
        self.app.root.current = 'game'

class GameScreen(Screen):
    def on_enter(self):
        self.app = MDApp.get_running_app()
        self.engine = self.app.engine
        self._current_dialog = None
        # Only build UI if it hasn't been built before (i.e., self.ids is empty)
        if not self.ids:
             self.build_ui()
        self.update() # Initial update when entering screen
        Clock.schedule_interval(self.check_dialog_queue, 0.5) # Check for dialogs more frequently

    def build_ui(self):
        self.clear_widgets()
        root = MDBoxLayout(orientation='vertical', padding=[dp(10), dp(5)], spacing=dp(5))

        head = MDBoxLayout(orientation='horizontal', size_hint_y=0.15)
        self.lbl_face = MDLabel(text=self.engine.face, font_style="H2", size_hint_x=0.2, halign="center", id='lbl_face')
        info = MDBoxLayout(orientation='vertical')
        self.lbl_name = MDLabel(text="Name", font_style="H6", bold=True, id='lbl_name')
        self.lbl_job = MDLabel(text="Job", theme_text_color="Secondary", id='lbl_job')
        self.lbl_bank = MDLabel(text="$$$", theme_text_color="Custom", text_color=(0,1,0,1), id='lbl_bank')
        info.add_widget(self.lbl_name); info.add_widget(self.lbl_job); info.add_widget(self.lbl_bank)
        head.add_widget(self.lbl_face); head.add_widget(info)
        root.add_widget(head)

        self.log_rv = RecycleView(viewclass=LogEntryViewClass, size_hint=(1, 0.45), id='log_rv')
        self.log_rv_layout = RecycleBoxLayout(default_size=(None, dp(32)), default_size_hint=(1, None),
                                                orientation='vertical', size_hint_y=None)
        self.log_rv_layout.bind(minimum_height=self.log_rv_layout.setter('height'))
        self.log_rv.add_widget(self.log_rv_layout)
        root.add_widget(self.log_rv)

        self.age_button = MDFillRoundFlatButton(text="AGE UP +", font_size=26, size_hint=(1, 0.12), md_bg_color=(0, 0.7, 0, 1), on_release=self.do_age, id='age_button')
        root.add_widget(self.age_button)

        stats_row1 = MDBoxLayout(size_hint_y=0.08, spacing=dp(5))
        self.s_hap = StatBar("Hap", 100, (0,1,0,1), id='s_hap')
        self.s_hlt = StatBar("Hlt", 100, (1,0,0,1), id='s_hlt')
        self.s_smrt = StatBar("Smrt", 100, (0,0,1,1), id='s_smrt')
        self.s_lok = StatBar("Look", 100, (1,0.5,0,1), id='s_lok')
        stats_row1.add_widget(self.s_hap); stats_row1.add_widget(self.s_hlt)
        stats_row1.add_widget(self.s_smrt); stats_row1.add_widget(self.s_lok)
        root.add_widget(stats_row1)
        
        stats_row2 = MDBoxLayout(size_hint_y=0.08, spacing=dp(5))
        self.s_karma = StatBar("Karma", 0, (0.7, 0.7, 0.7, 1), is_percent=False, id='s_karma')
        self.s_stress = StatBar("Stress", 0, (1, 0, 1, 1), id='s_stress')
        self.s_energy = StatBar("Energy", 100, (1, 1, 0, 1), id='s_energy')
        self.s_fame = StatBar("Fame", 0, (0.9, 0.7, 0.2, 1), is_percent=False, id='s_fame')
        stats_row2.add_widget(self.s_karma); stats_row2.add_widget(self.s_stress)
        stats_row2.add_widget(self.s_energy); stats_row2.add_widget(self.s_fame)
        root.add_widget(stats_row2)

        nav = MDBoxLayout(size_hint_y=0.08, spacing=dp(2))
        nav.add_widget(MDRectangleFlatButton(text="JOB", size_hint=(0.25, 1), on_release=lambda x: self.menu("job")))
        nav.add_widget(MDRectangleFlatButton(text="ASSET", size_hint=(0.25, 1), on_release=lambda x: self.menu("asset")))
        nav.add_widget(MDRectangleFlatButton(text="REL", size_hint=(0.25, 1), on_release=lambda x: self.menu("rel")))
        nav.add_widget(MDRectangleFlatButton(text="ACT", size_hint=(0.25, 1), on_release=lambda x: self.menu("act")))
        root.add_widget(nav)

        self.add_widget(root)
        self.update()

    def update(self, *args):
        e = self.engine
        self.age_button.disabled = not e.alive
        if not e.alive: self.age_button.text = f"GAME OVER! {e.game_over_reason.upper()}"
        else: self.age_button.text = f"AGE UP ({e.age}) +"
        
        self.lbl_face.text = e.face
        self.lbl_name.text = f"{e.name} ({e.age}) {e.gender}"
        self.lbl_job.text = f"{e.career} | {e.education}"
        self.lbl_bank.text = f"${e.money:,} | Net: ${e.get_net_worth():,}"
        
        self.s_hap.update(e.hap); self.s_hlt.update(e.hlt)
        self.s_smrt.update(e.smrt); self.s_lok.update(e.look)
        self.s_karma.update(e.karma); self.s_stress.update(e.stress)
        self.s_energy.update(e.energy); self.s_fame.update(e.fame)
        
        self.log_rv.data = [{'text': txt} for txt in e.log_history[:50]]
        self.log_rv.refresh_from_data() # Ensure RV updates visually

        # Process dialog queue
        if e.dialog_queue and (self._current_dialog is None or not self._current_dialog.is_open):
            title, text, opts = e.dialog_queue.pop(0)
            self.show_popup(title, text, opts)

    def check_dialog_queue(self, dt):
        self.update() # Update UI and check for dialogs

    def do_age(self, *x): 
        if self.engine.alive:
            self.engine.age_up()
            self.update()
            # If a scenario was triggered during age_up, open it immediately
            if self.engine.scenario:
                if self.engine.scenario == "wallet": 
                    self.show_popup("Found Wallet!", "You found a wallet with $500. What will you do?", [("Keep", self.scen_keep), ("Return", self.scen_ret)])
                elif self.engine.scenario == "job_offer":
                    job_offer_data = random.choice(list(JOBS.values()))
                    self.show_popup("Job Offer!", f"A local company offered you a job as a {job_offer_data['icon']} {job_offer_data['sal']:,}/year. Do you accept?", [("Accept", lambda: self.scen_accept_job(job_offer_data)), ("Decline", self.scen_decline_job)])
                self.engine.scenario = None # Clear scenario after handling

    def show_popup(self, title, text, opts):
        # Dismiss existing dialog if any before showing a new one
        if self._current_dialog and self._current_dialog.is_open:
            self._current_dialog.dismiss()

        btns = []
        for o_text, o_func in opts:
            # Wrap the function call to dismiss the dialog
            def _callback(f=o_func):
                if self._current_dialog:
                    self._current_dialog.dismiss()
                    self._current_dialog = None
                f()
                self.update() # Ensure UI updates after dialog action
            btns.append(MDRectangleFlatButton(text=o_text, on_release=_callback))
        
        if not btns: # If no buttons provided, add a dismiss button
            btns.append(MDRectangleFlatButton(text="OK", on_release=lambda x: self.dismiss_dialog_and_update()))

        self._current_dialog = MDDialog(title=title, text=text, buttons=btns, auto_dismiss=False)
        self._current_dialog.open()

    def dismiss_dialog_and_update(self):
        if self._current_dialog:
            self._current_dialog.dismiss()
            self._current_dialog = None
        self.update()

    # Scenario handlers
    def scen_keep(self): 
        self.engine.money += 500
        self.engine.adjust_stat("karma", -5)
        self.engine.log("Kept the wallet and its contents.", SPRITES['Money'])

    def scen_ret(self): 
        self.engine.adjust_stat("karma", 10)
        self.engine.adjust_stat("hap", 5)
        self.engine.log("Returned the wallet to its owner.", SPRITES['Karma'])

    def scen_accept_job(self, job_data):
        self.engine.career = next(name for name, data in JOBS.items() if data == job_data) # Find job name by its data
        self.engine.log(f"Accepted the job as a {self.engine.career}!", SPRITES['Job'])
        self.update()

    def scen_decline_job(self):
        self.engine.log("Declined the job offer.", SPRITES['Sad'])
        self.update()

    def menu(self, m): self.manager.current = m

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.dialog = None

    def on_enter(self):
        self.engine = self.app.engine
        self.build_ui()
    
    def back(self, *x): self.manager.current = 'game'

    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        layout.add_widget(MDLabel(text=self.name.upper(), font_style="H5", halign="center", size_hint_y=0.1))
        
        self.menu_rv = RecycleView(viewclass=SelectableTwoLineIconListItem)
        self.menu_rv_layout = RecycleBoxLayout(default_size=(None, dp(64)), default_size_hint=(1, None),
                                        orientation='vertical', size_hint_y=None, spacing=dp(2))
        self.menu_rv_layout.bind(minimum_height=self.menu_rv_layout.setter('height'))
        self.menu_rv.add_widget(self.menu_rv_layout)
        layout.add_widget(self.menu_rv)
        
        items_data = [] 
        if self.name == "job":
            if self.engine.career != "Unemployed":
                items_data.append({'text': f"Current: {self.engine.career}", 'secondary_text': f"Salary: ${JOBS[self.engine.career]['sal']:,}. Click to Quit.", 'icon': JOBS[self.engine.career]['icon'], 'callback': self.quit_job})
            items_data.append({'text': "--- Available Jobs ---", 'secondary_text': "", 'disabled': True})
            for t, d in JOBS.items():
                if t == self.engine.career: continue # Don't list current job again
                req_skills_str = ", ".join([f"{s} ({lvl})" for s, lvl in d['req_skills'].items()])
                if req_skills_str: req_skills_str = f"| Skills: {req_skills_str}"
                
                can_apply = self.engine.age >= d['req_age'] and self.engine.smrt >= d['req_smrt']
                
                # Check for required degree if applicable
                req_degree = d.get('req_degree')
                if req_degree and self.engine.education != req_degree:
                    can_apply = False
                    req_skills_str += f" | Req: {req_degree}"

                secondary_text = f"${d['sal']:,} | Age: {d['req_age']} | Smrt: {d['req_smrt']}% {req_skills_str}"
                items_data.append({'text': t, 'secondary_text': secondary_text, 'icon': d['icon'], 'callback': (lambda t=t: self.get_job(t)) if can_apply else None, 'disabled': not can_apply})
        
        elif self.name == "asset":
            if self.engine.assets:
                items_data.append({'text': "--- Your Assets ---", 'secondary_text': "", 'disabled': True})
                for i, a in enumerate(self.engine.assets):
                    items_data.append({'text': f"{a['name']} (${a['val']:,})", 'secondary_text': "Click to Sell", 'icon': SPRITES[a['type']], 'callback': lambda idx=i: self.sell_asset(idx)})
            items_data.append({'text': "--- Buy New Assets ---", 'secondary_text': "", 'disabled': True})
            for n, p, t, props in ASSETS:
                can_buy = self.engine.money >= p
                secondary_text = f"${p:,}"
                if t == 'House': secondary_text += f" | Upkeep: ${props.get('upkeep',0):,} | Apprec: {props.get('appreciation',0)*100:.0f}%"
                elif t == 'Car': secondary_text += f" | Upkeep: ${props.get('upkeep',0):,} | Deprec: {props.get('depreciation',0)*100:.0f}%"
                elif t in ['Stocks', 'Crypto']: secondary_text += f" | Volatility: {props.get('volatility',0)*100:.0f}%"

                items_data.append({'text': n, 'secondary_text': secondary_text, 'icon': SPRITES[t], 'callback': (lambda n=n,p=p,t=t,props=props:self.buy_asset(n,p,t,props)) if can_buy else None, 'disabled': not can_buy})
        
        elif self.name == "act":
            items_data.append({'text': "--- General Actions ---", 'secondary_text': "", 'disabled': True})
            opts = [
                ("Go to Doctor", self.doc, SPRITES['Doc'], "$100 - Boosts Health (+20 Hlt)", 100, "money"),
                ("Go to Gym", self.gym, SPRITES['Gym'], "$50 - Boosts Health & Looks (+5 Hlt, +5 Look)", 50, "money"),
                ("Study (Smarts)", self.study, SPRITES['Study'], "Boosts Smarts (+5 Smrt)", 0, None),
                ("Meditate (Stress)", self.meditate, SPRITES['Meditate'], "Reduces Stress (-10 Stress)", 0, None),
                ("Volunteer (Karma)", self.volunteer, SPRITES['Volunteer'], "Boosts Karma (+5 Karma)", 0, None),
                ("Attempt Crime", self.crime, SPRITES['Crime'], "High Risk - Money or Jail!", 0, None),
                ("Find Life Orb", self.discover_orb_action, SPRITES['LifeOrb'], "Discover a hidden Life Orb location.", 0, None)
            ]
            for t, f, icon, desc, cost, cost_type in opts:
                can_afford = True
                if cost_type == "money" and self.engine.money < cost: can_afford = False
                items_data.append({'text': t, 'secondary_text': desc, 'icon': icon, 'callback': f if can_afford else None, 'disabled': not can_afford})

            items_data.append({'text': "--- Education ---", 'secondary_text': "", 'disabled': True})
            if self.engine.current_education:
                items_data.append({'text': f"Currently studying: {self.engine.current_education['degree']}", 'secondary_text': f"{self.engine.education_years_left} years left. Cost: ${self.engine.current_education['cost']/self.engine.current_education['duration']:.0f}/year.", 'icon': SPRITES['Study'], 'disabled': True})
                items_data.append({'text': "Drop Out", 'secondary_text': "End current education program early.", 'icon': SPRITES['Layoff'], 'callback': self.drop_out_education})
            else:
                for t, d in EDUCATION_PROGRAMS.items():
                    can_enroll = self.engine.age >= d['min_age'] and self.engine.money >= d['cost']
                    if d.get('req_smrt') and self.engine.smrt < d['req_smrt']: can_enroll = False
                    if d.get('req_degree') and self.engine.education != d['req_degree']: can_enroll = False

                    secondary_text = f"Cost: ${d['cost']:,} | Duration: {d['duration']} yrs | Smarts gain: {d['smrt_gain']}"
                    if d.get('req_smrt'): secondary_text += f" | Req Smarts: {d['req_smrt']}%"
                    if d.get('req_degree'): secondary_text += f" | Req Degree: {d['req_degree']}"
                    
                    items_data.append({'text': t, 'secondary_text': secondary_text, 'icon': SPRITES['School'], 'callback': (lambda t=t: self.enroll_education(t)) if can_enroll else None, 'disabled': not can_enroll})

            items_data.append({'text': "--- Inventory (Life Orbs) ---", 'secondary_text': "", 'disabled': True})
            if not self.engine.inventory:
                items_data.append({'text': "No items in inventory.", 'secondary_text': "", 'disabled': True})
            else:
                for orb_type, count in self.engine.inventory.items():
                    if count > 0:
                        orb_data = LIFE_ORBS[orb_type]
                        items_data.append({'text': f"{orb_type} (x{count})", 'secondary_text': orb_data['description'], 'icon': orb_data['icon'], 'callback': (lambda ot=orb_type: self.use_orb_action(ot))})


        elif self.name == "rel":
            items_data.append({'text': "--- Your Family & Friends ---", 'secondary_text': "", 'disabled': True})
            if self.engine.married_to: 
                items_data.append({'text': f"{self.engine.married_to} (Spouse)", 'secondary_text': f"Relationship: {next(r['rel'] for r in self.engine.relations if r['name'] == self.engine.married_to)}%", 'icon': SPRITES['Love'], 'callback': (lambda r_name=self.engine.married_to: self.interact_rel({"name": r_name, "type": "Spouse"}))})
                items_data.append({'text': "Have a Child", 'secondary_text': "Start a family!", 'icon': SPRITES['Baby'], 'callback': self.have_child, 'disabled': self.engine.age < 18 or self.engine.age > 45})
            
            for r in self.engine.relations:
                if r['name'] == self.engine.married_to: continue # Already listed spouse
                if r['type'] == 'Partner': # Special action for potential partner
                    items_data.append({'text': f"{r['name']} (Partner)", 'secondary_text': f"Relationship: {r['rel']}% | Ask to marry?", 'icon': SPRITES['Love'], 'callback': (lambda r=r: self.propose_marriage(r))})
                else:
                    items_data.append({'text': f"{r['name']} ({r['type']})", 'secondary_text': f"Relationship: {r['rel']}% | Interact", 'icon': SPRITES['Love'], 'callback': lambda r=r: self.interact_rel(r)})
            
            if self.engine.children:
                items_data.append({'text': "--- Your Children ---", 'secondary_text': "", 'disabled': True})
                for child in self.engine.children:
                    items_data.append({'text': f"{child['name']} (Age: {child['age']})", 'secondary_text': "Show affection", 'icon': SPRITES['Child'], 'callback': lambda c=child: self.interact_child(c)})


        self.menu_rv.data = items_data
        layout.add_widget(MDFillRoundFlatButton(text="BACK", size_hint_y=0.08, on_release=self.back))
        self.add_widget(layout)

    # Job Actions
    def get_job(self, job_name): 
        self.engine.career = job_name
        self.engine.log(f"Hired as {job_name}!", SPRITES['Job'])
        self.back()

    def quit_job(self): 
        self.engine.career = "Unemployed"
        self.engine.log("Quit job.", SPRITES['Layoff'])
        self.back()
    
    # Asset Actions
    def buy_asset(self, n, p, t, props): 
        self.engine.money -= p
        self.engine.assets.append({"name": n, "val": p, "type": t, "props": props})
        self.engine.log(f"Bought {n}!", SPRITES['Money'])
        self.back()

    def sell_asset(self, idx): 
        a = self.engine.assets.pop(idx)
        self.engine.money += a['val']
        self.engine.log(f"Sold {a['name']} for ${a['val']:,}.", SPRITES['Money'])
        self.back()
    
    # General Actions
    def doc(self): 
        self.engine.money -= 100
        self.engine.adjust_stat("hlt", 20)
        self.engine.adjust_stat("stress", -5)
        self.engine.log("Visited Doctor. Feeling better!", SPRITES['Doc'])
        self.back()

    def gym(self): 
        self.engine.money -= 50
        self.engine.adjust_stat("hlt", 5)
        self.engine.adjust_stat("look", 5)
        self.engine.adjust_stat("energy", -10)
        self.engine.log("Had a good workout at the gym.", SPRITES['Gym'])
        self.back()
    
    def study(self):
        self.engine.adjust_stat("smrt", 5)
        self.engine.adjust_stat("energy", -5)
        self.engine.adjust_stat("stress", 3)
        self.engine.log("Spent time studying.", SPRITES['Study'])
        self.back()

    def meditate(self):
        self.engine.adjust_stat("stress", -10)
        self.engine.adjust_stat("hap", 5)
        self.engine.adjust_stat("energy", 5)
        self.engine.log("Meditated for a while. Feeling peaceful.", SPRITES['Meditate'])
        self.back()

    def volunteer(self):
        self.engine.adjust_stat("karma", 5)
        self.engine.adjust_stat("hap", 10)
        self.engine.adjust_stat("energy", -5)
        self.engine.log("Volunteered for a good cause.", SPRITES['Volunteer'])
        self.back()

    def crime(self):
        self.engine.adjust_stat("karma", -random.randint(5, 15))
        self.engine.adjust_stat("stress", random.randint(10, 20))
        if random.random() > 0.6: # 40% chance of success
            profit = random.randint(500, 5000)
            self.engine.money += profit
            self.engine.log(f"Successfully committed a crime and gained ${profit:,}!", SPRITES['Crime'])
        else: # 60% chance of failure/arrest
            jail_time = random.randint(1, 5)
            self.engine.jail = jail_time
            self.engine.log(f"Caught! Sentenced to {jail_time} years in jail.", SPRITES['Jail'])
        self.back()

    def discover_orb_action(self):
        self.engine.discover_life_orb()
        self.back()

    def use_orb_action(self, orb_type):
        self.engine.use_life_orb(orb_type)
        self.back()

    # Education Actions
    def enroll_education(self, program_name):
        program_data = EDUCATION_PROGRAMS[program_name]
        self.engine.current_education = program_data
        self.engine.education_years_left = program_data['duration']
        self.engine.money -= program_data['cost'] / program_data['duration'] # Pay first year upfront
        self.engine.log(f"Enrolled in {program_name}.", SPRITES['School'])
        self.back()
    
    def drop_out_education(self):
        self.engine.current_education = None
        self.engine.education_years_left = 0
        self.engine.adjust_stat("smrt", -5) # Small penalty for dropping out
        self.engine.log("Dropped out of education.", SPRITES['Sad'])
        self.back()

    # Relationship Actions
    def propose_marriage(self, partner_data):
        if self.engine.age < 18:
            self.engine.log("Too young to get married!", SPRITES['Sad'])
            return
        
        partner_rel = next(r['rel'] for r in self.engine.relations if r['name'] == partner_data['name'])
        if partner_rel >= 70 and random.random() < (partner_rel / 100): # Higher relationship, higher chance
            self.engine.married_to = partner_data['name']
            for r in self.engine.relations:
                if r['name'] == partner_data['name']:
                    r['type'] = 'Spouse'
                    break
            self.engine.adjust_stat("hap", 20)
            self.engine.adjust_stat("stress", -10)
            self.engine.log(f"Married {partner_data['name']}! ❤️", SPRITES['Marriage'])
        else:
            self.engine.adjust_stat("hap", -15)
            self.engine.adjust_stat("stress", 10)
            self.engine.log(f"Proposal rejected by {partner_data['name']} 💔. Relationship took a hit.", SPRITES['Sad'])
            for r in self.engine.relations:
                if r['name'] == partner_data['name']:
                    r['rel'] = max(0, r['rel'] - 20)
                    break
        self.back()

    def have_child(self): 
        if self.engine.married_to:
            child_name = random.choice(['Mia', 'Zoe', 'Leo', 'Max', 'Sam', 'Ella'])
            self.engine.children.append({"name": child_name, "age": 0})
            self.engine.relations.append({"name": child_name, "rel": 100, "type": "Child"})
            self.engine.adjust_stat("money", -1000, allow_below_min=True) # Initial cost of raising a child
            self.engine.adjust_stat("hap", 15)
            self.engine.adjust_stat("stress", 10)
            self.engine.log(f"Had a baby named {child_name}!", SPRITES['Child'])
        else:
            self.engine.log("You need to be married to have a child!", SPRITES['Sad'])
        self.back()

    def interact_rel(self, r_data): 
        # For general interaction with family/spouse
        r = next(item for item in self.engine.relations if item['name'] == r_data['name'])
        r['rel'] = min(100, r['rel'] + random.randint(5, 15))
        self.engine.adjust_stat("hap", 5)
        self.engine.adjust_stat("stress", -3)
        self.engine.log(f"Spent time with {r_data['name']}. Relationship improved.", SPRITES['Love'])
        self.back()

    def interact_child(self, child_data):
        child_rel = next(r for r in self.engine.relations if r['name'] == child_data['name'])
        child_rel['rel'] = min(100, child_rel['rel'] + random.randint(10, 20))
        self.engine.adjust_stat("hap", 5)
        self.engine.log(f"Played with {child_data['name']}. Good times!", SPRITES['Child'])
        self.back()


class Year3000App(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        self.engine = SimEngine()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(CharacterCreationScreen(name='char_create'))
        sm.add_widget(GameScreen(name='game'))
        for m in ['job', 'asset', 'act', 'rel']: sm.add_widget(MenuScreen(name=m))
        return sm

if __name__ == "__main__":
    Year3000App().run()