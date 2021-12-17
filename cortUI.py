import time
from dataclasses import dataclass
from collections import deque

from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton

#TODO: fix the dialog window

#look here for docs: C:\Andi_Arbeit\Programmieren\cort\kivy_venv\Lib\site-packages\kivymd\uix
#look here for icons: https://materialdesignicons.com/

@dataclass
class Person:
    name : str
    start_time : float 
    status : str

persons = deque([])
overview = deque([])

#time in seconds
TEST_TIME = 15 * 60


KV = '''
<MDRaisedButton>
    md_bg_color: app.theme_cls.primary_color
    text_color: app.theme_cls.opposite_bg_dark

<MDFlatButton>
    text_color: app.theme_cls.opposite_bg_dark

#this doesnt work 
<Add_dialog_content>
    size_hint_y: None
    MDTextField:
        hint_text: "Enter a name"
        helper_text: "This will disappear when you click off"
        helper_text_mode: "on_focus"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

MDScreen:
    ScrollView:

        MDList:
            id: container

    MDToolbar:
        title: "Cort"
        right_action_items: [["plus", lambda x: app.callback_plus()], ["cog-outline", lambda x: app.callback_cog()]]
'''

dialog_content_add = """
<Dialog_content_add>:
    name: name
    orientation: 'vertical'
    spacing: 12
    size_hint_y: None 
    height: 25 

    MDTextField:
        id: name
        hint_text: "Enter a name"
        helper_text: ""
        helper_text_mode: "on_focus"
"""
class Cort(MDApp):

    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"

        Clock.schedule_interval(self.update, 1)

        Builder.load_string(dialog_content_add)
        return Builder.load_string(KV) 

    #just for testing
    def on_start(self):
        self.add_person('Günter', time.time(), 'undefined')
        self.add_person('Jauch', time.time(), 'undefined')


    def callback_plus(self):
        if not self.dialog:
            self.dialog = MDDialog(
                type="custom",
                content_cls=Dialog_content_add(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=self.callback_CANCEL
                    ),
                    MDRaisedButton(
                        text="OK",
                        on_release=self.callback_OK
                    ),
                ],
            )
            self.dialog.open()

    def callback_CANCEL(self, obj):
        self.dialog.dismiss(force=True)
        self.dialog = None

    def callback_OK(self, obj):
        name = self.dialog.content_cls.name.text
        self.add_person(name, time.time(), 'undefined')

        self.dialog.dismiss(force=True)
        self.dialog = None

    def add_person(self, name, start_time, status):
        person = Person(name, start_time, status)
        persons.appendleft(person)
        time_left = (TEST_TIME - (time.time() - person.start_time)) / 60
        self.root.ids.container.add_widget(
            ThreeLineListItem(
                text = f"{name}",
                secondary_text = f"time: {time_left: .1f}min",
                tertiary_text = f"status: {status}"
            )
        )

    def update(self, obj):
        displayed_persons = self.root.ids.container.children
        i = len(persons) - 1
        while i >= 0:

            time_left = (TEST_TIME - (time.time() - persons[i].start_time)) / 60

            if time_left <= 0:
                print(f'{persons[i].name}\'s time is up')
                overview.appendleft(persons[i])
                self.root.ids.container.remove_widget(displayed_persons[i])
                del persons[i]

            else:
                displayed_persons[i].secondary_text = f"time: {time_left: .1f}min"

            i -= 1

    def callback_cog(self):
        raise NotImplementedError

class Dialog_content_add(MDBoxLayout):
    pass

if __name__ == "__main__":
    Cort().run()