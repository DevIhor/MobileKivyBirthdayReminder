from kivy.clock import Clock
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarListItem

from settings import Settings

# Window.size = (360, 780)
Window.size = (400, 780)


class BirthdaysBackdropLayer(TwoLineAvatarListItem):
    pass


class AgeBackdropLayer(BoxLayout):
    def __init__(self, **kwargs):
        super(AgeBackdropLayer, self).__init__(**kwargs)
        self.store = JsonStore("age.json")
        Clock.schedule_once(self.load, 0.1)

    def save(self):
        self.store.put('profile', age=self.ids.age.text)

    def load(self, *args):
        if self.store.exists('profile'):
            profile = self.store.get('profile')
            age = profile.get("age") or 0
            self.ids.age.text = age
        else:
            self.ids.age.text = "You haven't set your birthday yet!"


class BirthdayBackdropLayer(Screen):
    def __init__(self, **kwargs):
        super(BirthdayBackdropLayer, self).__init__(**kwargs)


class AgeBackdrop(Screen):
    def __init__(self, **kwargs):
        super(AgeBackdrop, self).__init__(**kwargs)


class SetAgeScreen(Screen):
    def __init__(self, **kwargs):
        super(SetAgeScreen, self).__init__(**kwargs)


class BirthdayApp(MDApp):
    def on_start(self):
        if Settings.DEBUG:
            self.fps_monitor_start()


if __name__ == "__main__":
    BirthdayApp().run()
