# импорт классов
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (300, 690)
Window.title = 'my Random'

class MenuScreen(Screen):  # класс-наследник
    def __init__(self, **kw):  # конструктор
        super(MenuScreen, self).__init__(**kw)  # наследование свойств из супер-класса
        self.box = BoxLayout(orientation='vertical')
        self.main_text = Label(text='my RANDOM')
        self.image_food = Image(source='food.jpg')
        self.food_text = Label(text='Блюдо')
        self.image_sound = Image(source='sound.jpeg')
        self.sound_text = Label(text='Случайный звук')
        self.image_cube = Image(source='кубик.jpg')
        self.cube_text = Label(text='Бросить кубик')
        self.box.add_widget(self.main_text)
        self.box.add_widget(self.image_food)
        self.box.add_widget(self.food_text)
        self.box.add_widget(self.image_sound)
        self.box.add_widget(self.sound_text)
        self.box.add_widget(self.image_cube)
        self.box.add_widget(self.cube_text)
        self.add_widget(self.box)

sm = ScreenManager()
sm.add_widget(MenuScreen())

class MyApp(App):  # класс-наследник
    # построение программы
    def build(self):
        return sm

MyApp().run()  # запускаем приложение