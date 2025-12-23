from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import NumericProperty

class LifeGameApp(App):
    # Game stats as Kivy properties for easy management
    health = NumericProperty(100)
    happiness = NumericProperty(50)
    money = NumericProperty(100)

    def build(self):
        self.title = 'Life Simulator'
        
        # Main layout: vertical box layout for stats and buttons
        root_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)

        # Stats display section at the top
        stats_layout = BoxLayout(orientation='horizontal', size_hint_y=0.25, spacing=10)
        self.health_label = Label(text=self._get_health_text(), font_size='22sp', halign='center', valign='middle')
        self.happiness_label = Label(text=self._get_happiness_text(), font_size='22sp', halign='center', valign='middle')
        self.money_label = Label(text=self._get_money_text(), font_size='22sp', halign='center', valign='middle')
        
        stats_layout.add_widget(self.health_label)
        stats_layout.add_widget(self.happiness_label)
        stats_layout.add_widget(self.money_label)
        root_layout.add_widget(stats_layout)

        # Action buttons section in the middle
        buttons_layout = BoxLayout(orientation='vertical', spacing=25, padding=[20, 0, 20, 20]) # Left, Top, Right, Bottom

        work_button = Button(text='Work', font_size='35sp', size_hint_y=None, height=120)
        work_button.bind(on_release=self.do_work)
        buttons_layout.add_widget(work_button)

        rest_button = Button(text='Rest', font_size='35sp', size_hint_y=None, height=120)
        rest_button.bind(on_release=self.do_rest)
        buttons_layout.add_widget(rest_button)

        socialize_button = Button(text='Socialize', font_size='35sp', size_hint_y=None, height=120)
        socialize_button.bind(on_release=self.do_socialize)
        buttons_layout.add_widget(socialize_button)

        root_layout.add_widget(buttons_layout)

        # Initial display update
        self._update_all_labels()
        
        return root_layout

    def _get_health_text(self):
        """Returns formatted text for health stat."""
        return f"Health: {int(self.health)}"

    def _get_happiness_text(self):
        """Returns formatted text for happiness stat."""
        return f"Happiness: {int(self.happiness)}"

    def _get_money_text(self):
        """Returns formatted text for money stat."""
        return f"Money: {int(self.money)}"

    def _update_all_labels(self):
        """Updates the text of all stat labels."""
        self.health_label.text = self._get_health_text()
        self.happiness_label.text = self._get_happiness_text()
        self.money_label.text = self._get_money_text()

    def do_work(self, instance):
        """Handles the 'Work' button click, updating stats."""
        self.health = max(0, self.health - 15)
        self.happiness = max(0, self.happiness - 10)
        self.money += 20
        self._update_all_labels()

    def do_rest(self, instance):
        """Handles the 'Rest' button click, updating stats."""
        self.health = min(100, self.health + 20)
        self.happiness = min(100, self.happiness + 10)
        self._update_all_labels()

    def do_socialize(self, instance):
        """Handles the 'Socialize' button click, updating stats."""
        self.happiness = min(100, self.happiness + 15)
        self.money = max(0, self.money - 10) # Socializing can cost money
        self._update_all_labels()

if __name__ == '__main__':
    LifeGameApp().run()
