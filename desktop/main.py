import json

from kivy.app import App
from kivy.core.text import Text
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, SlideTransition, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import platform

Window.clearcolor = (0.95, 0.95, 1, 1)
API_URL = "http://10.0.2.2:8001"


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super(LoginPage, self).__init__(**kwargs)
        layout = GridLayout(cols=1)

        self.label = Label(text='Login', color="#00000")
        layout.add_widget(self.label)

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

        json_data = {
            "username": self.username.text,
            "password": self.password.text,
        }
        data = json.dumps(json_data)  # Data must be a string
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.make_request(data, headers)


    def make_request(self, data, headers):
        url = f"{API_URL}/users/login"
        req = UrlRequest(url,
                         on_success=self.on_success,
                         on_failure=self.on_failure,
                         on_error=self.on_error,
                         on_redirect=self.on_redirect,
                         req_body=data,
                         req_headers=headers,
                         method='POST',
                         )
        print(req)

    def on_success(self, req, result):
        app = App.get_running_app()
        # This function is called when the request is successful
        # The 'result' is automatically decoded from JSON if the Content-Type is application/json
        print(result)
        app.current_user = {"username": result['username']}
        app.root.current = 'profile'

    def on_failure(self, req, result):
        # This function is called if the request fails
        self.label.text = "Request failed."
        print(f"Request failed. Result: {result}")

    def on_error(self, req, error):
        # This function is called if an error occurs during the request
        self.label.text = f"An error occurred: {error}"
        print(f"An error occurred: {error}")

    def on_redirect(self, req, result):
        # This function is called if the request is redirected
        self.label.text = "Request redirected."
        print(f"Request redirected. Result: {result}")

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
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                             Permission.READ_EXTERNAL_STORAGE,
                             Permission.INTERNET])
    DesktopApp().run()
