from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

from settings import Settings


class AgeBackdrop(Screen):
    def __init__(self, **kwargs):
        super(AgeBackdrop, self).__init__(**kwargs)

    def get_age(self):
        self.ids.age_label.text = "Hello"


class BirthdayApp(MDApp):
    def build(self):
        return AgeBackdrop()

    def on_start(self):
        if Settings.DEBUG:
            self.fps_monitor_start()


if __name__ == "__main__":
    BirthdayApp().run()
