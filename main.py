from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty, DictProperty
from kivy.core.window import Window
import random

# Ensure mobile-friendly sizing for development/Buildozer targets
# Window.size = (400, 700) # Optional for PC testing, commented for true mobile layout reliance

# --- Screen Definitions ---
class StartScreen(Screen):
    """The main entry point/menu screen."""
    pass

class GameScreen(Screen):
    """The core simulation screen displaying stats, log, and actions."""
    pass

class DeathScreen(Screen):
    """Displayed upon game termination."""
    pass

# --- Custom Widget Styling ---

KV = """
# Define robust, reusable visual components
<LifeButton@Button>:
    # Modern flat design
    background_normal: ''
    background_down: 'atlas://data/images/defaulttheme/button_pressed'
    background_color: 0.05, 0.35, 0.65, 1 # Deep Blue/Teal
    color: 1, 1, 1, 1 
    font_size: '18sp'
    size_hint_y: None
    height: dp(55)
    padding: dp(15), dp(10)
    canvas.before:
        Color:
            rgba: self.background_color if self.state == 'normal' else (self.background_color[0]*0.8, self.background_color[1]*0.8, self.background_color[2]*0.8, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12),]

<AgeButton@LifeButton>:
    background_color: 0.8, 0.2, 0.2, 1 # Critical Action Red

<StatLabel@Label>:
    color: 0.1, 0.1, 0.1, 1
    font_size: '16sp'
    bold: True
    valign: 'middle'
    halign: 'center'
    text_size: self.width, self.height

# --- Screen Manager & Layouts ---

ScreenManager:
    StartScreen:
        name: 'start_screen'
    GameScreen:
        name: 'game_screen'
    DeathScreen:
        name: 'death_screen'

<StartScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(25)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#F8F8F8') # Light background for clean start
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: 'LIFE SIMULATOR'
            color: 0.1, 0.1, 0.1, 1
            font_size: '52sp'
            bold: True
            size_hint_y: 0.35
        
        Label:
            text: 'A lifetime of choices, one year at a time.'
            color: 0.4, 0.4, 0.4, 1
            font_size: '22sp'
            size_hint_y: 0.15

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(15)
            padding: dp(10)
            size_hint_y: 0.4

            LifeButton:
                text: 'START NEW LIFE'
                on_release: app.start_new_life()
            
            LifeButton:
                text: 'QUIT'
                background_color: 0.5, 0.5, 0.5, 1
                on_release: app.stop()

<GameScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#FFFFFF') 
            Rectangle:
                pos: self.pos
                size: self.size

        # 1. STATUS STATS (HUD)
        GridLayout:
            cols: 4
            size_hint_y: 0.12
            padding: dp(5)
            spacing: dp(5)
            canvas.before:
                Color:
                    rgba: 0.95, 0.95, 0.95, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10),]

            StatLabel:
                text: f'[b]AGE:[/b] {int(app.age)}'
                markup: True
            StatLabel:
                text: f'[b]HLTH:[/b] [color={app.get_health_color()}]{int(app.health)}%[/color]'
                markup: True
            StatLabel:
                text: f'[b]HPNS:[/b] [color={app.get_happiness_color()}]{int(app.happiness)}%[/color]'
                markup: True
            StatLabel:
                text: f'[b]WLT:[/b] [color=0055AA]${app.money:,.0f}[/color]'
                markup: True
        
        # 2. LOG/EVENT FEED
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.5
            padding: dp(8)
            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10),]

            Label:
                id: life_log
                text: app.game_log
                markup: True
                font_size: '15sp'
                halign: 'left'
                valign: 'top'
                color: 0, 0, 0, 1
                text_size: self.width, None
        
        # 3. ACTIONS
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(8)
            size_hint_y: 0.25

            Label:
                text: '[b]LIFE CHOICES[/b]'
                color: 0.2, 0.2, 0.2, 1
                font_size: '18sp'
                size_hint_y: None
                height: dp(30)

            GridLayout:
                cols: 3
                spacing: dp(10)
                LifeButton:
                    text: 'STUDY (+INT)'
                    background_color: 0.1, 0.5, 0.1, 1 # Green
                    on_release: app.perform_action('study')
                LifeButton:
                    text: 'WORK (+$$)'
                    background_color: 0.6, 0.4, 0.1, 1 # Gold/Brown
                    on_release: app.perform_action('work')
                LifeButton:
                    text: 'EXERCISE (+HLTH)'
                    background_color: 0.8, 0.3, 0.5, 1 # Pink/Purple
                    on_release: app.perform_action('exercise')

        # 4. AGE LOOP BUTTON
        AgeButton:
            text: f'LIVE ANOTHER YEAR (Age {int(app.age)})'
            size_hint_y: 0.1
            on_release: app.age_up()

<DeathScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(25)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#151515') # Dark, solemn background
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: '[color=FF3333][b]MORTALITY[/b][/color]'
            markup: True
            color: 1, 1, 1, 1
            font_size: '56sp'
            size_hint_y: 0.2
        
        Label:
            id: death_summary
            text: app.death_message
            markup: True
            color: 0.9, 0.9, 0.9, 1
            font_size: '20sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width * 0.9, None
            size_hint_y: 0.5

        LifeButton:
            text: 'RETURN TO MAIN MENU'
            background_color: 0.4, 0.4, 0.4, 1
            on_release: app.root.current = 'start_screen'
"""

