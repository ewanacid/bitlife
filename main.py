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

# Define custom screens for the ScreenManager
class MainScreen(Screen):
    pass

class CasinoScreen(Screen):
    pass

# Define the KV string for our UI, embedding styles directly
KV = """
# Define a custom button style named CyberButton (for general actions)
<CyberButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0.09, 0.09, 0.2, 1 # Dark Blue background as per style guide
    color: 1, 1, 1, 1 # White text as per style guide
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

# Define a custom button style named RedCyberButton (for casino actions)
<RedCyberButton@Button>:
    background_normal: ''
    background_down: ''
    background_color: 0.6, 0.0, 0.0, 1 # Dark Red background for casino buttons
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
    MainScreen:
        name: 'main_screen'
    CasinoScreen:
        name: 'casino_screen'

<MainScreen>:
    orientation: 'vertical'
    padding: dp(20) # Padding around the entire layout
    spacing: dp(15) # Spacing between widgets
    canvas.before:
        Color:
            rgba: get_color_from_hex('#111111') # Updated background to Dark Grey
        Rectangle:
            pos: self.pos
            size: self.size

    # HUD BoxLayout for Health, Money, Happiness
    BoxLayout:
        id: hud_box
        orientation: 'horizontal'
        size_hint_y: 0.15 # Allocate space for HUD
        padding: dp(15) # Inner padding for HUD elements
        spacing: dp(10) # Spacing between HUD elements
        canvas.before:
            Color:
                rgba: get_color_from_hex('#222222') # Slightly lighter dark grey for HUD box
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(10),]
        Label:
            text: '[color=39ff14]HEALTH:[/color] ' + str(app.health) # Neon Green text
            markup: True
            font_size: '18sp'
            halign: 'left'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]MONEY:[/color] ' + str(app.money) + ' Crd' # Neon Green text
            markup: True
            font_size: '18sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, self.height
        Label:
            text: '[color=39ff14]HAPPINESS:[/color] ' + str(app.happiness) # Neon Green text
            markup: True
            font_size: '18sp'
            halign: 'right'
            valign: 'middle'
            text_size: self.width, self.height

    # Main "Hello World!" title label
    Label:
        text: '[color=39ff14]CYBERPUNK[/color] // HELLO WORLD!' # Neon Green text using markup
        markup: True
        font_size: '50sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.5 # Adjusted vertical space
        text_size: self.width, self.height

    # BoxLayout for organizing main action buttons horizontally
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(15) # Spacing between buttons as per style guide
        size_hint_y: 0.25 # Adjusted vertical space
        padding: dp(20) # Padding around the buttons layout as per style guide

        CyberButton: # Using the new CyberButton style
            text: 'ENGAGE PROTOCOL'
            on_release: app.on_engage_button_press() # Connect to app method for functionality

        CyberButton: # Using the new CyberButton style
            text: 'TERMINATE SEQUENCE'
            on_release: app.on_terminate_button_press() # Connect to app method for functionality

    # New button to enter the casino, using CyberButton style
    CyberButton:
        text: 'ENTER CYBER CASINO'
        size_hint_y: 0.1 # Allocate remaining space
        on_release: app.on_enter_casino()

<CasinoScreen>:
    orientation: 'vertical'
    padding: dp(20) # Padding around the entire layout
    spacing: dp(15) # Spacing between widgets
    canvas.before:
        Color:
            rgba: get_color_from_hex('#111111') # Updated background to Dark Grey
        Rectangle:
            pos: self.pos
            size: self.size

    # HUD for Casino screen (showing only money for brevity)
    BoxLayout:
        id: casino_hud_box
        orientation: 'horizontal'
        size_hint_y: 0.15
        padding: dp(15)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#222222')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(10),]
        Label:
            text: '[color=39ff14]MONEY:[/color] ' + str(app.money) + ' Crd'
            markup: True
            font_size: '18sp'
            halign: 'center'
            valign: 'middle'
            text_size: self.width, self.height

    Label:
        text: '[color=39ff14]CYBER CASINO[/color]' # Casino title with Neon Green text
        markup: True
        font_size: '40sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.2
        text_size: self.width, self.height

    # Casino game message label, bound to app property
    Label:
        id: casino_message
        text: app.casino_message_text
        markup: True
        font_size: '22sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.2
        text_size: self.width, self.height

    # Current number label for the casino game, bound to app property
    Label:
        id: current_number_label
        text: app.casino_current_number_text
        markup: True
        font_size: '28sp'
        halign: 'center'
        valign: 'middle'
        size_hint_y: 0.1
        text_size: self.width, self.height

    # BoxLayout for casino game action buttons (red buttons)
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(15)
        padding: dp(20)
        size_hint_y: 0.1

        RedCyberButton:
            text: 'GUESS LOWER (50 Crd)'
            on_release: app.play_casino_game('lower')
        RedCyberButton:
            text: 'GUESS HIGHER (50 Crd)'
            on_release: app.play_casino_game('higher')
    
    # Red button for exact bet option
    RedCyberButton:
        text: 'BET 50 ON 50 (100 Crd)'
        size_hint_y: 0.1
        on_release: app.play_casino_game('exact')

    # Red button to go back to the main screen
    RedCyberButton:
        text: 'BACK TO MAIN'
        size_hint_y: 0.1
        on_release: app.on_back_to_main()
"""

