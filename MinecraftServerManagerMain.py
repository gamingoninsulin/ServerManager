# MinecraftServerManager.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from MinecraftServerHandler import MinecraftServerHandler
from MinecraftColorCodeParser import MinecraftColorCodeParser


class MinecraftServerManager(BoxLayout):
    def __init__(self, **kwargs):
        super(MinecraftServerManager, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.server_handler = MinecraftServerHandler(self.insert_console_output)
        self.console_output = Label(size_hint_y=None, height=200)
        self.add_widget(self.console_output)
        self.console_input = TextInput(multiline=False)
        self.console_input.bind(on_text_validate=self.on_enter)
        self.add_widget(self.console_input)
        self.start_button = Button(text='Start')
        self.start_button.bind(on_press=self.start_server)
        self.add_widget(self.start_button)
        # Add more buttons and bind them to their respective functions...

    def on_enter(self, instance):
        self.console_input.text = ''

    def insert_console_output(self, output):
        parsed_output = MinecraftColorCodeParser.parse_color_codes(output)
        self.console_output.text += parsed_output + '\n'

    def start_server(self, instance):
        self.server_handler.start_server()


class MyApp(App):
    def build(self):
        return MinecraftServerManager()


if __name__ == '__main__':
    MyApp().run()
