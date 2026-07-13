import os
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.size = (360, 640)

class DatabaseDriver:
    def __init__(self, filename="app_state.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            self.write_data({"wishes": [], "milestone_date": "2025-10-24 00:00:00"})

    def read_data(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def write_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

db = DatabaseDriver()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        self.title = Label(text="SYSTEM AUTHENTICATION", font_size=24, bold=True, color=(0.23, 0.51, 0.96, 1))
        self.username = TextInput(hint_text="Username", multiline=False, write_tab=False, padding=10)
        self.password = TextInput(hint_text="Access Pin", password=True, multiline=False, write_tab=False, padding=10)
        
        self.login_btn = Button(text="Validate Credentials", background_color=(0.23, 0.51, 0.96, 1), font_weight='bold')
        self.login_btn.bind(on_press=self.verify)
        
        self.error_lbl = Label(text="", color=(0.92, 0.26, 0.26, 1))

        layout.add_widget(self.title)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_btn)
        layout.add_widget(self.error_lbl)
        self.add_widget(layout)

    def verify(self, instance):
        if self.username.text.strip().lower() == "admin" and self.password.text == "1234":
            self.manager.current = 'dashboard'
        else:
            self.error_lbl.text = "Error: Invalid Security Parameter Token"

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.countdown_label = Label(text="Initializing Timer Runtime...", font_size=16, color=(0.66, 0.33, 0.97, 1))
        self.main_layout.add_widget(self.countdown_label)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=10)
        self.wish_input = TextInput(hint_text="Commit a custom item string...", multiline=False, write_tab=False)
        submit_btn = Button(text="Commit", size_hint_x=0.3, background_color=(0.1, 0.73, 0.51, 1))
        submit_btn.bind(on_press=self.add_wish_item)
        input_layout.add_widget(self.wish_input)
        input_layout.add_widget(submit_btn)
        self.main_layout.add_widget(input_layout)
        
        self.scroll = ScrollView()
        self.wish_grid = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.wish_grid.bind(minimum_height=self.wish_grid.setter('height'))
        self.scroll.add_widget(self.wish_grid)
        self.main_layout.add_widget(self.scroll)
        
        self.add_widget(self.main_layout)
        self.on_enter = self.populate_dashboard

    def populate_dashboard(self):
        from kivy.clock import Clock
        Clock.schedule_interval(self.update_countdown_runtime, 1)
        self.refresh_grid_view()

    def update_countdown_runtime(self, dt):
        try:
            target = datetime.strptime(db.read_data()["milestone_date"], "%Y-%m-%d %H:%M:%S")
            diff = datetime.now() - target
            self.countdown_label.text = f"System Lifecycle Tracker Run:\n{diff.days} Days | {diff.seconds // 3600} Hours | {(diff.seconds % 3600) // 60} Mins"
        except Exception:
            self.countdown_label.text = "Runtime Error Processing Dates"

    def refresh_grid_view(self):
        self.wish_grid.clear_widgets()
        current_wishes = db.read_data().get("wishes", [])
        for index, item_text in enumerate(current_wishes):
            lbl = Label(text=f"[{index + 1}] {item_text}", size_hint_y=None, height=40, color=(0.95, 0.95, 0.98, 1))
            self.wish_grid.add_widget(lbl)

    def add_wish_item(self, instance):
        text_val = self.wish_input.text.strip()
        if text_val:
            current_state = db.read_data()
            current_state["wishes"].append(text_val)
            db.write_data(current_state)
            self.wish_input.text = ""
            self.refresh_grid_view()

class MobileFrameworkEngine(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm

if __name__ == '__main__':
    MobileFrameworkEngine().run()
