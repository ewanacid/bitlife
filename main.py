from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.metrics import dp # Import for dp units

# Define the KV string for our UI, embedding styles directly
KV = """
# Define a custom button style named NeonButton
<NeonButton@Button>:
    background_normal: '' # Disable default background image
    background_down: '' # Disable default background image for pressed state
    background_color: 0.2, 0.2, 0.2, 1 # Dark gray for button body
    color: 1, 1, 1, 1 # White text as per "Modern Dark Theme (Text: White)"
    font_size: '20sp' # Readable font size for buttons
    size_hint_y: None # Disable vertical size hinting for fixed height
    height: dp(60) # Fixed height for buttons
    # Ensure text is centered and has internal padding
    text_size: self.width - dp(20), self.height - dp(20)
    valign: 'middle'
    halign: 'center'
    canvas.before:
        # Draw neon green border
        Color:
            rgba: 0, 1, 0, 1 # Neon green accent color
        Line:
            width: dp(2) # Border thickness
            rounded_rectangle: self.x + dp(2), self.y + dp(2), self.width - dp(4), self.height - dp(4), dp(15)
        # Draw dark gray button background
        Color:
            rgba: self.background_color # Use the defined background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(15),] # Apply rounded corners

# Define the root layout (vertical BoxLayout)
BoxLayout:
    orientation: 'vertical'
    padding: dp(20) # Padding around the entire layout
    spacing: dp(15) # Spacing between widgets
    canvas.before:
        # Set the Modern Dark Theme background color
        Color:
            rgba: get_color_from_hex('#121212')
        Rectangle:
            pos: self.pos
            size: self.size

    # Main "Hello World!" label
    Label:
        text: '[color=00ff00]CYBERPUNK[/color] // HELLO WORLD!' # Neon green text using markup
        markup: True # Enable markup for color tag
        font_size: '50sp' # Large, readable font size for the main title
        halign: 'center' # Center the text horizontally
        valign: 'middle' # Center the text vertically
        size_hint_y: 0.6 # Allocate more vertical space for the label
        text_size: self.width, self.height # Essential for halign/valign to work consistently

    # BoxLayout for organizing buttons horizontally
    BoxLayout:
        orientation: 'horizontal'
        spacing: dp(10) # Spacing between buttons
        size_hint_y: 0.4 # Allocate less vertical space for buttons
        padding: dp(10) # Padding around the buttons layout

        # First button with NeonButton style
        NeonButton:
            text: 'ENGAGE PROTOCOL'
            on_release: app.on_engage_button_press() # Connect to app method for functionality

        # Second button with NeonButton style
        NeonButton:
            text: 'TERMINATE SEQUENCE'
            on_release: app.on_terminate_button_press() # Connect to app method for functionality
"""

class HelloWorldApp(App):
    def build(self):
        self.title = 'Cyberpunk Interface' # Updated app title
        # Load the KV string to build the UI
        return Builder.load_string(KV)

    # Placeholder function for the 'ENGAGE PROTOCOL' button
    def on_engage_button_press(self):
        print("ENGAGE PROTOCOL button pressed! Initiating...")
        # Add your engagement logic here

    # Placeholder function for the 'TERMINATE SEQUENCE' button
    def on_terminate_button_press(self):
        print("TERMINATE SEQUENCE button pressed! Shutting down...")
        # Add your termination logic here

if __name__ == '__main__':
    HelloWorldApp().run()
