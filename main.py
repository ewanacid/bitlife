import sys, traceback

# --- CRASH HANDLER (THE LAZARUS SHIELD) ---
# If Kivy fails to load, this block catches it.
try:
    from kivymd.app import MDApp
    from kivymd.uix.screen import MDScreen
    from kivymd.uix.button import MDFillRoundFlatButton
    from kivymd.uix.label import MDLabel
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.scrollview import MDScrollView
    from kivymd.uix.list import MDList, OneLineListItem
    import random
except Exception as e:
    # FALLBACK: If imports fail, run a raw Kivy error screen
    from kivy.app import App
    from kivy.uix.label import Label
    class ErrorApp(App):
        def build(self):
            return Label(text=f"CRITICAL IMPORT ERROR:\n{e}\n\nCheck buildozer.spec requirements!", color=(1,0,0,1))
    ErrorApp().run()
    sys.exit(1)

# --- GAME LOGIC ---
class GameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.age = 0
        self.money = 0
        self.happiness = 100
        self.health = 100
        self.log_history = []
        self.build_ui()

    def build_ui(self):
        # MAIN LAYOUT
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # HEADER (STATS)
        self.stats_label = MDLabel(
            text=self.get_stats_text(),
            halign="center",
            theme_text_color="Primary",
            font_style="H6"
        )
        layout.add_widget(self.stats_label)

        # EVENT LOG (SCROLLABLE)
        scroll = MDScrollView(size_hint=(1, 0.6))
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        layout.add_widget(scroll)

        # AGE UP BUTTON
        btn = MDFillRoundFlatButton(
            text="AGE UP (+1 Year)",
            font_size=20,
            size_hint=(1, 0.1),
            on_release=self.age_up
        )
        layout.add_widget(btn)

        self.add_widget(layout)
        self.log_event("born", "You were born into a digital world.")

    def get_stats_text(self):
        return f"Age: {self.age} | Money: ${self.money}\nHappiness: {self.happiness}% | Health: {self.health}%"

    def log_event(self, type, text):
        self.log_list.add_widget(OneLineListItem(text=f"Age {self.age}: {text}"))
        # Keep log short to prevent lag
        if len(self.log_list.children) > 50:
            self.log_list.remove_widget(self.log_list.children[0])

    def age_up(self, instance):
        self.age += 1
        
        # RANDOM EVENTS
        events = [
            ("Found $10 on the street.", 10, 5, 0),
            ("Got the flu.", -20, -10, -5),
            ("Made a new friend!", 0, 15, 0),
            ("Ate bad sushi.", -50, -20, -10),
            ("Won a small lottery!", 100, 20, 0),
            ("Nothing interesting happened.", 0, -2, 0)
        ]
        
        evt = random.choice(events)
        msg, money_chg, hap_chg, hlth_chg = evt
        
        self.money += money_chg
        self.happiness = max(0, min(100, self.happiness + hap_chg))
        self.health = max(0, min(100, self.health + hlth_chg))
        
        self.stats_label.text = self.get_stats_text()
        self.log_event("life", msg)

        if self.health <= 0:
            self.log_event("death", "YOU DIED.")
            instance.disabled = True
            self.stats_label.text = "GAME OVER"

class BitLifeApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        
        # SAFETY WRAPPER
        try:
            return GameScreen()
        except Exception as e:
            from kivymd.uix.label import MDLabel
            return MDLabel(text=f"RUNTIME ERROR:\n{traceback.format_exc()}", halign="center", theme_text_color="Error")

if __name__ == "__main__":
    try:
        BitLifeApp().run()
    except Exception as e:
        # ULTIMATE FAILSAFE: If App crashes, print why to a file AND stdout
        print("CRITICAL CRASH:")
        traceback.print_exc()
        with open("crash_log.txt", "w") as f:
            f.write(traceback.format_exc())
