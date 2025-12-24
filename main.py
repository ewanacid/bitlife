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
from kivy.uix.scrollview import ScrollView
import random

# Elite Configuration: Enforcing modern, high-contrast palette and mobile responsiveness
# Window.size = (400, 700) # Only for desktop debugging
Window.clearcolor = get_color_from_hex('#F0F0F0')

# --- Screen Definitions ---
class StartScreen(Screen):
    """The main entry point/menu screen. High contrast, focused UX."""
    pass

class GameScreen(Screen):
    """The core simulation screen displaying stats, log, and actions."""
    pass

class DeathScreen(Screen):
    """Displayed upon game termination, providing a detailed summary."""
    pass

# --- Custom Widget Styling (Kivy Language Definition Block) ---

KV = """
# Define robust, reusable visual components for mobile touch targets

<LifeButton@Button>:
    # Modern, elevated flat design
    background_normal: ''
    background_down: ''
    background_color: 0.1, 0.45, 0.75, 1 # Primary Blue
    color: 1, 1, 1, 1 
    font_size: '18sp'
    size_hint_y: None
    height: dp(60) # Generous height for reliable touch input
    padding: dp(15), dp(10)
    # Custom shading for visual feedback
    canvas.before:
        Color:
            # Darker shade when pressed
            rgba: (self.background_color[0]*0.7, self.background_color[1]*0.7, self.background_color[2]*0.7, 1) if self.state == 'down' else self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]
            
<AgeButton@LifeButton>:
    background_color: 0.8, 0.2, 0.2, 1 # Critical Action Red

<StatLabel@Label>:
    color: 0.1, 0.1, 0.1, 1
    font_size: '17sp'
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
        spacing: dp(35)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#F0F0F0') # Light background for clean start
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: '[b]MORTALIS[/b]'
            markup: True
            color: 0.1, 0.1, 0.1, 1
            font_size: '56sp'
            size_hint_y: 0.35
            padding_y: dp(15)
        
        Label:
            text: 'A high-stakes simulation of life, optimized for mobile performance.'
            color: 0.4, 0.4, 0.4, 1
            font_size: '20sp'
            size_hint_y: 0.15
            text_size: self.width, None

        BoxLayout:
            orientation: 'vertical'
            spacing: dp(20)
            padding: dp(10)
            size_hint_y: 0.4

            LifeButton:
                text: 'START NEW LIFE'
                background_color: 0.1, 0.6, 0.1, 1 # Green Start Button
                on_release: app.start_new_life()
            
            LifeButton:
                text: 'EXIT GAME'
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

        # 1. STATUS STATS (HUD - Always visible, top priority)
        GridLayout:
            cols: 4
            size_hint_y: 0.12
            padding: dp(8)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: 0.97, 0.97, 0.97, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(12),]
                    
            StatLabel:
                text: f'[b]AGE[/b]\\n{int(app.age)}'
                markup: True
                color: 0.1, 0.1, 0.1, 1
            StatLabel:
                text: f'[b]HLTH[/b]\\n[color={app.get_health_color()}]{int(app.health)}%[/color]'
                markup: True
            StatLabel:
                text: f'[b]HPNS[/b]\\n[color={app.get_happiness_color()}]{int(app.happiness)}%[/color]'
                markup: True
            StatLabel:
                text: f'[b]WLT[/b]\\n[color=0055AA]${app.money:,.0f}[/color]'
                markup: True

        # 2. LOG/EVENT FEED (Scrollable, ensures performance stability)
        ScrollView:
            size_hint_y: 0.5
            effect_cls: 'ScrollEffect' 
            bar_width: dp(4) # Slim scrollbar for clean mobile look
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
                size_hint_y: None 
                height: self.texture_size[1] # Automatically adjusts height for content
                text_size: self.width * 0.95, None # 5% margin padding

        # 3. ACTIONS
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: 0.25

            Label:
                text: '[b]YEARLY FOCUS[/b]'
                markup: True
                color: 0.2, 0.2, 0.2, 1
                font_size: '18sp'
                size_hint_y: None
                height: dp(30)

            GridLayout:
                cols: 3
                spacing: dp(12)
                LifeButton:
                    text: 'STUDY\\n(+INT)'
                    background_color: 0.1, 0.5, 0.1, 1
                    on_release: app.perform_action('study')
                LifeButton:
                    text: 'WORK\\n(+$$)'
                    background_color: 0.65, 0.45, 0.15, 1
                    on_release: app.perform_action('work')
                LifeButton:
                    text: 'EXERCISE\\n(+HLTH)'
                    background_color: 0.7, 0.2, 0.4, 1
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
        spacing: dp(30)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#151515') # Dark, solemn background
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: '[color=E53935][b]MORTALITY REACHED[/b][/color]'
            markup: True
            color: 1, 1, 1, 1
            font_size: '50sp'
            size_hint_y: 0.2
        
        Label:
            id: death_summary
            text: app.death_message
            markup: True
            color: 0.9, 0.9, 0.9, 1
            font_size: '19sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width * 0.9, None
            size_hint_y: 0.55

        LifeButton:
            text: 'REBIRTH (Main Menu)'
            background_color: 0.4, 0.4, 0.4, 1
            on_release: app.root.current = 'start_screen'
"""

