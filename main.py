from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton, MDRectangleFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineListItem, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.toolbar import MDTopAppBar # Added toolbar for better UI

import random

# --- Life Engine ---
class LifeEngine:
    def __init__(self):
        self.age = 0
        self.money = 0
        self.health = random.randint(70, 100)
        self.smarts = random.randint(20, 90)
        self.looks = random.randint(20, 90) # New stat
        self.happiness = random.randint(50, 100) # New stat
        self.karma = random.randint(0, 100) # New stat (mostly for good/bad actions)

        self.job = None # {"title": "Developer", "salary": 60000, "level": 1}
        self.school_level = "None" # Elementary, Middle, High, University, Graduated High School, Graduated University
        self.education_completed = [] # List of degrees/schools completed

        self.relationships = [] # Format: [{"name": "Mom", "type": "parent", "karma": 80, "status": "Alive"}]
        self.generate_parents()

        self.alive = True
        self.log_history = ["Born into a digital world."]
        self.dialog_instance = None # To hold reference to active dialog for dismissal

    def generate_parents(self):
        self.relationships.append({"name": "Mom", "type": "mother", "karma": random.randint(70, 100), "status": "Alive"})
        self.relationships.append({"name": "Dad", "type": "father", "karma": random.randint(70, 100), "status": "Alive"})
        self.log("You have a mother and a father.")

    def log(self, text):
        self.log_history.insert(0, f"Age {self.age}: {text}")
        # Keep log history trimmed for performance if it gets too long
        if len(self.log_history) > 100:
            self.log_history = self.log_history[:100]

    def _update_stats_after_action(self):
        # Basic decay/growth
        self.happiness = max(0, min(100, self.happiness - random.randint(0, 2)))
        self.health = max(0, min(100, self.health - random.randint(0, 1)))
        self.looks = max(0, min(100, self.looks - random.randint(0, 0))) # Looks decay slower
        self.smarts = max(0, min(100, self.smarts - random.randint(0, 0)))
        self.karma = max(0, min(100, self.karma - random.randint(0, 0))) # Karma decays slowly naturally

        # Age-related effects
        if self.age >= 60:
            self.health = max(0, self.health - random.randint(1, 3))
        if self.age >= 80 and random.random() < 0.2:
            self.health = 0 # Higher chance of death

    def _check_death(self):
        if self.health <= 0:
            self.alive = False
            self.log("DIED of poor health.")
        elif self.age >= random.randint(90, 105) and random.random() < 0.5: # Old age
            self.health = 0 # Force death
            self.alive = False
            self.log("DIED of old age.")
        elif self.happiness <= 0: # Extreme unhappiness
            self.alive = False
            self.log("DIED due to extreme unhappiness.")

    def age_up(self):
        if not self.alive:
            self.log("You have died. Start a new life!")
            return

        self.age += 1
        self.log(f"You turned {self.age} years old.")

        # Apply base stat changes and checks
        self._update_stats_after_action()

        # Job income
        if self.job:
            self.money += self.job['salary']
            if random.random() < 0.1: # Chance for raise
                raise_amt = int(self.job['salary'] * 0.05)
                self.job['salary'] += raise_amt
                self.log(f"Got a raise at work! Salary: ${self.job['salary']:,}")
            if random.random() < 0.02: # Chance for promotion
                if self.job['level'] < 5: # Max level 5 for now
                    self.job['level'] += 1
                    self.job['salary'] += int(self.job['salary'] * 0.15)
                    self.log(f"You were promoted to {self.job['title']} Level {self.job['level']}! Salary: ${self.job['salary']:,}")
        
        # Random Events - More BitLife-like events
        roll = random.random()
        if self.age < 18: # Childhood events
            if roll < 0.08:
                self.smarts += random.randint(1, 5)
                self.log("You learned something new at school and feel smarter.")
            elif roll < 0.12:
                self.happiness += random.randint(2, 7)
                self.log("You had a great day playing with friends.")
            elif roll < 0.15:
                self.health -= random.randint(1, 5)
                self.log("You caught a minor cold.")
            elif roll < 0.16: # Special event - bully
                self.happiness = max(0, self.happiness - random.randint(5, 15))
                self.log("You were bullied at school, your happiness decreased.")
        else: # Adult events
            if roll < 0.03:
                self.money += random.randint(50, 200)
                self.log("You found some money on the ground.")
            elif roll < 0.06:
                self.health = max(0, self.health - random.randint(5, 15))
                self.log("You got a minor injury.")
            elif roll < 0.07:
                self.happiness = max(0, self.happiness - random.randint(10, 20))
                self.log("A close friend moved away.")
            elif roll < 0.08:
                self.smarts = min(100, self.smarts + random.randint(1, 3))
                self.log("You read an interesting book and feel more intelligent.")
            elif roll < 0.09:
                self.looks = min(100, self.looks + random.randint(1, 5))
                self.log("You started a new grooming routine and look better.")
            elif roll < 0.10: # Relationship event (parents aging)
                for rel in self.relationships:
                    if rel['type'] in ['mother', 'father'] and rel['status'] == 'Alive':
                        if random.random() < 0.1: # Small chance parents die
                            rel['status'] = 'Deceased'
                            self.happiness = max(0, self.happiness - 20)
                            self.log(f"Your {rel['name']} ({rel['type']}) passed away. Happiness decreased.")
                            break # Only one parent per age up event

        # Handle education progression for childhood
        if self.age == 6 and self.school_level == "None":
            self.school_level = "Elementary"
            self.log("You started Elementary School.")
        elif self.age == 12 and self.school_level == "Elementary":
            self.school_level = "Middle"
            self.log("You graduated Elementary School and started Middle School.")
        elif self.age == 14 and self.school_level == "Middle":
            self.school_level = "High"
            self.log("You graduated Middle School and started High School.")
        elif self.age == 18 and self.school_level == "High":
            self.education_completed.append("High School Diploma")
            self.log("You graduated High School.")
            self.school_level = "Graduated High School" # Now eligible for University or work

        # Check for death after all events
        self._check_death()

    # --- Actions ---
    def go_to_gym(self):
        cost = 100
        if self.money >= cost:
            self.money -= cost
            self.health = min(100, self.health + random.randint(5, 10))
            self.looks = min(100, self.looks + random.randint(2, 7))
            self.happiness = min(100, self.happiness + random.randint(1, 3))
            self.log(f"You went to the gym. Health and Looks improved! (-${cost})")
        else:
            self.log(f"You don't have enough money to go to the gym. (Need ${cost})")
            return False
        return True

    def study(self):
        self.smarts = min(100, self.smarts + random.randint(3, 8))
        self.happiness = max(0, self.happiness - random.randint(1, 3)) # Studying can be boring
        self.log("You hit the books and increased your smarts.")

    def meditate(self):
        self.happiness = min(100, self.happiness + random.randint(5, 10))
        self.health = min(100, self.health + random.randint(1, 3))
        self.karma = min(100, self.karma + random.randint(1, 2))
        self.log("You meditated and feel more at peace.")

    def visit_doctor(self):
        cost = 500
        if self.money >= cost:
            self.money -= cost
            self.health = 100 # Fully restore health
            self.log(f"You visited the doctor. Health restored! (-${cost})")
        else:
            self.log(f"You don't have enough money to visit the doctor. (Need ${cost})")
            return False
        return True

    def apply_for_job(self, job_title, salary, required_smarts=0, required_degree=None):
        if self.age < 18:
            self.log("You are too young to apply for a job.")
            return False
        if required_degree and required_degree not in self.education_completed:
            self.log(f"You need a {required_degree} to apply for this job.")
            return False
        if self.smarts < required_smarts:
            self.log(f"You are not smart enough for this job (requires {required_smarts} smarts).")
            return False
        if self.job:
            self.log(f"You already have a job as a {self.job['title']}.")
            return False

        if random.random() * 100 < self.smarts: # Chance based on smarts
            self.job = {"title": job_title, "salary": salary, "level": 1}
            self.log(f"Hired as a {job_title}! Salary: ${salary:,}")
            self.happiness = min(100, self.happiness + 10)
            return True
        else:
            self.log(f"Your application for {job_title} was rejected.")
            self.happiness = max(0, self.happiness - 5)
            return False
    
    def resign_from_job(self):
        if self.job:
            job_title = self.job['title']
            self.job = None
            self.log(f"You resigned from your job as a {job_title}.")
            self.happiness = min(100, self.happiness + 5) # Maybe relief?
        else:
            self.log("You are currently unemployed.")

    def commit_petty_crime(self):
        if self.age < 12:
            self.log("You are too young for crime.")
            return False

        if random.random() < 0.6: # Success chance
            loot = random.randint(50, 500)
            self.money += loot
            self.karma = max(0, self.karma - random.randint(1, 5))
            self.happiness = min(100, self.happiness + random.randint(2, 7)) # Thrill
            self.log(f"You successfully committed a petty crime! +${loot}")
            return True
        else:
            self.health = max(0, self.health - random.randint(5, 15)) # Caught or injured
            self.happiness = max(0, self.happiness - random.randint(10, 20))
            self.karma = max(0, self.karma - random.randint(5, 10))
            self.log("You were caught or injured during a petty crime! Health and Happiness decreased.")
            return False

    def go_to_university(self, university_name="Generic University", cost=10000):
        if self.age < 18:
            self.log("You are too young for university.")
            return False
        if "High School Diploma" not in self.education_completed:
            self.log("You need to graduate high school first.")
            return False
        if self.money < cost:
            self.log(f"You don't have enough money for {university_name}. (Need ${cost:,})")
            return False
        if self.school_level == "University":
            self.log("You are already enrolled in university.")
            return False
        
        self.money -= cost
        self.smarts = min(100, self.smarts + random.randint(10, 20))
        self.happiness = min(100, self.happiness + random.randint(5, 10))
        self.school_level = "University"
        self.education_completed.append(f"Enrolled in {university_name}")
        self.log(f"You enrolled in {university_name}! (-${cost:,}) Smarts and happiness increased.")
        return True

    def graduate_university(self):
        if self.school_level != "University":
            self.log("You are not currently enrolled in university.")
            return False
        
        self.education_completed.append("University Degree")
        self.smarts = min(100, self.smarts + random.randint(15, 25))
        self.happiness = min(100, self.happiness + random.randint(10, 15))
        self.school_level = "Graduated University"
        self.log("You graduated from University! Smarts and happiness significantly increased.")
        return True
    
    def interact_with_relationship(self, relationship):
        self.log(f"You spent time with {relationship['name']} ({relationship['type']}).")
        self.happiness = min(100, self.happiness + random.randint(3, 8))
        relationship['karma'] = min(100, relationship['karma'] + random.randint(1, 5))