class HelloWorldApp(App):
    # Game stats as Kivy properties for automatic UI updates
    health = NumericProperty(100)
    money = NumericProperty(500)
    happiness = NumericProperty(75)

    # Casino game specific properties, bound to labels in KV
    casino_message_text = StringProperty('[color=39ff14]Guess if the next number is higher or lower than 50![/color]')
    casino_current_number_text = StringProperty('[color=39ff14]Current Number: ???[/color]')
    casino_target_number = NumericProperty(0) # The number to guess against

    def build(self):
        self.title = 'Cyberpunk Interface' # Updated app title
        # Load the KV string to build the UI
        return Builder.load_string(KV)

    def on_start(self):
        # Initialize the casino game when the app starts
        self.reset_casino_game()

    def reset_casino_game(self):
        """Resets the state of the casino game."""
        self.casino_target_number = random.randint(1, 100) # Generate new number
        self.casino_current_number_text = f'[color=39ff14]Current Number: {self.casino_target_number}[/color]'
        self.casino_message_text = '[color=39ff14]Guess if the next number is higher or lower than 50![/color]'

    # Main screen button handlers
    def on_engage_button_press(self):
        """Handles the 'ENGAGE PROTOCOL' button press."""
        print("ENGAGE PROTOCOL button pressed! Initiating...")
        # Placeholder logic: Increase happiness slightly
        self.happiness += 5
        if self.happiness > 100: self.happiness = 100

    def on_terminate_button_press(self):
        """Handles the 'TERMINATE SEQUENCE' button press."""
        print("TERMINATE SEQUENCE button pressed! Shutting down...")
        # Placeholder logic: Decrease health slightly
        self.health -= 10
        if self.health < 0: self.health = 0

    def on_enter_casino(self):
        """Switches to the casino screen."""
        self.root.current = 'casino_screen'
        self.reset_casino_game() # Reset game state when entering casino

    def on_back_to_main(self):
        """Switches back to the main screen."""
        self.root.current = 'main_screen'

    def play_casino_game(self, guess_type):
        """
        Implements the logic for the casino 'Higher/Lower/Exact' game.
        :param guess_type: 'lower', 'higher', or 'exact'
        """
        bet_amount = 50
        if guess_type == 'exact':
            bet_amount = 100 # Higher bet for exact guess

        if self.money < bet_amount:
            self.casino_message_text = '[color=ff0000]INSUFFICIENT FUNDS. You need more credits.[/color]'
            return

        # Generate a new random number for the game
        self.casino_target_number = random.randint(1, 100)
        self.casino_current_number_text = f'[color=39ff14]Number revealed: {self.casino_target_number}[/color]'

        win = False
        if guess_type == 'lower':
            if self.casino_target_number < 50:
                win = True
        elif guess_type == 'higher':
            if self.casino_target_number > 50:
                win = True
        elif guess_type == 'exact':
            if self.casino_target_number == 50:
                win = True

        if win:
            payout = bet_amount * 2 if guess_type != 'exact' else bet_amount * 4 # Higher payout for exact
            self.money += payout
            self.happiness += 10 # Reward for winning
            self.casino_message_text = f'[color=39ff14]WINNER! You won {payout} credits![/color]'
        else:
            self.money -= bet_amount
            self.happiness -= 5 # Consequence for losing
            self.casino_message_text = f'[color=ff0000]LOSER. You lost {bet_amount} credits.[/color]'
        
        # Ensure stats don't go out of expected bounds
        if self.health < 0: self.health = 0
        if self.happiness < 0: self.happiness = 0
        if self.happiness > 100: self.happiness = 100
        if self.money < 0: self.money = 0

if __name__ == '__main__':
    HelloWorldApp().run()
