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
from datetime import datetime

# Define custom screens for the ScreenManager
class HackingConsoleScreen(Screen):
    pass

class EvolutionChamberScreen(Screen):
    pass

# Define the KV string for our UI, embedding styles directly
KV = """
# Define a custom button style named CyberButton (for general actions)
<CyberButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0.09, 0.09, 0.2, 1 # Dark Blue background
    color: 1, 1, 1, 1 # White text
    font_size: '20sp'
    size_hint_y: None
    height: dp(60)
    text_size: self.width - dp(20), self.height - dp(20)
    valign: 'middle'
    halign: 'center'
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(15),] # Apply rounded corners

# Define a custom button style named RedCyberButton (for high-risk/evolution actions)
<RedCyberButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0.6, 0.0, 0.0, 1 # Dark Red background
    color: 1, 1, 1, 1 # White text
    font_size: '20sp'
    size_hint_y: None
    height: dp(60)
    text_size: self.width - dp(20), self.height - dp(20)
    valign: 'middle'
    halign: 'center'
    canvas.before:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(15),] # Apply rounded corners

# ScreenManager to manage different application views
ScreenManager:
    HackingConsoleScreen:
        name: 'hacking_console_screen'
    EvolutionChamberScreen:
        name: 'evolution_chamber_screen'

<HackingConsoleScreen>:
    orientation: 'vertical'
    padding: dp(20) # Padding around the entire layout
    spacing: dp(15) # Spacing between widgets
    canvas.before:
        Color:
            rgba: get_color_from_hex('#050505') # Cyberpunk Dark background
        Rectangle:
            pos: self.pos
            size: self.size

    # HUD BoxLayout for Data Bits, Processing Power, Growth Factor, System Integrity
    BoxLayout:
        id: hud_box
        orientation: 'horizontal'
        size_hint_y: 0.15 # Allocate space for HUD
        padding: dp(15) # Inner padding for HUD elements
        spacing: dp(10) # Spacing between HUD elements
        canvas.before:
            Color:
                rgba: get_color_from_hex('#0F0F0F') # Slightly lighter dark grey for HUD box
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(10),]
        Label:
            text: '[color=39ff14]DATA BITS:[/color] ' + str(app.data_bits)
            markup: True
            font_size: '18sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]PROC. POWER:[/color] ' + str(app.processing_power)
            markup: True
            font_size: '18sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]GROWTH:[/color] ' + str(app.growth_factor) + '%'
            markup: True
            font_size: '18sp'
            halign: 'right'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]INTEGRITY:[/color] ' + str(app.system_integrity) + '%'
            markup: True
            font_size: '18sp'
            halign: 'right'
            valign: 'middle'
            text_size: self.width, self.height

    # Main title label
    Label:
        text: '[color=39ff14]PYTHON[/color] // FORGE V' + str(app.evolution_level) # Neon Green text using markup
        markup: True
        font_size: '50sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.25 # Adjusted vertical space
        text_size: self.width, self.height

    # System Log / Message Feed
    Label:
        id: system_log
        text: app.system_log_text
        markup: True
        font_size: '16sp'
        halign: 'left'
        valign: 'top'
        size_hint_y: 0.25
        text_size: self.width, self.height
        padding_x: dp(10) # Add some horizontal padding to the log

    # BoxLayout for organizing main action buttons horizontally
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10) # Spacing between buttons
        size_hint_y: 0.25 # Adjusted vertical space
        padding: dp(20) # Padding around the buttons layout

        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(15)
            CyberButton:
                text: 'MINE DATA BITS'
                on_release: app.mine_data_bits()
            CyberButton:
                text: 'OPTIMIZE CODE (200 DB)'
                on_release: app.optimize_code()
        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(15)
            CyberButton:
                text: 'INJECT GROWTH MODULE (150 DB)'
                on_release: app.inject_growth_module()
            CyberButton:
                text: 'PERFORM SYSTEM CHECK (50 DB)'
                on_release: app.perform_system_check()

    # Button to access Evolution Chamber
    CyberButton:
        text: 'ACCESS EVOLUTION CHAMBER'
        size_hint_y: 0.1 # Allocate remaining space
        on_release: app.on_enter_evolution_chamber()

<EvolutionChamberScreen>:
    orientation: 'vertical'
    padding: dp(20) # Padding around the entire layout
    spacing: dp(15) # Spacing between widgets
    canvas.before:
        Color:
            rgba: get_color_from_hex('#050505') # Cyberpunk Dark background
        Rectangle:
            pos: self.pos
            size: self.size

    # HUD for Evolution Chamber screen (showing only Data Bits for brevity)
    BoxLayout:
        id: evolution_hud_box
        orientation: 'horizontal'
        size_hint_y: 0.15
        padding: dp(15)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#0F0F0F')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(10),]
        Label:
            text: '[color=39ff14]DATA BITS:[/color] ' + str(app.data_bits)
            markup: True
            font_size: '18sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]GROWTH:[/color] ' + str(app.growth_factor) + '%'
            markup: True
            font_size: '18sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]INTEGRITY:[/color] ' + str(app.system_integrity) + '%'
            markup: True
            font_size: '18sp'
            halign: 'right'
            valign: 'middle'
            text_size: self.width, self.height


    Label:
        text: '[color=39ff14]EVOLUTION CHAMBER[/color] // PROTOCOL V' + str(app.evolution_level)
        markup: True
        font_size: '40sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.2
        text_size: self.width, self.height

    # Evolution status message label, bound to app property
    Label:
        id: evolution_message
        text: app.evolution_status_text
        markup: True
        font_size: '22sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.3
        text_size: self.width, self.height

    # Button to attempt evolution (red button for critical action)
    RedCyberButton:
        text: 'ATTEMPT EVOLUTION (500 DB, 100% Growth)'
        size_hint_y: 0.1
        on_release: app.attempt_evolution()
    
    # Red button to go back to the main console
    RedCyberButton:
        text: 'BACK TO CONSOLE'
        size_hint_y: 0.1
        on_release: app.on_back_to_console()
"""

