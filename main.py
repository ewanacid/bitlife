from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse
from kivy.metrics import dp
import random
import time

# --- MODULE: RADAR WIDGET ---
class RadarWidget(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(250), dp(250))
        self.pos_hint = {'center_x': 0.5}
        self.radius = [125]
        self.md_bg_color = (0, 0.1, 0.1, 1)
        self.angle = 0
        self.blips = []
        Clock.schedule_interval(self.update, 0.05)

    def update(self, dt):
        self.angle = (self.angle + 5) % 360
        self.canvas.after.clear()
        
        with self.canvas.after:
            # Radar Sweep Line
            Color(0, 1, 1, 0.8)
            Line(circle=(self.center_x, self.center_y, dp(120), self.angle, self.angle+2), width=2)
            
            # Random Blips (Enemies)
            if random.random() < 0.05:
                self.blips.append({'x': random.randint(-100, 100), 'y': random.randint(-100, 100), 'life': 50})
            
            # Draw Blips
            for blip in self.blips[:]:
                blip['life'] -= 1
                if blip['life'] <= 0: self.blips.remove(blip); continue
                
                opacity = blip['life'] / 50.0
                Color(1, 0, 0, opacity)
                Ellipse(pos=(self.center_x + dp(blip['x']), self.center_y + dp(blip['y'])), size=(dp(5), dp(5)))

# --- SCREEN: DASHBOARD ---
class Dashboard(MDScreen):
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # HEADER
        header = MDLabel(text="NFG SYSTEM v4.0", halign="center", font_style="H4", theme_text_color="Custom", text_color=(0,1,1,1), size_hint_y=0.1)
        layout.add_widget(header)

        # 1. OVERWATCH MODULE (CPU/Stats)
        stats_card = MDCard(orientation='vertical', size_hint_y=0.3, padding=15, radius=[15], md_bg_color=(0.1, 0.1, 0.1, 1))
        stats_card.add_widget(MDLabel(text="REACTOR STATUS", halign="center", theme_text_color="Secondary"))
        
        self.cpu_label = MDLabel(text="CPU LOAD: 0%", halign="center", font_style="H6")
        self.cpu_bar = MDProgressBar(value=0, color=(0,1,1,1))
        
        self.net_label = MDLabel(text="NET UPLINK: ONLINE", halign="center", font_style="Caption")
        
        stats_card.add_widget(self.cpu_label)
        stats_card.add_widget(self.cpu_bar)
        stats_card.add_widget(self.net_label)
        layout.add_widget(stats_card)

        # 2. RADAR MODULE
        self.radar = RadarWidget()
        layout.add_widget(self.radar)

        # 3. CONTROL GRID
        grid = MDGridLayout(cols=2, spacing=10, size_hint_y=0.2)
        btn1 = MDFillRoundFlatButton(text="EWTUBE", size_hint=(1, 1), md_bg_color=(1, 0, 0, 1))
        btn2 = MDFillRoundFlatButton(text="SCAN", size_hint=(1, 1), on_release=self.scan_network)
        grid.add_widget(btn1)
        grid.add_widget(btn2)
        layout.add_widget(grid)

        self.add_widget(layout)
        Clock.schedule_interval(self.update_stats, 1)

    def update_stats(self, dt):
        # Fake CPU simulation for visual effect (Actual /proc/stat access is restricted on some Androids)
        load = random.randint(10, 80)
        self.cpu_label.text = f"CPU LOAD: {load}%"
        self.cpu_bar.value = load
        
        # Blink effect
        color = (0,1,1,1) if load < 70 else (1,0,0,1)
        self.cpu_label.text_color = color
        self.cpu_bar.color = color

    def scan_network(self, instance):
        self.net_label.text = "SCANNING FREQUENCIES..."
        Clock.schedule_once(lambda x: setattr(self.net_label, 'text', "NO THREATS DETECTED"), 2)

class NFGApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        
        sm = MDScreenManager()
        dash = Dashboard(name='dashboard')
        dash.build_ui()
        sm.add_widget(dash)
        return sm

if __name__ == "__main__":
    NFGApp().run()
