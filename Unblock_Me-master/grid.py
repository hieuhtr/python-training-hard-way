# Course: CS 1MD3
# Name:  Malik Saim (Last, First)
# Student number: 1321796
# File: assgn4.py
# Description: A program using the graphics module to create a GUI of a 6x6 grid
#              and allow the user to select, highlight/unhighlight boxes

#Import everything from the graphics module
from graphics import *

#Function that creates the outer grey part (based on the x,y refrence points)
#The entire outer part is 8 pixels thick
def outline(x,y,win):
    #Drawing the outer top rectangle
    outer_rect_top = Rectangle(Point(x-8,y-8), Point(x+248,y))
    outer_rect_top.setFill("grey")
    outer_rect_top.setOutline("grey")
    outer_rect_top.draw(win)

    #Drawing the outer bottom rectangle
    outer_rect_bottom = Rectangle(Point(x-8,y+240), Point(x+248,y+248))
    outer_rect_bottom.setFill("grey")
    outer_rect_bottom.setOutline("grey")
    outer_rect_bottom.draw(win)

    #Drawing the outer left rectangle
    outer_rect_left = Rectangle(Point(x-8,y-8), Point(x,y+248))
    outer_rect_left.setFill("grey")
    outer_rect_left.setOutline("grey")
    outer_rect_left.draw(win)

    #Drawing the outer right rectangle (top half)
    outer_rect_right1 = Rectangle(Point(x+240,y-8), Point(x+248,y+80))
    outer_rect_right1.setFill("grey")
    outer_rect_right1.setOutline("grey")
    outer_rect_right1.draw(win)

    #Drawing the outer right rectangle (bottom half)
    outer_rect_right2 = Rectangle(Point(x+240,y+120), Point(x+248,y+248))
    outer_rect_right2.setFill("grey")
    outer_rect_right2.setOutline("grey")
    outer_rect_right2.draw(win)

#Function that creates the gridlines (based on the x,y refrence points)
def gridlines(x,y,win):
        #Assign initial x,y values to counters
        a, b = x, y

        #Create 5 vertical lines; each separated by 40 pixels
        for v in range(5):
            a += 40
            vertical_line = Line(Point(a,y), Point(a,y+240))
            vertical_line.setFill("grey")
            vertical_line.draw(win)

        #Create 5 horizontal lines; each separated by 40 pixels
        for h in range(5):
            b += 40
            horizontal_line = Line(Point(x,b), Point(x+240,b))
            horizontal_line.setFill("grey")
            horizontal_line.draw(win)

#Function that returns a 2-D list of top left and bottom right coordinates for each field
def coords(x,y):
    #Assign initial x,y values to counters
    a, b = x, y
    #Create a variable of type list
    lst = []

    #Go through the left column boxes and get their coordinates
    for i in range(6):
        top_left = (x,b)
        bottom_right = (x+40,b+40)
        coord = [top_left,bottom_right]
        lst.append(coord)

        #Get the coordinates of the rest of the row (i.e. 5 more boxes)
        for j in range(5):
            a += 40
            top_left = (a,b)
            bottom_right = (a+40,b+40)
            coord = [top_left,bottom_right]
            lst.append(coord)
        a = x
        b += 40

    #Return the 2-D list of both coordinates of each field
    return lst

#Function that takes a field id and returns its corresponding coordinates
def fieldCoords(x,y,fid):
    #Get the list of all the coordinates using the coords function and assign it to a variable
    fields = coords(x,y)
    #Return the element of the corresponding field id
    #(NOTE: Its fid - 1 b/c the element nums go from 0-35 instead of 1-36)
    return fields[fid - 1]

#Function that returns the field the click was made in; returns 0 if the click was outside
def checkClick(x,y,click):
    #Assign the x and y coordinates of the click to variables
    a = click.getX()
    b = click.getY()
    #Create a variable of type int
    field = -1

    #If the x or y coordinates are out of the appropriate range, return 0
    if a < x or b < y or a > x+240 or b > y+240: field = 0
    else:
        #If the coordinates are in the appropriate range, compare and check with coordinates
        #of each field
        for i in range(1,37):
            TL_xCoord = fieldCoords(x,y,i)[0][0]
            TL_yCoord = fieldCoords(x,y,i)[0][1]
            BR_xCoord = fieldCoords(x,y,i)[1][0]
            BR_yCoord = fieldCoords(x,y,i)[1][1]

            #If the coordinates are in range of a specific field, assign that field number
            #to the field variable and break out of the loop
            if (a > TL_xCoord and a < BR_xCoord) and (b > TL_yCoord and b < BR_yCoord):
                field = i
                break

    #Return the field number the click was made in (or 0)
    return field

#Function that returns a list with n number of empty lists (in this case n = 36)
def createFields(n):
    #Create a variable of type list
    lst = []
    #Loop n times and append an empty list to the actual list each time
    for i in range(n):
        lst.append([])

    #Return the resulting list
    return lst

