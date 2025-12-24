from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty
import random

# --- Screen Definitions ---
class StartScreen(Screen): pass
class GameScreen(Screen): pass
class DeathScreen(Screen): pass

# --- KV Setup ---
KV = """
# Define consistent styling for a clean, modern look 
<LifeButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0.1, 0.4, 0.7, 1 # Blue
    color: 1, 1, 1, 1 
    font_size: '18sp'
    size_hint_y: None
    height: dp(50)
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]

<AgeButton@LifeButton>:
    background_color: 0.7, 0.1, 0.1, 1 # Red for critical action

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
        padding: dp(50)
        spacing: dp(30)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#F0F0F0') 
            Rectangle:
                pos: self.pos
                size: self.size
        
        Label:
            text: 'BITLIFE CLONE'
            color: 0.1, 0.1, 0.1, 1
            font_size: '48sp'
            size_hint_y: 0.4
        
        Label:
            text: 'The choices you make define your destiny.'
            color: 0.3, 0.3, 0.3, 1
            font_size: '24sp'
            size_hint_y: 0.2

        LifeButton:
            text: 'START NEW LIFE'
            on_release: app.start_new_life()
        
        LifeButton:
            text: 'QUIT'
            on_release: app.stop()

<GameScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(15)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#FFFFFF') 
            Rectangle:
                pos: self.pos
                size: self.size

        # HUD: Status Stats (Age, Health, Happiness, Wealth)
        BoxLayout:
            size_hint_y: 0.15
            orientation: 'horizontal'
            spacing: dp(10)
            padding: dp(5)
            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(8),]

            Label:
                text: f'AGE: {app.age}'
                color: 0, 0, 0, 1
                font_size: '20sp'
            Label:
                text: f'HEALTH: [color=008800]{app.health}%[/color]'
                markup: True
                color: 0, 0, 0, 1
                font_size: '20sp'
            Label:
                text: f'HAPPINESS: [color=FFD700]{app.happiness}%[/color]'
                markup: True
                color: 0, 0, 0, 1
                font_size: '20sp'
            Label:
                text: f'WEALTH: [color=0000FF]${app.money:,.0f}[/color]'
                markup: True
                color: 0, 0, 0, 1
                font_size: '20sp'
        
        # Log/Event Feed
        Label:
            id: life_log
            text: app.game_log
            markup: True
            font_size: '16sp'
            halign: 'left'
            valign: 'top'
            size_hint_y: 0.4
            color: 0, 0, 0, 1
            text_size: self.width, None

        # Actions 
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: 0.25

            Label:
                text: 'ACTIONS'
                color: 0.2, 0.2, 0.2, 1
                font_size: '20sp'
                size_hint_y: None
                height: dp(30)

            BoxLayout:
                spacing: dp(10)
                LifeButton:
                    text: 'STUDY (+INT)'
                    on_release: app.perform_action('study')
                LifeButton:
                    text: 'WORK (+$$)'
                    on_release: app.perform_action('work')
                LifeButton:
                    text: 'EXERCISE (+HLTH)'
                    on_release: app.perform_action('exercise')

        # Age Button
        AgeButton:
            text: f'LIVE ANOTHER YEAR (Age {app.age})'
            size_hint_y: 0.15
            on_release: app.age_up()

<DeathScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(50)
        spacing: dp(30)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#1A1A1A') 
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: '[color=FF0000]GAME OVER[/color]'
            markup: True
            color: 1, 1, 1, 1
            font_size: '48sp'
            size_hint_y: 0.3
        
        Label:
            id: death_summary
            text: app.death_message
            markup: True
            color: 0.8, 0.8, 0.8, 1
            font_size: '24sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, self.height
            size_hint_y: 0.4

        LifeButton:
            text: 'RETURN TO MAIN MENU'
            on_release: app.root.current = 'start_screen'

"""

