#snake.py

from tkinter import *
from PIL import Image, ImageTk
import random
# pip install pillow

MOVE_INCREMENT = 20
MOVE_PER_SECOND = 10
GAME_SPEED = 1000 // MOVE_PER_SECOND

class Snake(Canvas):
    def __init__(self):
        super().__init__(width = 600, height = 620, background = 'black', highlightthickness = 0)

        self.reset = [(100, 100), (80, 100), (60, 100)]
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.loop = None
        self.direction = 'Right'

        self.bind_all('<Key>', self.on_key_press)
        
        self.load_assets()
        self.create_objects()
        self.rungame()
        self.starting = True

    def load_assets(self):
        self.snake_body_image = Image.open('./assets/body.png')
        self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

        self.food_image = Image.open('./assets/food.png')
        self.food = ImageTk.PhotoImage(self.food_image)

    def create_objects(self):
        #create score text
        FONT = (None, 14)
        self.create_text(45, 12, text = 'Score: {}'.format(self.score), tag = 'score', fill = 'white', font = FONT)

        #create snake body
        for x_pos , y_pos in self.snake_positions:
            self.create_image(x_pos, y_pos, image = self.snake_body, tag = 'snake')

        #create food
        self.create_image(self.food_position[0], self.food_position[1], image = self.food, tag = 'food')
        self.create_rectangle(7, 27, 593, 613, outline = '#FFF')

    def move_snake(self):
        head_x , head_y = self.snake_positions[0]

        if self.direction == 'Up':
            new_head_pos = (head_x, head_y - MOVE_INCREMENT)
        elif self.direction == 'Down':
            new_head_pos = (head_x, head_y + MOVE_INCREMENT)
        elif self.direction == 'Right':
            new_head_pos = (head_x + MOVE_INCREMENT, head_y)
        elif self.direction == 'Left':
            new_head_pos = (head_x - MOVE_INCREMENT, head_y)

        self.snake_positions = [new_head_pos] + self.snake_positions[:-1]

        findsnake = self.find_withtag('snake') # find old body
        for segment, pos in zip(findsnake, self.snake_positions):
            self.coords(segment, pos)

    def rungame(self):
        if self.check_collisions() and self.starting == True:
            # when collisions
            self.after_cancel(self.loop)
            self.starting = False
            self.delete('all')
            self.create_text(300, 300, justify = CENTER,
                             text = f'GAME OVER\n\nScore: {self.score}\n\nNew Game <F1>',
                             fill = 'yellow', font = (None, 30))
        elif self.check_collisions() and self.starting == False:
            # when press F1
            self.delete('all')
            self.snake_positions = self.reset
            self.food_position = self.set_new_food_position()
            self.create_objects()
            self.starting = True
            self.direction = 'Right'
            self.score = 0
            self.loop = self.after(GAME_SPEED, self.rungame)
        else:
            # when moving
            self.check_food_collisions()
            self.move_snake()
            self.loop = self.after(GAME_SPEED, self.rungame) # loopgame

    def on_key_press(self, e):
        new_direction = e.keysym # key pressed

        all_direction = ('Up', 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'}, {'Left', 'Right'})

        if (new_direction in all_direction and {new_direction, self.direction} not in opposites):
            self.direction = new_direction
        elif new_direction == 'F1':
            self.rungame()

    def check_collisions(self):
        head_x , head_y = self.snake_positions[0]

        return (head_x in (0, 600) or head_y in (20, 620) or (head_x, head_y) in self.snake_positions[1:])

    def check_food_collisions(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(*self.snake_positions[-1], image = self.snake_body, tag = 'snake')

            score = self.find_withtag('score')
            self.itemconfigure(score, text = 'Score: {}'.format(self.score))

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag('food'), self.food_position)

    def set_new_food_position(self):
        while True:
            x_pos = random.randint(1, 29) * MOVE_INCREMENT
            y_pos = random.randint(2, 30) * MOVE_INCREMENT
            food_position = (x_pos, y_pos)
            if food_position not in self.snake_positions:
                return food_position


GUI = Tk()
GUI.title('Snake Game by nomomon')
GUI.resizable(False, False)

game = Snake()
game.pack()

GUI.mainloop()