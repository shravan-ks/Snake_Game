import tkinter as tk
from random import randint

from PIL import Image, ImageTk

MOVE_INCREMENT = 20
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width = 800, height= 820, background='black',highlightthickness=0)

        self.snake_positions = [(100,100),(80,100),(60,100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = 'Right'
        self.bind_all("<Key>", self.on_key_press)

        self.load_assests()
        self.create_object()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assests(self):
        try:
            self.snake_body_image = Image.open('./images/snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('./images/food.png')
            self.food = ImageTk.PhotoImage(self.food_image)

        except IOError as error:
            print(error)
            root.destroy()

    def create_object(self):
        self.create_text(
            100,12, text=f"Score: {self.score} Speed: {moves_per_second}",tag='score',fill='#fff',font=('TkDefaultFont', 14)
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag='snake')

        self.create_image(*self.food_position, image=self.food, tag='food')
        self.create_rectangle(7,27,793,813, outline="#525d69")

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == 'Left':
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Right':
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Down':
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == 'Up':
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)


    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (
            head_x_position in (0,800)
            or head_y_position in (20,820)
            or (head_x_position,head_y_position) in self.snake_positions[1:]
        )

    def on_key_press(self,e):
        new_direction = e.keysym
        all_directions = ('Up','Down','Left','Right')
        opposites = ({'Up','Down'},{'Left','Right'})
        if (
            new_direction in all_directions
            and {new_direction, self.direction}not  in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag('food'),self.food_position)

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag='snake'
            )

            score = self.find_withtag('score')
            self.itemconfigure(score, text=f"Score: {self.score} Speed: {moves_per_second}", tag='score')

    def set_new_food_position(self):
        while True:
            x_position = randint(1,39) * MOVE_INCREMENT
            y_position = randint(3, 40)* MOVE_INCREMENT
            food_position = (x_position,y_position)

            if food_position not in self.snake_positions:
               return food_position

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text = f"Game over ! You Scored {self.score}!",
            fill='#fff',
            font=('TkDefaultFont', 24)
        )



root = tk.Tk()
root.title("Snake Game")
root.wm_iconbitmap('./images/Icon.ico')
root.resizable(False,False)

board = Snake()
board.pack()

root.mainloop()