class LifeSimulatorApp(App):
    # Core Stats
    age = NumericProperty(0)
    health = NumericProperty(100)
    happiness = NumericProperty(50)
    money = NumericProperty(1000.0)
    intelligence = NumericProperty(50)

    # UI Properties
    game_log = StringProperty("A new life begins...")
    death_message = StringProperty("")
    
    # Event Data 
    RANDOM_EVENTS = {
        'positive': [
            ("You found $100 on the street!", lambda app: app._update_stats(money=100)),
            ("You received an unexpected compliment, boosting your mood.", lambda app: app._update_stats(happiness=5, health=1)),
            ("A distant relative left you a small inheritance ($5,000).", lambda app: app._update_stats(money=5000, happiness=10)),
            ("You started a daily jogging habit. Health improved!", lambda app: app._update_stats(health=8)),
            ("You won $500 in a small lottery!", lambda app: app._update_stats(money=500)),
        ],
        'negative': [
            ("Inflation hit hard this year. You lost $500.", lambda app: app._update_stats(money=-500)),
            ("You caught a bad cold. Health decreased slightly.", lambda app: app._update_stats(health=-10, happiness=-5)),
            ("You failed an important test. Intelligence takes a minor hit.", lambda app: app._update_stats(intelligence=-3, happiness=-10)),
            ("A minor injury puts you out of commission. Health -15.", lambda app: app._update_stats(health=-15)),
            ("You were scammed and lost $200.", lambda app: app._update_stats(money=-200, happiness=-5)),
        ],
        'milestone_child': [
            (2, "You are learning to walk and talk!", lambda app: app._update_stats(intelligence=2)),
            (5, "You started elementary school!", lambda app: app._update_stats(intelligence=5)),
            (10, "You discovered your favorite hobby.", lambda app: app._update_stats(happiness=5)),
            (14, "Puberty hits: awkward years begin!", lambda app: app._update_stats(happiness=-5)),
        ],
        'milestone_teen': [
            (16, "You got your first driver's license!", lambda app: app._update_stats(happiness=15)),
            (18, "You are now legally an adult. Time to choose your path!", lambda app: app._update_stats(happiness=10)),
            (21, "You can legally drink alcohol now!", lambda app: app._update_stats(health=-5, happiness=10)),
        ],
    }

    def build(self):
        self.title = 'BitLife Sim'
        return Builder.load_string(KV)

    def _update_stats(self, money=0, health=0, happiness=0, intelligence=0):
        """Helper function to safely update and bound stats."""
        self.money = float(max(0, self.money + money))
        self.health = float(max(0, min(100, self.health + health)))
        self.happiness = float(max(0, min(100, self.happiness + happiness)))
        self.intelligence = float(max(1, min(100, self.intelligence + intelligence)))

    def log_event(self, message):
        """Adds a new message to the top of the game log."""
        color = '000000' # Black
        if 'inheritance' in message or 'Gained' in message or 'improved' in message:
            color = '008800' # Green (Success/Positive)
        elif 'lost' in message or 'hit' in message or 'injury' in message or 'scammed' in message:
            color = 'AA0000' # Red (Failure/Negative)
        else:
             color = '333333' # Dark Grey (Neutral)

        new_log = f'[color={color}][b]AGE {int(self.age)}:[/b] {message}[/color]\n' + self.game_log
        
        # Keep log trimmed (last 15 lines)
        log_lines = new_log.split('\n')
        self.game_log = '\n'.join(log_lines[:min(len(log_lines), 15)])
        
    def start_new_life(self):
        """Initializes game state and moves to the game screen."""
        self.age = 0
        self.health = float(random.randint(70, 100))
        self.happiness = float(random.randint(40, 60))
        self.money = float(random.randint(500, 2000))
        self.intelligence = float(random.randint(40, 60))
        self.game_log = "You are born! Your journey begins."
        self.root.current = 'game_screen'

    # --- Core Game Loop ---
    def age_up(self):
        """Increments age, applies mandatory changes, and triggers events."""
        if self.check_death(): return

        self.age += 1
        
        # 1. Mandatory Annual Degradation
        # Health and Happiness naturally decay slightly, worsening with age > 20
        health_decay = 0
        if self.age > 20:
             health_decay = max(1, (self.age - 20) // 10)
        
        self._update_stats(health=-health_decay, happiness=-1)
        
        # 2. Financial Upkeep 
        if self.money < 5000:
             self._update_stats(money=-100) # Basic annual cost of living
             
        # 3. Trigger Events
        self.trigger_events()

        # 4. Check for death after aging
        self.check_death()

        if self.root.current == 'game_screen': # Only log if still alive
            self.log_event(f"You turned [b]Age {int(self.age)}[/b].")


    def trigger_events(self):
        """Checks for milestone events and random events."""
        
        # 1. Milestone Events
        for group in ['milestone_child', 'milestone_teen']:
            for age_key, message, effect in self.RANDOM_EVENTS.get(group, []):
                if self.age == age_key:
                    effect(self)
                    self.log_event(f"[b]MILESTONE:[/b] {message}")
                    return # Only one major event per year

        # 2. General Random Events 
        event_chance = 0.15
        if self.age < 10 or self.age > 60:
            event_chance += 0.10
            
        if random.random() < event_chance:
            event_type = random.choice(['positive', 'negative'])
            events = self.RANDOM_EVENTS[event_type]
            message, effect = random.choice(events)
            
            effect(self)
            self.log_event(f"EVENT: {message}")

    def perform_action(self, action_type):
        """Handles player choice actions (Study, Work, Exercise)."""
        if self.check_death(): return

        if action_type == 'study':
            if self.age < 6 or self.age > 70:
                self.log_event("You are too young or old to effectively study.")
                return
            
            int_gain = random.randint(1, 5)
            self._update_stats(intelligence=int_gain, happiness=-3)
            self.log_event(f"You studied diligently. Intelligence +{int_gain}%.")

        elif action_type == 'work':
            if self.age < 18:
                self.log_event("You are too young to hold a real job.")
                return

            # Money gain based on Intelligence (up to 3x base income)
            base_income = 500
            income_multiplier = 1 + (self.intelligence / 100 * 2)
            money_gain = int(base_income * income_multiplier)
            
            self._update_stats(money=money_gain, health=-3, happiness=-5)
            self.log_event(f"You worked hard. Gained ${money_gain:,.0f}.")

        elif action_type == 'exercise':
            health_gain = random.randint(5, 12)
            self._update_stats(health=health_gain, happiness=5)
            self.log_event(f"You exercised and feel great. Health +{health_gain}%, Happiness +5%.")


    def check_death(self):
        """Checks for death conditions and handles Game Over."""
        reason = None
        
        if self.health <= 0:
            reason = "Your health reached 0 due to severe illness or injury."
        elif self.age > 105:
            reason = "You lived an extremely long life, surpassing 105 years."
        elif self.age >= 60 and random.random() < (self.age - 59) / 100:
             reason = "You passed away peacefully of old age."

        if reason:
            if self.age < 18:
                summary = f"Your life ended tragically young at age {int(self.age)}.\nReason: {reason}"
            elif self.age < 60:
                summary = f"Your life ended prematurely at age {int(self.age)}.\nReason: {reason}"
            else:
                summary = f"Your life concluded at age {int(self.age)}.\nReason: {reason}\n\n[b]Final Stats:[/b]\nWealth: ${self.money:,.0f}\nIntelligence: {int(self.intelligence)}%"
                
            self.death_message = summary
            if self.root.current != 'death_screen':
                self.root.current = 'death_screen'
            return True
        return False


if __name__ == '__main__':
    LifeSimulatorApp().run()