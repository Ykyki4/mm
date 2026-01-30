import httpx
from kivy.app import App
from kivy.core.text import Text
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window


Window.size = (400, 500)
Window.clearcolor = (0.95, 0.95, 1, 1)
API_URL = "https://grumpily-immediate-armadillo.cloudpub.ru"


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        layout = GridLayout(cols=2)

        # Add widgets for the form
        layout.add_widget(Label(text='User Name:', color="#00000"))
        self.username = TextInput(
            multiline=False,
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.username)

        layout.add_widget(Label(text='Password:', color="#00000"))
        self.password = TextInput(
            password=True,
            multiline=False,
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.password)

        # Add a submit button spanning two columns
        self.submit_button = Button(text='Login', size_hint_y=None, height=40)
        self.submit_button.bind(on_press=self.do_login)
        layout.add_widget(self.submit_button)

        self.add_widget(layout)

    def do_login(self, instance):
        app = App.get_running_app()

        json = {
            "username": self.username.text,
            "password": self.password.text,
        }
        response = httpx.post(f"{API_URL}/users/login", json=json)
        if response.status_code == 200:
            app.current_user = {"username": response.json()['username']}
            app.root.current = 'profile'

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""


class ProfilePage(Screen):
    def __init__(self, **kwargs):
        super(ProfilePage, self).__init__(**kwargs)

        # Add widgets for the form
        self.text = Label(text='User Name:', color="#00000")
        self.add_widget(self.text)

    def on_enter(self, *args):
        user = App.get_running_app().current_user
        if user:
            self.text.text = f"User Name: {user}"


class DesktopApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        screen = ScreenManager()
        screen.add_widget(LoginPage(name='login'))
        screen.add_widget(ProfilePage(name='profile'))
        return screen


if __name__ == '__main__':
    DesktopApp().run()