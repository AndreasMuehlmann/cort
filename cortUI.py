from dataclasses import dataclass
from re import I

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton

#TODO: fix the dialog window

#look here for docs: C:\Andi_Arbeit\Programmieren\cort\kivy_venv\Lib\site-packages\kivymd\uix
#look here for icons: https://materialdesignicons.com/

@dataclass
class Person:
    name : str
    status : str
    time : float 

persons = [Person('Person1', 'undefined', '10:26'), Person('Person2', 'done', '12:33') ]




KV = '''
<MDRaisedButton>
    md_bg_color: app.theme_cls.primary_color
    text_color: app.theme_cls.opposite_bg_dark

<MDFlatButton>
    text_color: app.theme_cls.opposite_bg_dark

#this doesnt work 
<Add_dialog>
    MDTextField:
        hint_text: "Helper text on focus"
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

class Cort(MDApp):

    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    #just for testing
    def on_start(self):
        for person in persons:
            self.root.ids.container.add_widget(
                ThreeLineListItem(
                    text = f"{person.name}",
                    secondary_text = f"status: {person.status}",
                    tertiary_text = f"time: {person.time}"
                )
            )

    def callback_plus(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Add a new person",
                type="custom",
                content_cls=Add_dialog_content(),
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

    def callback_CANCEL(self, *args):
        self.dialog.dismiss(force=True)
        self.dialog = None

    def callback_OK(self, *args):
        #also save the entered settings and name
        self.dialog.dismiss(force=True)
        self.dialog = None



    def callback_cog(self):
        raise NotImplementedError

class Add_dialog_content(FloatLayout):
    pass

if __name__ == "__main__":
    Cort().run()