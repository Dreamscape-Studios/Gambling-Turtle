import turtle

dice_button = turtle.Turtle()
dice_button.shape("square")
exit_button = turtle.Turtle()
exit_button.shape("square")
exit_button.color("red")
exit_button.setx(100)
exit_button.sety(100)

def clicked(x, y):
    print("thing")

def close_window(x, y):
    turtle.bye()

turtle.listen()

dice_button.onclick(clicked)
exit_button.onclick(close_window)

turtle.mainloop()