class LifeSimulatorApp(App):
    # Core Game State Properties
    age = NumericProperty(0)
    health = NumericProperty(100.0)
    happiness = NumericProperty(50.0)
    money = NumericProperty(1000.0)
    intelligence = NumericProperty(50.0)

    # UI/Log Properties
    game_log = StringProperty("A new life begins...")
    death_message = StringProperty("")
    
    # Event Data structure (Using DictProperty for potential dynamic updates, though static here)
    RANDOM_EVENTS = {
        'positive': [
            ("Financial windfall: You received an unexpected bonus of $1,500!", lambda app: app._update_stats(money=1500, happiness=5)),
            ("You met an inspirational mentor. Intelligence improved.", lambda app: app._update_stats(intelligence=3, happiness=5)),
            ("Deep satisfaction: You achieved a major personal goal.", lambda app: app._update_stats(happiness=15, health=2)),
            ("A healthy diet pays off. Your vitality improved!", lambda app: app._update_stats(health=10)),
        ],
        'negative': [
            ("Misfortune strikes: You lost $750 in a bad investment.", lambda app: app._update_stats(money=-750, happiness=-8)),
            ("Stressful period: Chronic lack of sleep lowers health.", lambda app: app._update_stats(health=-12, happiness=-5)),
            ("A moment of public embarrassment shatters your ego.", lambda app: app._update_stats(happiness=-15)),
            ("Minor illness requires medicine: Health -8, Money -150.", lambda app: app._update_stats(health=-8, money=-150)),
        ],
        'milestones': [
            (6, "You started school. The world of knowledge opens up!", lambda app: app._update_stats(intelligence=8, happiness=5)),
            (16, "You mastered a new skill.", lambda app: app._update_stats(intelligence=5, happiness=10)),
            (25, "You secured a steady, full-time career position.", lambda app: app._update_stats(money=2000)),
            (50, "Half a century! You reflect on your accomplishments.", lambda app: app._update_stats(happiness=5)),
        ],
    }
    
    # --- Utility Methods for UX ---
    
    def get_health_color(self):
        """Returns hex color code based on health level for dynamic HUD."""
        if self.health >= 80: return '00AA00'  # Green
        if self.health >= 50: return 'FFAA00'  # Orange
        return 'FF0000'                       # Red
        
    def get_happiness_color(self):
        """Returns hex color code based on happiness level for dynamic HUD."""
        if self.happiness >= 70: return '0000AA' # Blue
        if self.happiness >= 40: return 'AAAA00' # Yellow/Gold
        return 'AA0000'                         # Dark Red
        
    # --- Kivy App Lifecycle ---

    def build(self):
        self.title = 'Life Simulator: Elite Edition'
        Window.clearcolor = get_color_from_hex('#FFFFFF')
        return Builder.load_string(KV)

    # --- Game State Management ---

    def _update_stats(self, money=0, health=0, happiness=0, intelligence=0):
        """Safely updates stats, ensuring properties remain within realistic bounds (0-100)."""
        
        # Apply changes
        new_money = self.money + money
        new_health = self.health + health
        new_happiness = self.happiness + happiness
        new_intelligence = self.intelligence + intelligence

        # Enforce bounds
        self.money = float(max(0, new_money))
        self.health = float(max(1.0, min(100.0, new_health))) # Health must stay above 1 to differentiate death by health=0
        self.happiness = float(max(0.0, min(100.0, new_happiness)))
        self.intelligence = float(max(1.0, min(100.0, new_intelligence)))

    def log_event(self, message):
        """Formats and prepends a new event message to the log."""
        
        color = '333333' # Default Neutral
        if 'MILESTONE' in message:
            color = '0055AA' # Blue for Milestones
        elif 'Gained' in message or '+' in message or 'improved' in message:
            color = '008800' # Green for Gains
        elif 'lost' in message or '-' in message or 'injury' in message or 'Stressful' in message:
            color = 'AA0000' # Red for Losses

        new_entry = f'[color={color}][b]Age {int(self.age)}:[/b] {message}[/color]\n'
        
        # Trim log to prevent performance degradation on older devices
        log_lines = self.game_log.split('\n')
        self.game_log = new_entry + '\n'.join(log_lines[:14])

    def start_new_life(self):
        """Resets all stats for a new game."""
        self.age = 0
        self.health = float(random.randint(80, 100))
        self.happiness = float(random.randint(50, 70))
        self.money = float(random.randint(800, 3000))
        self.intelligence = float(random.randint(50, 70))
        self.game_log = "You are born! The infinite possibilities await."
        self.root.current = 'game_screen'

    # --- Core Game Loop Functions ---
    
    def age_up(self):
        """The primary game tick: processes yearly changes, decay, and checks for death."""
        
        # Pre-age check (if player clicked 'Age Up' when already dead)
        if self.check_death(suppress_log=True): return 

        self.age += 1
        
        # 1. Mandatory Annual Decay & Costs
        
        # Decay increases sharply after 60, moderately after 30
        health_decay = 1.0
        if self.age > 30:
            health_decay += (self.age - 30) * 0.1
        if self.age > 60:
            health_decay += (self.age - 60) * 0.3
            
        # Basic cost of living (adjusted by age)
        cost_of_living = 200 + (self.age * 5)
        
        self._update_stats(
            health=-health_decay, 
            happiness=-1.0, # Slight boredom decay
            money=-cost_of_living
        )
        
        # 2. Trigger Events
        self.trigger_events()

        # 3. Final Death Check
        self.check_death()

        if self.root.current == 'game_screen':
            self.log_event(f"You turned {int(self.age)}. Annual upkeep cost: ${cost_of_living:,.0f}.")


    def trigger_events(self):
        """Handles special events and random occurrences."""
        
        # Check Milestone Events (always prioritized)
        for age_key, message, effect in self.RANDOM_EVENTS['milestones']:
            if self.age == age_key:
                effect(self)
                self.log_event(f"[b]MILESTONE:[/b] {message}")
                return 

        # General Random Events
        event_chance = 0.15 # 15% chance of event per year
        
        if random.random() < event_chance:
            # Favor negative events if happiness/health is low
            if self.health < 50 or self.happiness < 30:
                event_type = random.choices(['positive', 'negative'], weights=[20, 80], k=1)[0]
            else:
                event_type = random.choice(['positive', 'negative'])
                
            events = self.RANDOM_EVENTS[event_type]
            message, effect = random.choice(events)
            
            effect(self)
            self.log_event(f"EVENT: {message}")

    def perform_action(self, action_type):
        """Handles explicit player actions."""
        if self.check_death(): return

        if action_type == 'study':
            if self.age < 5 or self.age > 80:
                self.log_event("You cannot focus on formal study effectively right now.")
                return

            int_gain = max(1, random.randint(3, 8) - int(self.intelligence / 20)) # Diminishing returns on high INT
            self.intelligence = min(100.0, self.intelligence + int_gain)
            self._update_stats(happiness=-5, health=-1)
            self.log_event(f"You dedicated time to learning. Intelligence Gained +{int_gain}%.")

        elif action_type == 'work':
            if self.age < 18:
                self.log_event("You must be an adult to work legally.")
                return

            # Income highly dependent on Intelligence
            base_income = 800 
            # Multiplier: 1.0 (low INT) up to 2.5 (high INT)
            income_multiplier = 0.5 + (self.intelligence / 40)
            money_gain = int(base_income * income_multiplier)
            
            self._update_stats(money=money_gain, health=-5, happiness=-2) # Work is stressful
            self.log_event(f"You put in a solid effort at work. Gained ${money_gain:,.0f}.")

        elif action_type == 'exercise':
            health_gain = random.randint(6, 15)
            self._update_stats(health=health_gain, happiness=8)
            self.log_event(f"A rigorous workout improved your stamina. Health Gained +{health_gain}%, Happiness +8%.")

    def check_death(self, suppress_log=False):
        """Determines if the character has died and handles transition to DeathScreen."""
        reason = None
        
        # Critical failure (Health/Happiness)
        if self.health <= 1.0:
            reason = "Your health deteriorated completely due to neglect or chronic disease."
        elif self.happiness <= 0.0:
            reason = "A deep depression or tragedy led to an ultimate loss of will to live."

        # Old Age Check
        base_survival_chance = 1.0
        if self.age > 75:
            # Survival chance decreases exponentially after 75
            base_survival_chance = 1.0 - ((self.age - 75) / 50.0)
            
            # Health/Happiness drastically affect late-life survival
            survival_modifier = (self.health / 100.0) * (self.happiness / 100.0)
            
            final_chance = base_survival_chance * survival_modifier
            
            if random.random() > final_chance:
                reason = "You passed away peacefully of old age, having run the course of your life."
        
        # Ultra long life cap
        if self.age > 120:
             reason = "You defied all odds and lived to be an absolute centenarian."


        if reason and not suppress_log:
            # Construct a comprehensive final summary
            summary = (
                f"Your journey concluded at the age of [b]{int(self.age)}[/b].\n\n"
                f"Reason for death: {reason}\n\n"
                f"[b]LIFE SUMMARY[/b]\n"
                f"Final Wealth: [color=00AA00]${self.money:,.0f}[/color]\n"
                f"Max Intelligence: {int(self.intelligence)}%\n"
                f"Total Years Lived: {int(self.age)}"
            )
                
            self.death_message = summary
            
            if self.root.current != 'death_screen':
                self.root.current = 'death_screen'
            return True
        
        return False


if __name__ == '__main__':
    LifeSimulatorApp().run()