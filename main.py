from kivy.app import App
from kivy.uix.label import Label

class HelloWorldApp(App):
    def build(self):
        self.title = 'Hello World App'
        return Label(text='Hello World!', font_size='40sp')

if __name__ == '__main__':
    HelloWorldApp().run()