class LifeSimulatorApp(App):
    # Core Game State Properties (Optimized for Kivy binding)
    age = NumericProperty(0)
    health = NumericProperty(100.0)
    happiness = NumericProperty(50.0)
    money = NumericProperty(1000.0)
    intelligence = NumericProperty(50.0)

    # UI/Log Properties
    game_log = StringProperty("A new life begins...")
    death_message = StringProperty("")
    
    # Event Data structure: Static but extensible definition
    RANDOM_EVENTS = {
        'positive': [
            ("You received an unexpected bonus of $1,500!", lambda app: app._update_stats(money=1500, happiness=5)),
            ("An intense intellectual pursuit improved your focus.", lambda app: app._update_stats(intelligence=4, happiness=5)),
            ("Achieving a major personal milestone provided deep satisfaction.", lambda app: app._update_stats(happiness=15, health=2)),
            ("A vacation revitalized you. Health and Happiness restored.", lambda app: app._update_stats(health=10, happiness=10, money=-500)),
        ],
        'negative': [
            ("A bad investment caused a significant financial loss ($750).", lambda app: app._update_stats(money=-750, happiness=-8)),
            ("Chronic stress leads to burnout and reduced vitality.", lambda app: app._update_stats(health=-12, happiness=-5)),
            ("A public failure causes severe emotional trauma.", lambda app: app._update_stats(happiness=-15)),
            ("Serious illness requires expensive treatment. Health -15, Money -1200.", lambda app: app._update_stats(health=-15, money=-1200)),
        ],
        'milestones': [
            (6, "Formal schooling begins. Your intellect blossoms.", lambda app: app._update_stats(intelligence=8, happiness=5)),
            (18, "You gained legal independence. New responsibilities await.", lambda app: app._update_stats(money=100, intelligence=2)),
            (25, "You established a stable career foundation.", lambda app: app._update_stats(money=2000)),
            (50, "Half a century! Reflecting on your wisdom.", lambda app: app._update_stats(happiness=5, intelligence=3)),
        ],
    }
    
    # --- Utility Methods for Dynamic UX ---
    
    def get_health_color(self):
        """Returns hex color code based on health level for dynamic HUD signaling."""
        if self.health >= 75: return '4CAF50'  # Green (Healthy)
        if self.health >= 40: return 'FF9800'  # Orange (Warning)
        return 'F44336'                       # Red (Critical)
        
    def get_happiness_color(self):
        """Returns hex color code based on happiness level for dynamic HUD signaling."""
        if self.happiness >= 65: return '2196F3' # Blue (Happy)
        if self.happiness >= 30: return 'FFC107' # Yellow (Neutral/Stressed)
        return 'E53935'                          # Dark Red (Depressed)
        
    # --- Kivy App Lifecycle ---

    def build(self):
        self.title = 'MORTALIS: Life Simulator'
        return Builder.load_string(KV)

    # --- Game State Management ---

    def _update_stats(self, money=0, health=0, happiness=0, intelligence=0):
        """Safely updates stats, ensuring properties remain within realistic, crash-free bounds."""
        
        new_money = self.money + money
        new_health = self.health + health
        new_happiness = self.happiness + happiness
        new_intelligence = self.intelligence + intelligence

        # Money must not be negative (debt is abstracted or results in immediate consequence elsewhere)
        self.money = float(max(0.0, new_money))
        
        # Health must stay above 0 for a living character, but 1.0 is the effective 'near death' limit.
        self.health = float(max(0.0, min(100.0, new_health))) 
        self.happiness = float(max(0.0, min(100.0, new_happiness)))
        self.intelligence = float(max(1.0, min(100.0, new_intelligence)))

    def log_event(self, message):
        """Formats and prepends a new event message to the log, applying color coding."""
        
        color = '333333' # Default Neutral
        
        # Color coding for immediate feedback
        if '[b]MILESTONE' in message or 'Gained' in message or 'improved' in message:
            color = '2E7D32' # Dark Green (Success)
        elif 'lost' in message or 'failure' in message or 'stress' in message:
            color = 'D32F2F' # Dark Red (Failure)
        elif 'Age' in message:
            color = '444444' # Grey (Routine)

        new_entry = f'[color={color}][b]Age {int(self.age)}:[/b] {message}[/color]\n'
        
        # Efficiently manage log history to prevent UI slowdown over long sessions
        log_lines = self.game_log.split('\n')
        self.game_log = new_entry + '\n'.join(log_lines[:20]) # Keep max 20 entries

    def start_new_life(self):
        """Initializes game state and transitions to the game screen."""
        self.age = 0
        self.health = float(random.randint(85, 100))
        self.happiness = float(random.randint(60, 80))
        self.money = float(random.randint(1500, 5000))
        self.intelligence = float(random.randint(60, 80))
        self.game_log = "Year 0: You are born, starting a clean slate. Focus on Health, Wealth, and Wisdom."
        self.root.current = 'game_screen'

    # --- Core Game Loop Functions ---
    
    def age_up(self):
        """The mandatory yearly life cycle tick, handling decay, events, and mortality."""
        
        # Ensure the user cannot age up if they are already dead (edge case protection)
        if self.check_death(suppress_log=True): return 

        self.age += 1
        
        # 1. Mandatory Annual Decay & Costs
        
        health_decay = 1.0
        intel_decay = 0.0
        
        # Decay scaling based on age for realism
        if self.age > 40:
            health_decay += (self.age - 40) * 0.15
            intel_decay = (self.age - 40) * 0.08 # Intelligence decay begins
        if self.age > 70:
            health_decay += (self.age - 70) * 0.4
            
        # Cost of living (abstracted expenses, slightly higher during peak adult years)
        base_cost = 500
        age_factor = max(0.5, 1.0 - abs(self.age - 35) / 50)
        cost_of_living = base_cost * age_factor
        
        self._update_stats(
            health=-health_decay, 
            happiness=-1.0, 
            money=-cost_of_living,
            intelligence=-intel_decay
        )
        
        # 2. Trigger Events
        self.trigger_events()

        # 3. Final Death Check
        self.check_death()

        if self.root.current == 'game_screen':
            self.log_event(f"You turned {int(self.age)}. Annual upkeep cost: ${cost_of_living:,.0f}.")


    def trigger_events(self):
        """Handles special milestone and random occurrences."""
        
        # Check Milestone Events
        for age_key, message, effect in self.RANDOM_EVENTS['milestones']:
            if self.age == age_key:
                effect(self)
                self.log_event(f"[b]MILESTONE:[/b] {message}")
                return 

        # General Random Events (18% chance)
        event_chance = 0.18
        
        if random.random() < event_chance:
            # Weighted random choice based on current state (low stats -> higher chance of negative events)
            weight_positive = 70 if (self.health > 40 and self.happiness > 40) else 30
            weight_negative = 100 - weight_positive
                
            event_type = random.choices(['positive', 'negative'], weights=[weight_positive, weight_negative], k=1)[0]
                
            events = self.RANDOM_EVENTS[event_type]
            message, effect = random.choice(events)
            
            effect(self)
            self.log_event(f"EVENT: {message}")

    def perform_action(self, action_type):
        """Handles explicit player actions with nuanced outcomes based on current stats."""
        if self.check_death(): return

        if action_type == 'study':
            if self.age < 5:
                self.log_event("You are too young for focused study.")
                return
            if self.age > 85:
                self.log_event("Advanced age severely limits mental retention.")
                return

            # Diminishing returns the smarter you get
            int_gain = max(1, random.randint(3, 8) - int(self.intelligence / 18))
            self.intelligence = min(100.0, self.intelligence + int_gain)
            self._update_stats(happiness=-6, health=-2) # Study is taxing
            self.log_event(f"Focused learning session. Intelligence Gained +{int_gain}%.")

        elif action_type == 'work':
            if self.age < 18:
                self.log_event("Child labor laws prohibit this action.")
                return
            if self.age > 75:
                 self.log_event("You are likely retired and should conserve energy.")
                 return

            # Income is strongly tied to Intelligence (representing career status)
            base_income = 1500 
            income_multiplier = 0.7 + (self.intelligence / 50)
            money_gain = int(base_income * income_multiplier)
            
            self._update_stats(money=money_gain, health=-7, happiness=-3) # Work is stressful
            self.log_event(f"Productive year of work. Gained ${money_gain:,.0f}.")

        elif action_type == 'exercise':
            health_gain = random.randint(8, 18)
            # Health gain is penalized if health is already high (max 100) or if age is very high
            age_penalty = max(0, (self.age - 60) / 10)
            final_health_gain = max(1, health_gain - age_penalty)
            
            self._update_stats(health=final_health_gain, happiness=10) # Exercise boosts mood
            self.log_event(f"A rigorous workout paid off. Health Gained +{int(final_health_gain)}%, Happiness +10%.")

    def check_death(self, suppress_log=False):
        """Determines if the character has died and executes the mortality sequence."""
        reason = None
        
        # 1. Critical Failure Check
        if self.health <= 0.0:
            reason = "A catastrophic health failure or injury terminated your existence."
        elif self.happiness <= 0.0:
            reason = "The complete lack of purpose led to a final loss of the will to live."
        elif self.money <= 0.0 and self.age > 18 and random.random() < 0.1:
            reason = "Severe, prolonged poverty resulted in destitution and subsequent failure to thrive."

        # 2. Old Age Mortality Curve
        if self.age > 70:
            base_survival_rate = 1.0 - ((self.age - 70) / 80.0) # Rate drops faster after 70
            
            # Survival is heavily modified by current health/happiness
            survival_modifier = (self.health / 100.0) * (self.happiness / 100.0)
            final_chance = base_survival_rate * survival_modifier
            
            if random.random() > final_chance:
                reason = "You succumbed to the inevitable decline of advanced age."
        
        # 3. Absolute Mortality Cap
        if self.age > 125:
             reason = "A true centenarian, you reached the absolute limit of human lifespan."


        if reason and not suppress_log:
            # Generate final summary report
            summary = (
                f"Your life concluded at the venerable age of [b]{int(self.age)}[/b] years.\n\n"
                f"[color=E53935][b]CAUSE OF DEATH:[/b][/color] {reason}\n\n"
                f"[b]FINAL STATS SUMMARY[/b]\n"
                f"Peak Intelligence: {int(self.intelligence)}/100\n"
                f"Remaining Wealth: [color=4CAF50]${self.money:,.0f}[/color]\n"
                f"Total Years Lived: {int(self.age)}"
            )
                
            self.death_message = summary
            
            if self.root.current != 'death_screen':
                self.root.current = 'death_screen'
            return True
        
        return False


if __name__ == '__main__':
    LifeSimulatorApp().run()