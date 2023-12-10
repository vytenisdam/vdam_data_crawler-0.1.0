from turtle import Screen, Turtle

screen = Screen()
screen.bgcolor('black')
screen.setup(width=800, height=600)
screen.title('Pong')
screen.tracer(0)
paddle1 = Turtle()
paddle1.setpos(x=350, y=0)
paddle1.penup()
paddle1.shape('square')
paddle1.color('white')
paddle1.shapesize(stretch_wid=5,stretch_len=1)
paddle1.setpos(x=350, y=0)

def move_up():
    new_y = paddle1.ycor() + 20
    if new_y >= 300:
        new_y = 300
    paddle1.goto(paddle1.xcor(), new_y)

def move_down():
    new_y = paddle1.ycor() - 20
    if new_y <= -300:
        new_y = -300
    paddle1.goto(paddle1.xcor(), new_y)

game_is_on = True

while game_is_on:
    screen.update()
    screen.listen()

    screen.onkey(move_up, 'Up')
    screen.onkey(move_down,'Down')


















    screen.exitonclick()

