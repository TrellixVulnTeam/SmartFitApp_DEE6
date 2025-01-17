from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.app import App
import kivy.utils

class WorkoutGrid(GridLayout):
    rows = 1

    #If the heart button is double clicked on the friend workout screen it will add a 'like' to the workout
    def on_touch_down(self, touch):
        if self.can_like:
            if touch.is_double_tap:
                if self.collide_point(*touch.pos):
                    app = App.get_running_app()
                    likes = self.right_label.text.split(" ")[0]
                    likes = str(int(likes) + 1)
                    self.right_label.text = likes + " " + " ".join(self.right_label.text.split(" ")[1:])

                    friends_id = App.get_running_app().friends_id
                    app.authentication.update_likes(friends_id, self.workout_key, likes)

    def __init__(self, **kwargs):
        try:
            self.can_like = kwargs['can_like']
            self.workout_key = kwargs['workout_key']
        except:
            self.can_like = False
            self.workout_key = ""

        super().__init__()
        with self.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex("#d5d5d5"))) #Change Background Colour Of Workout Banner
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect, size=self.update_rect) #Anytime the size of the banner changes then it will call 'update_rect' to update the size and pos of banner

        #Left Float
        left = FloatLayout()
        left_image = Image(source="icons/workout/" + kwargs['Workout_Image'], size_hint=(1, 0.7), pos_hint={"top":0.95, "right":1})
        left_label = Label(text=kwargs['Description'], size_hint=(1, 0.2), pos_hint={"top":.225, "right":1}, font_name= "Alphakind", color= (0,0,0,1))

        left.add_widget(left_image)
        left.add_widget(left_label)

        #Middle Float
        middle = FloatLayout()
        date = Label(text=kwargs['Date'], size_hint=(1, .2), pos_hint={"top": .975, "right": 1}, font_name="Alphakind", color= (0,0,0,1))
        middle_image = Image(source=kwargs['Unit_Image'], size_hint=(1, 0.5), pos_hint={"top":0.75, "right":1})
        middle_label = Label(text=str(kwargs['Amount']) + " " + kwargs['Units'], size_hint=(1, 0.2), pos_hint={"top":.225, "right":1}, font_name= "Alphakind", color= (0,0,0,1))

        middle.add_widget(middle_image)
        middle.add_widget(middle_label)
        middle.add_widget(date)

        #Right Float
        right = FloatLayout()
        right_image = Image(source="icons/heart.png", size_hint=(1, 0.5), pos_hint={"top": 0.75, "right":1})
        self.right_label = Label(text=str(kwargs['Likes']), size_hint=(1, 0.2), pos_hint={"top":.225, "right":1}, font_name="Alphakind", color= (0,0,0,1))

        right.add_widget(right_image)
        right.add_widget(self.right_label)

        self.add_widget(left)
        self.add_widget(middle)
        self.add_widget(right)

    #Updates size of banner when the size changes
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size