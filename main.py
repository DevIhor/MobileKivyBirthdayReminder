import datetime

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.picker import MDDatePicker

from settings import Settings

# Window.size = (360, 780)
from utils import calculate_age

Window.size = (400, 780)


class AddBirthdayScreen(Screen):
    def __init__(self, **kwargs):
        super(AddBirthdayScreen, self).__init__(**kwargs)
        self.store = JsonStore("data/data.json")
        self.people = self.store.get('others').get('people') if self.store.exists('others') else []
        now = datetime.datetime.now()
        self.person = {
            "year": now.year,
            "month": now.month,
            "day": now.day
        }

    def on_save(self):
        self.person["name"] = self.ids.name.text
        self.person["surname"] = self.ids.surname.text
        self.people.append(self.person)
        self.store.put("others", people=self.people)
        pass

    def on_date_dialog_save(self, instance, value, date_range):
        self.person["year"] = value.year
        self.person["month"] = value.month
        self.person["day"] = value.day

    def on_date_dialog_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_dialog_save, on_cancel=self.on_date_dialog_cancel)
        date_dialog.open()


class ItemBackdropFrontLayer(TwoLineAvatarListItem):
    text = StringProperty()
    secondary_text = StringProperty()


class AgeBackdropLayer(BoxLayout):
    def __init__(self, **kwargs):
        super(AgeBackdropLayer, self).__init__(**kwargs)
        self.store = JsonStore("data/data.json")
        self.birthday_date = None
        Clock.schedule_once(self.load, 0.1)

    def load(self, *args):
        if self.store.exists('me'):
            birthday = self.store.get('me')
            self.birthday_date = datetime.datetime(birthday.get("year"), birthday.get("month"), birthday.get("day"))
            self.ids.age.text = calculate_age(self.birthday_date)
            self.ids.change_age_btn.text = "CHANGE"
        else:
            self.ids.age.text = "You haven't set your birthday yet!"
            self.ids.change_age_btn.text = "SET"

    def on_date_dialog_save(self, instance, value, date_range):
        self.store.put('me', year=value.year, month=value.month, day=value.day)
        self.load()

    def on_date_dialog_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        if self.birthday_date:
            date_dialog = MDDatePicker(self.birthday_date.year, self.birthday_date.month, self.birthday_date.day)
        else:
            date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_dialog_save, on_cancel=self.on_date_dialog_cancel)
        date_dialog.open()


class BirthdaysBackdropLayer(BoxLayout):
    def __init__(self, **kwargs):
        super(BirthdaysBackdropLayer, self).__init__(**kwargs)
        self.store = JsonStore("data/data.json")
        Clock.schedule_once(self.load, 0.1)

    def load(self, *args):
        if self.store.exists('others'):
            people = self.store.get('others').get('people')
            for person in people:
                title = f"{person.get('name')} {person.get('surname')}"
                birthday_date = datetime.datetime(person.get("year"), person.get("month"), person.get("day"))
                info = f"{birthday_date.strftime('%d.%m.%Y')} ({calculate_age(birthday_date)})"
                self.ids.scroll.add_widget(
                    ItemBackdropFrontLayer(text=title, secondary_text=info)
                )


class BirthdayApp(MDApp):
    def on_start(self):
        if Settings.DEBUG:
            self.fps_monitor_start()


if __name__ == "__main__":
    BirthdayApp().run()
