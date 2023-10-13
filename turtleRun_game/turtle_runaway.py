# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner1, runner2, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner1 = runner1
        self.runner2 = runner2
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.score = 0
        # Initialize 'runner' and 'chaser'
        self.runner1.shape('turtle')
        self.runner1.color('blue')
        self.runner1.penup()

        self.runner2.shape('turtle')
        self.runner2.color('green')
        self.runner2.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate an another turtle for drawing
        self.drawer1 = turtle.RawTurtle(canvas)
        self.drawer1.hideturtle()
        self.drawer1.penup()
        self.drawer2 = turtle.RawTurtle(canvas)
        self.drawer2.hideturtle()
        self.drawer2.penup()
        self.timer = 60
        self.drawEnd = turtle.RawTurtle(canvas)
        self.drawEnd.hideturtle()
        self.drawEnd.penup()

    def is_catched1(self):
        p = self.runner1.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    def is_catched2(self):
        p = self.runner2.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner1.setpos((-init_dist / 2, -50))
        self.runner1.setheading(0)
        self.runner2.setpos((-init_dist / 2, +50))
        self.runner2.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        self.print_score()
        # TODO) You can do something here and follows.
        
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner1.run_ai(self.chaser.pos(), self.chaser.heading())
        self.runner2.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner1.pos(), self.runner1.heading())
        self.chaser.run_ai(self.runner2.pos(), self.runner2.heading())

        # TODO) You can do something here and follows.
        if self.is_catched1():
            self.score += 1
            self.reset_positions()
            self.print_score()
            if self.score == 10:
                self.drawEnd.undo()
                self.drawEnd.penup()
                self.drawEnd.setpos(-200, 0)
                self.drawEnd.write(f'Game Clear!', font=("Arial", 50, "normal"))
                self.game_over()
        if self.is_catched2():
            if (self.score != 0):
                self.score -= 1
            self.reset_positions()
            self.print_score()
                
        self.timer -= 0.16
        self.print_timer()

        if self.timer <= 0:
            self.drawEnd.undo()
            self.drawEnd.penup()
            self.drawEnd.setpos(-200, 0)
            self.drawEnd.write(f'Game Over!', font=("Arial", 50, "normal"))
            self.game_over()
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def reset_positions(self):
        self.runner1.setpos(-200, -50)
        self.runner2.setpos(-200, 50)
        self.chaser.setpos(200, 0)

    def print_score(self):
        self.drawer1.undo()
        self.drawer1.penup()
        self.drawer1.setpos(-300, 300)
        self.drawer1.write(f'Score: {self.score}', align="left", font=("Arial", 20, "normal"))  

    def print_timer(self):
        self.drawer2.undo()
        self.drawer2.penup()
        self.drawer2.setpos(200, 300)
        self.drawer2.write(f'Time: {int(self.timer)}', align="right", font=("Arial", 20, "normal"))

    def game_over(self):
        time.sleep(3)
        quit()

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner1 = RandomMover(screen)
    runner2 = RandomMover(screen)
    chaser = ManualMover(screen)

    game = RunawayGame(screen, runner1, runner2, chaser)
    game.start()
    screen.mainloop()