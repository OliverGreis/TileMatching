import turtle

pen = turtle.Turtle()


pen.pu()
pen.pd()




def draw_triangle(length):
    pen.setheading(180)      # set the direction of the pen to left
    for i in range(3):       # draw 3 sides
        pen.rt(120)          # rotate the pen 120 degrees clockwise
        pen.fd(length)       # draw side
                             # pen will end facing left (180)