class PythonForgeApp(App):
    # Game stats as Kivy properties for automatic UI updates
    data_bits = NumericProperty(1000)
    processing_power = NumericProperty(10) # Affects data mining rate and evolution success chance
    growth_factor = NumericProperty(0) # Progress towards next evolution level (0-100)
    system_integrity = NumericProperty(100) # System 'health', if 0, game over
    evolution_level = NumericProperty(0) # Current Python version/level

    # Game specific message properties, bound to labels in KV
    system_log_text = StringProperty('[color=39ff14]System online. Initiate Python Forge protocols.[/color]')
    evolution_status_text = StringProperty('[color=39ff14]Ready for next evolution. Increase Growth Factor to 100%.[/color]')

    def build(self):
        self.title = 'Python Forge // Cyberpunk OS' # Updated app title
        # Load the KV string to build the UI
        return Builder.load_string(KV)

    def on_start(self):
        # Initialize game state when the app starts
        self.reset_game_state()

    def log_message(self, message, color='39ff14'):
        """Appends a timestamped message to the system log."""
        timestamp = datetime.now().strftime('[%H:%M:%S]')
        new_log = f'[color={color}]{timestamp} {message}[/color]\n' + self.system_log_text
        # Keep log to a reasonable length, e.g., last 7 lines
        log_lines = new_log.split('\n')
        self.system_log_text = '\n'.join(log_lines[:min(len(log_lines), 7)])

    def reset_game_state(self):
        """Resets the core game state, typically for a new game or game over."""
        self.data_bits = 1000
        self.processing_power = 10
        self.growth_factor = 0
        self.system_integrity = 100
        self.evolution_level = 0
        self.system_log_text = '[color=39ff14]System online. Initiate Python Forge protocols.[/color]'
        self.evolution_status_text = '[color=39ff14]Ready for next evolution. Increase Growth Factor to 100%.[/color]'

    def check_game_over(self):
        """Checks for game over conditions."""
        if self.system_integrity <= 0:
            self.system_integrity = 0
            self.log_message("CRITICAL SYSTEM FAILURE! Python Forge terminated.", 'ff0000')
            self.system_log_text = '[color=ff0000]SYSTEM SHUTDOWN: INTEGRITY CRITICAL. Rebooting protocols...[/color]'
            # Optionally, switch to a game over screen or reset immediately
            # For now, just reset for simplicity
            self.root.current = 'hacking_console_screen'
            self.reset_game_state()
            return True
        return False

    # Main console action handlers
    def mine_data_bits(self):
        """Action: Mine Data Bits."""
        if self.check_game_over(): return
        
        gained_data = self.processing_power * random.randint(5, 15)
        self.data_bits += gained_data
        self.log_message(f"Data mining successful. Gained {gained_data} Data Bits.")
        
        # Small chance of integrity hit
        if random.random() < 0.15: # 15% chance
            integrity_hit = random.randint(1, 5)
            self.system_integrity -= integrity_hit
            self.log_message(f"Mining anomaly detected: System Integrity -{integrity_hit}%.", 'ffff00') # Yellow for warning
            self.check_game_over()

    def optimize_code(self):
        """Action: Optimize Code to increase Processing Power."""
        if self.check_game_over(): return

        cost = 200
        if self.data_bits < cost:
            self.log_message("Insufficient Data Bits for Code Optimization. Need 200 DB.", 'ff0000')
            return

        self.data_bits -= cost
        self.processing_power += 5
        self.log_message(f"Code optimization complete. Processing Power +5.")
        
        # Small chance of integrity hit due to faulty optimization
        if random.random() < 0.1: # 10% chance
            integrity_hit = random.randint(2, 8)
            self.system_integrity -= integrity_hit
            self.log_message(f"Optimization error: System Integrity -{integrity_hit}%. Requires debugging.", 'ffff00')
            self.check_game_over()

    def inject_growth_module(self):
        """Action: Inject Growth Module to increase Growth Factor."""
        if self.check_game_over(): return

        cost = 150
        if self.data_bits < cost:
            self.log_message("Insufficient Data Bits for Growth Module Injection. Need 150 DB.", 'ff0000')
            return

        self.data_bits -= cost
        self.growth_factor += random.randint(10, 25)
        if self.growth_factor > 100: self.growth_factor = 100
        self.log_message(f"Growth Module injected. Growth Factor increased to {self.growth_factor}%.")

        # Small chance of integrity hit due to module incompatibility
        if random.random() < 0.12: # 12% chance
            integrity_hit = random.randint(3, 10)
            self.system_integrity -= integrity_hit
            self.log_message(f"Growth module incompatibility: System Integrity -{integrity_hit}%.", 'ffff00')
            self.check_game_over()

    def perform_system_check(self):
        """Action: Perform System Check to restore System Integrity."""
        if self.check_game_over(): return

        cost = 50
        if self.data_bits < cost:
            self.log_message("Insufficient Data Bits for System Check. Need 50 DB.", 'ff0000')
            return

        self.data_bits -= cost
        integrity_gain = random.randint(10, 20)
        self.system_integrity += integrity_gain
        if self.system_integrity > 100: self.system_integrity = 100
        self.log_message(f"System check complete. System Integrity +{integrity_gain}%.")
        self.check_game_over() # Just in case integrity dropped to 0 and was then restored by this check

    def on_enter_evolution_chamber(self):
        """Switches to the evolution chamber screen."""
        if self.check_game_over(): return
        self.root.current = 'evolution_chamber_screen'
        self.evolution_status_text = '[color=39ff14]Ready for next evolution. Increase Growth Factor to 100%.[/color]'
        self.log_message("Entering Evolution Chamber. Assess Python's readiness.")

    def on_back_to_console(self):
        """Switches back to the hacking console screen."""
        if self.check_game_over(): return
        self.root.current = 'hacking_console_screen'
        self.log_message("Returning to Hacking Console. Continue operations.")

    def attempt_evolution(self, *args):
        """
        Implements the logic for attempting Python evolution.
        Requires 100% Growth Factor and Data Bits.
        """
        if self.check_game_over(): return

        evolution_cost = 500
        if self.growth_factor < 100:
            self.evolution_status_text = '[color=ff0000]Evolution failed: Growth Factor not at 100%. Inject more modules![/color]'
            self.log_message("Evolution attempt failed. Growth Factor insufficient.", 'ff0000')
            return
        if self.data_bits < evolution_cost:
            self.evolution_status_text = f'[color=ff0000]Evolution failed: Insufficient Data Bits. Need {evolution_cost} DB.[/color]'
            self.log_message("Evolution attempt failed. Insufficient Data Bits.", 'ff0000')
            return

        self.data_bits -= evolution_cost
        self.growth_factor = 0 # Growth resets after attempt

        # Calculate success chance: Base 60% + (Processing Power / 1000 * 20%) capped at 95%
        success_chance = 0.60 + (self.processing_power / 1000 * 0.20) # e.g., 100 PP -> 2%, 1000 PP -> 20%
        success_chance = min(success_chance, 0.95) # Cap at 95%
        
        if random.random() < success_chance:
            self.evolution_level += 1
            bonus_data = self.evolution_level * 200 + 500 # Base bonus + level multiplier
            self.data_bits += bonus_data
            self.processing_power += 5 # Small boost after successful evolution
            self.system_integrity = min(100, self.system_integrity + 10) # Small integrity boost
            self.evolution_status_text = f'[color=39ff14]EVOLUTION SUCCESS! Python V{self.evolution_level} achieved. Gained {bonus_data} DB.[/color]'
            self.log_message(f"Python evolved to V{self.evolution_level}! Data Bonus: {bonus_data} DB.", '39ff14')
        else:
            integrity_hit = random.randint(15, 30)
            self.system_integrity -= integrity_hit
            self.evolution_status_text = f'[color=ff0000]EVOLUTION FAILED! System Integrity -{integrity_hit}%. Back to the drawing board.[/color]'
            self.log_message(f"Evolution attempt failed. System Integrity -{integrity_hit}%.", 'ff0000')
            self.check_game_over() # Check if failure led to game over

        # Ensure stats don't go out of expected bounds
        self.data_bits = max(0, self.data_bits)
        self.processing_power = max(1, self.processing_power) # Minimum 1 processing power
        self.system_integrity = max(0, self.system_integrity)
        self.growth_factor = max(0, self.growth_factor) # Cannot be negative
        
        self.evolution_status_text += f'\n[color=39ff14]Current Growth: {self.growth_factor}%. Next Evolution requires 100%.[/color]'
        self.system_log_text = '[color=39ff14]Evolution protocols updated.[/color]\n' + self.system_log_text

if __name__ == '__main__':
    PythonForgeApp().run()