#Function that takes the field id, the color of the box and border, the type of the border
#and either highlights/unhighlights the corresponding field with the corresponding border
#or just colors the box with the corresponding color
def e(x,y,win,fid,color,border,btype,fields):
    #Get the length of the fid'th element of the list fields
    n = len(fields[fid])

    #If the length is one (i.e. field[fid] = [r]), then undraw that rectangle and empty the list
    if n == 1:
        fields[fid].pop().undraw()
    #If the length is two (i.e. field[fid] = [r,s]), then undraw the rectangle and the border
    #and empty the list
    elif n == 2:
        fields[fid].pop().undraw()
        fields[fid].pop().undraw()

    #Get the corresponding top left and bottom right coordinates for the given field id
    #and assign them to variables
    TL_xCoord = fieldCoords(x,y,fid)[0][0]
    TL_yCoord = fieldCoords(x,y,fid)[0][1]
    BR_xCoord = fieldCoords(x,y,fid)[1][0]
    BR_yCoord = fieldCoords(x,y,fid)[1][1]

    #If the border type is '', then just create a rectangle in the fid'th field
    #with the color 'color' and set the fields[fid] values to [r]
    #Note: The outline is 'grey' so it looks like the box is "inside" the field
    if btype == '':
        r = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        r.setFill(color)
        r.setOutline("grey")
        r.draw(win)

        fields[fid] = [r]

    #If the border type is '[', then create a rectangle in the fid'th field with
    #the color 'border', create another rectangle inside so the bigger rectangle
    #looks like a '[' border and finally, set the fields[fid] value to [r,s]
    elif btype == '[':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord-1, BR_yCoord))
        s.setFill(border)
        s.setOutline(border)
        s.draw(win)

        r = Rectangle(Point(TL_xCoord+3, TL_yCoord+3), Point(BR_xCoord-1, BR_yCoord-3))
        r.setFill(color)
        r.draw(win)

        fields[fid] = [r,s]

    #Works similarly as the '[' case, except this time the border looks like ']'
    elif btype == ']':
        s = Rectangle(Point(TL_xCoord+1, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline(border)
        s.draw(win)

        r = Rectangle(Point(TL_xCoord+1, TL_yCoord+3), Point(BR_xCoord-3, BR_yCoord-3))
        r.setFill(color)
        r.draw(win)

        fields[fid] = [r,s]

    #Also works in the same way, with the border looking like '=' (i.e. border on top and bottom)
    elif btype == '=':
        s = Rectangle(Point(TL_xCoord+1, TL_yCoord), Point(BR_xCoord-1, BR_yCoord))
        s.setFill(border)
        s.setOutline(border)
        s.draw(win)

        r = Rectangle(Point(TL_xCoord+1, TL_yCoord+3), Point(BR_xCoord-1, BR_yCoord-3))
        r.setFill(color)
        r.draw(win)

        fields[fid] = [r,s]

#The main function
def main():
    #Set the x,y reference points
    x, y = 20, 20
    #Enter dimensions and title for the graphic window and assign it to a variable
    win = GraphWin("Unblock me", 280, 280)
    #Create a list of 36 empty lists using createFields function
    fields = createFields(36)

    #Create the outer grey border using the outline function by passing the x,y reference points
    #and the graphic window
    outline(x, y, win)
    #Create the grey gridlines using the gridlines function by passing the x,y reference points
    #and the graphic window
    gridlines(x,y,win)

    #Wait for the user to click before initiating the code below
    win.getMouse()

    #Run the e function on fields 8, 9 and 10 with border and fill color, 'brown'
    #(i.e. no border)
    e(x,y,win,8,'brown','brown','',fields)
    e(x,y,win,9,'brown','brown','',fields)
    e(x,y,win,10,'brown','brown','',fields)

    #Create a boolean type variable hilite, and set it to False
    hilited = False

    #Loop until the loop is broken out of
    while True:
        #Wait for the user to click before initiating the code below
        #Store the mouse click object into a variable
        click = win.getMouse()
        #Get the field number the click was made in using the checkClick function
        fclicked = checkClick(x,y,click)

        #If the click is made outside the boxes 8-10, then break out of the loop
        if fclicked < 8 or fclicked > 10: break

        #If the boxes are highlighted, unhighlight them (i.e. set border color to the fill color
        #and border type to '')
        if hilited:
            e(x,y,win,8,'brown','brown','',fields)
            e(x,y,win,9,'brown','brown','',fields)
            e(x,y,win,10,'brown','brown','',fields)
            hilited = False

        #If the boxes are not highlighted, then highlight them (i.e. set appropriate borders
        #on each box)
        else:
           e(x,y,win,8,'brown','green','[',fields)
           e(x,y,win,9,'brown','green','=',fields)
           e(x,y,win,10,'brown','green',']',fields)
           hilited = True

    #Close the graphics window
    #Note: This only executes if the loop is broken out of; in other words, if a click is made
    #outside the boxes 8-10
    win.close()

# main()