# --- KivyMD UI ---
class GameScreen(MDScreen):
    engine = LifeEngine() # Initialize engine once per app lifecycle, re-init on game start

    def on_enter(self):
        # Reset engine if it's not a new game, or on first entry, or if the character died
        if not hasattr(self, '_initialized') or not self._initialized or not self.engine.alive:
            self.engine = LifeEngine()
            self._initialized = True
            if not self.engine.alive: # Only log if it's a forced reset after death
                self.engine.log("Starting a new life...")
            self._death_dialog_shown = False # Reset flag for death dialog

        self.build_ui()
        self.update_ui() # Initial UI update

    def build_ui(self):
        self.clear_widgets()
        
        main_layout = MDBoxLayout(orientation='vertical')

        # Top Bar for stats
        stats_toolbar = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="120dp",
            padding=10,
            spacing=10,
            md_bg_color=(0.1, 0.1, 0.1, 1)
        )
        
        # Left side stats (age, money, job)
        left_stats_layout = MDBoxLayout(orientation='vertical', size_hint_x=0.4)
        self.lbl_age = MDLabel(text="AGE: 0", font_style="H5", theme_text_color="Custom", text_color=(1,1,1,1))
        self.lbl_money = MDLabel(text="$0", font_style="H6", theme_text_color="Custom", text_color=(0,1,0,1))
        self.lbl_job = MDLabel(text="Unemployed", theme_text_color="Secondary", size_hint_y=None, height="20dp", font_style="Caption")
        left_stats_layout.add_widget(self.lbl_age)
        left_stats_layout.add_widget(self.lbl_money)
        left_stats_layout.add_widget(self.lbl_job)
        stats_toolbar.add_widget(left_stats_layout)

        # Right side stats (health, smarts, looks, happiness, karma)
        right_stats_grid = MDGridLayout(cols=2, spacing=5, size_hint_x=0.6)
        
        self.lbl_health = MDLabel(text="Health: 100%", font_style="Body2")
        self.lbl_smarts = MDLabel(text="Smarts: 0", font_style="Body2")
        self.lbl_looks = MDLabel(text="Looks: 0", font_style="Body2")
        self.lbl_happiness = MDLabel(text="Happiness: 0", font_style="Body2")
        self.lbl_karma = MDLabel(text="Karma: 0", font_style="Body2")

        right_stats_grid.add_widget(self.lbl_health)
        right_stats_grid.add_widget(self.lbl_smarts)
        right_stats_grid.add_widget(self.lbl_looks)
        right_stats_grid.add_widget(self.lbl_happiness)
        right_stats_grid.add_widget(self.lbl_karma)
        stats_toolbar.add_widget(right_stats_grid)

        main_layout.add_widget(stats_toolbar)

        # Log History
        self.log_scroll = MDScrollView(size_hint_y=0.7)
        self.log_list = MDList()
        self.log_scroll.add_widget(self.log_list)
        main_layout.add_widget(self.log_scroll)

        # Bottom Action Bar
        action_bar = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height="60dp",
            md_bg_color=(0.1, 0.1, 0.1, 1),
            padding=5,
            spacing=5
        )
        action_bar.add_widget(MDFillRoundFlatButton(text="ACTIVITIES", on_release=self.show_activities_menu))
        action_bar.add_widget(MDFillRoundFlatButton(text="RELATIONS", on_release=self.show_relationships_menu))
        action_bar.add_widget(MDFillRoundFlatButton(text="WORK", on_release=self.show_work_menu))
        action_bar.add_widget(MDFillRoundFlatButton(text="EDUCATION", on_release=self.show_education_menu))
        action_bar.add_widget(MDFillRoundFlatButton(text="HEALTH", on_release=self.show_health_menu))
        main_layout.add_widget(action_bar)

        # Age Up Button (Prominently placed, BitLife style)
        age_btn = MDFillRoundFlatButton(
            text="AGE UP",
            size_hint=(1, None),
            height="60dp",
            on_release=self.do_age,
            md_bg_color=self.theme_cls.primary_color
        )
        main_layout.add_widget(age_btn)
        
        self.add_widget(main_layout)
        self.engine.dialog_instance = None # Ensure dialog is reset

    def update_ui(self):
        e = self.engine
        self.lbl_age.text = f"AGE: {e.age}"
        self.lbl_money.text = f"${e.money:,}"
        self.lbl_job.text = e.job['title'] if e.job else "Unemployed"
        self.lbl_health.text = f"Health: {e.health}%"
        self.lbl_smarts.text = f"Smarts: {e.smarts}"
        self.lbl_looks.text = f"Looks: {e.looks}"
        self.lbl_happiness.text = f"Happiness: {e.happiness}"
        self.lbl_karma.text = f"Karma: {e.karma}"

        # Update text color based on value for health, happiness, karma
        if e.health < 30: self.lbl_health.text_color = (1,0,0,1) # Red
        elif e.health < 60: self.lbl_health.text_color = (1,0.5,0,1) # Orange
        else: self.lbl_health.text_color = (0,1,0,1) # Green

        if e.happiness < 30: self.lbl_happiness.text_color = (1,0,0,1) # Red
        elif e.happiness < 60: self.lbl_happiness.text_color = (1,1,0,1) # Yellow
        else: self.lbl_happiness.text_color = (0,1,0,1) # Green
        
        if e.karma < 30: self.lbl_karma.text_color = (1,0,0,1) # Red
        elif e.karma < 60: self.lbl_karma.text_color = (1,1,0,1) # Yellow
        else: self.lbl_karma.text_color = (0,1,0,1) # Green

        # Update log history
        self.log_list.clear_widgets()
        for txt in e.log_history[:30]: # Show latest 30 logs
            self.log_list.add_widget(TwoLineListItem(text=txt, secondary_text=""))
        
        # Check for game over
        if not e.alive and not hasattr(self, '_death_dialog_shown'):
            self.show_game_over_dialog()
            self._death_dialog_shown = True # Prevent multiple dialogs

    def do_age(self, *args):
        if not self.engine.alive:
            self.show_game_over_dialog()
            return
        
        self.engine.age_up()
        self.update_ui()
        # Scroll to top of log after age up if there are new entries
        if len(self.engine.log_history) > 0 and self.log_list.children:
            self.log_scroll.scroll_y = 1 # Scroll to top

    # --- Dialog Management ---
    def show_dialog(self, title, text, buttons, dismiss_callback=None):
        if self.engine.dialog_instance: # Dismiss any existing dialog first
            self.engine.dialog_instance.dismiss()
        
        dialog_buttons = []
        for btn_text, btn_callback in buttons:
            dialog_buttons.append(
                MDFlatButton(
                    text=btn_text,
                    on_release=lambda x, cb=btn_callback: self._dialog_button_pressed(cb)
                )
            )

        self.engine.dialog_instance = MDDialog(
            title=title,
            text=text,
            buttons=dialog_buttons,
            on_dismiss=dismiss_callback
        )
        self.engine.dialog_instance.open()

    def _dialog_button_pressed(self, callback):
        if self.engine.dialog_instance:
            self.engine.dialog_instance.dismiss()
            self.engine.dialog_instance = None
        if callback:
            callback()
        self.update_ui() # Always update UI after an action via dialog

    def show_game_over_dialog(self):
        if self.engine.dialog_instance: self.engine.dialog_instance.dismiss()
        self.engine.dialog_instance = MDDialog(
            title="GAME OVER",
            text=f"You died at age {self.engine.age}.\nYour final money was ${self.engine.money:,}.\n\nDo you want to start a new life?",
            buttons=[
                MDFlatButton(
                    text="NEW LIFE",
                    on_release=self.start_new_game
                )
            ],
            on_dismiss=lambda x: self.start_new_game(x) # Ensure it dismisses and restarts even if closed
        )
        self.engine.dialog_instance.open()

    def start_new_game(self, *args):
        self._initialized = False # Force re-initialization of the engine
        self._death_dialog_shown = False # Reset flag for next game
        if self.engine.dialog_instance:
            self.engine.dialog_instance.dismiss()
            self.engine.dialog_instance = None
        self.on_enter() # Re-enter the screen to build/reset everything


    # --- Action Menus (using Dialogs) ---

    def show_activities_menu(self, *args):
        if not self.engine.alive: return
        self.show_dialog(
            "Activities",
            "What would you like to do?",
            [
                ("Study (Smarts)", self.engine.study),
                ("Go to Gym (Health, Looks)", self.engine.go_to_gym),
                ("Meditate (Happiness, Karma)", self.engine.meditate),
                ("Commit Petty Crime (Money, Karma)", self.engine.commit_petty_crime),
                ("Cancel", None)
            ]
        )

    def show_relationships_menu(self, *args):
        if not self.engine.alive: return
        relation_items = [
            (f"{r['name']} ({r['type'].capitalize()}) - {r['status']}", 
             lambda r=r: self.engine.interact_with_relationship(r) if r['status'] == 'Alive' else self.engine.log(f"{r['name']} is deceased."))
            for r in self.engine.relationships
        ]
        relation_items.append(("Cancel", None))

        self.show_dialog(
            "Relationships",
            "Who would you like to interact with?",
            relation_items
        )

    def show_work_menu(self, *args):
        if not self.engine.alive: return
        job_options = []
        if not self.engine.job:
            job_options = [
                ("Apply: Janitor ($25K, 20 Smarts)", lambda: self.engine.apply_for_job("Janitor", 25000, 20)),
                ("Apply: Retail Clerk ($30K, 30 Smarts)", lambda: self.engine.apply_for_job("Retail Clerk", 30000, 30)),
                ("Apply: Developer ($60K, 60 Smarts, University Degree)", lambda: self.engine.apply_for_job("Developer", 60000, 60, "University Degree")),
            ]
        else:
            job_options = [
                ("Resign from Job", self.engine.resign_from_job)
            ]
        job_options.append(("Cancel", None))

        job_info = f"Current Job: {self.engine.job['title']}\nSalary: ${self.engine.job['salary']:,}\nLevel: {self.engine.job['level']}" if self.engine.job else "Currently Unemployed."
        
        self.show_dialog(
            "Work",
            job_info,
            job_options
        )
    
    def show_education_menu(self, *args):
        if not self.engine.alive: return
        edu_options = []
        
        current_status = f"Current: {self.engine.school_level}"
        completed_status = f"Completed: {', '.join(self.engine.education_completed) or 'None'}"

        if self.engine.age < 18:
            edu_options.append(("You are currently in school (Automatic progress)", None))
        elif "High School Diploma" not in self.engine.education_completed:
            edu_options.append(("Graduate High School (Automatic at 18)", None))
        elif self.engine.school_level != "University" and "University Degree" not in self.engine.education_completed:
            edu_options.append(("Enroll in University (-$10,000)", lambda: self.engine.go_to_university()))
        elif self.engine.school_level == "University" and "University Degree" not in self.engine.education_completed: # If enrolled but not graduated
            edu_options.append(("Graduate University", lambda: self.engine.graduate_university()))
        else: # All education completed for now
            edu_options.append(("No further education options available.", None))
        
        edu_options.append(("Cancel", None))

        self.show_dialog(
            "Education",
            f"{current_status}\n{completed_status}",
            edu_options
        )

    def show_health_menu(self, *args):
        if not self.engine.alive: return
        self.show_dialog(
            "Health",
            "What would you like to do about your health?",
            [
                ("Go to Doctor (-$500)", self.engine.visit_doctor),
                ("Cancel", None)
            ]
        )


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        
        # The GameScreen itself serves as the main interactive screen,
        # where game actions and stats are managed, similar to BitLife's main interface.
        return GameScreen()

if __name__ == "__main__":
    MainApp().run()