# Course: CS 1MD3
# Name:  Malik Saim (Last,First)
# Student number: 1321796
# File: grid.py
# Description: Fully functional level 1 of the "Unlock Me" application

# Importing the graphics and time modules

import grid
from graphics import *


# Initializing the class Block
class Block:
    # Setting up the __init__ method/constructor with all the required parameters
    def __init__(self, x, y, win, fid, length, orien, color, fields):
        self.x = x
        self.y = y
        self.win = win
        self.fid = fid
        self.length = length
        self.orien = orien
        self.color = color
        self.fields = fields
        self.bcolor = "black"
        self.hilited = False

    # The draw method draws a horizontal or vertical box with lengths 2 or 3 based on the given field
    # It uses the e function to do the actual "drawing" of the boxes
    def draw(self):
        if self.orien == "horizontal":
            if self.length == 2:
                e(self.x, self.y, self.win, self.fid, self.color, self.bcolor, "[", self.fields)
                e(self.x, self.y, self.win, self.fid + 1, self.color, self.bcolor, "]", self.fields)
            else:
                e(self.x, self.y, self.win, self.fid, self.color, self.bcolor, "[", self.fields)
                e(self.x, self.y, self.win, self.fid + 1, self.color, self.bcolor, "=", self.fields)
                e(self.x, self.y, self.win, self.fid + 2, self.color, self.bcolor, "]", self.fields)
        else:
            if self.length == 2:
                e(self.x, self.y, self.win, self.fid, self.color, self.bcolor, "v[", self.fields)
                e(self.x, self.y, self.win, self.fid + 6, self.color, self.bcolor, "v]", self.fields)
            else:
                e(self.x, self.y, self.win, self.fid, self.color, self.bcolor, "v[", self.fields)
                e(self.x, self.y, self.win, self.fid + 6, self.color, self.bcolor, "v=", self.fields)
                e(self.x, self.y, self.win, self.fid + 12, self.color, self.bcolor, "v]", self.fields)

    # The undraw method erases the given block
    # It uses the built-in undraw function from graphics module
    def undraw(self):
        if self.orien == "horizontal":
            inc = 1
            end = self.fid + self.length
        else:
            inc = 6
            end = self.fid + (6 * (self.length))

        for i in range(self.fid, end, inc):
            self.fields[i].pop().undraw()
            self.fields[i].pop().undraw()

    # The hilite method undraws and redraws the given box with the border color changed to 'green'
    # (note: initially the border color is set to 'black' in the __init__ method)
    # It also sets the hilited value to 'True' (which is initially set to 'False')
    def hilite(self):
        self.undraw()
        self.bcolor = "green"
        self.draw()
        self.hilited = True

    # The unhilite method does the opposite of the hilite method and changes the border color of the
    # the given box to 'black' before redrawing it
    # It then sets the hilited value back to 'False'
    def unhilite(self):
        self.undraw()
        self.bcolor = "black"
        self.draw()
        self.hilited = False

    # The switchHilite method hilites the box if its not hilited and unhilites it if it is hilited
    # (note: it does the hiliting/unhiliting using the class' own methods)
    def switchHilite(self):
        if self.hilited == True:
            self.unhilite()
        else:
            self.hilite()

    # The move method undraws the given box, changes its field id (which is used as a reference to
    # draw the box) to the targeted field id (based on where the click was made), redraws the box
    # and then unhilites it
    def move(self, target):
        self.undraw()
        self.fid = target[0]
        self.draw()
        self.unhilite()

    # The getLocation method returns the fields that are taken up by the given box
    def getLocation(self):
        if self.orien == "vertical":
            if self.length == 3:
                return [self.fid, self.fid + 6, self.fid + 12]
            else:
                return [self.fid, self.fid + 6]
        else:
            if self.length == 3:
                return [self.fid, self.fid + 1, self.fid + 2]
            else:
                return [self.fid, self.fid + 1]

    # The getRow method returns the first and last field id's of the row the box is located in
    # (assumes the box is horizontal)
    def getRow(self):
        eleft = self.fid - (self.fid % 6) + 1
        return [eleft, eleft + 5]

    # The getCol method returns the column number the box is located in
    # (assumes the box is vertical)
    def getCol(self):
        colnum = self.fid % 6
        return colnum

    # The flash method uses built in functions from the time module to create the animated flashing
    # effect on the given box
    # The given box is hilited then unhilited with each switch taking 0.5 seconds (so assuming the box is
    # already hilited, it will switch b/w the two states 3 times in 2.5 seconds)
    def flash(self, seconds):
        start = time.time()
        time.clock()
        elapsed = 0
        while elapsed < seconds:
            elapsed = time.time() - start
            self.switchHilite()
            time.sleep(0.5)


# Function that returns a 2-D list of top left and bottom right coordinates for each field
def coords(x, y):
    # Assign initial x,y values to counters
    a, b = x, y
    # Create a variable of type list
    lst = []

    # Go through the left column boxes and get their coordinates
    for i in range(6):
        top_left = (x, b)
        bottom_right = (x + 40, b + 40)
        coord = [top_left, bottom_right]
        lst.append(coord)

        # Get the coordinates of the rest of the row (i.e. 5 more boxes)
        for j in range(5):
            a += 40
            top_left = (a, b)
            bottom_right = (a + 40, b + 40)
            coord = [top_left, bottom_right]
            lst.append(coord)
        a = x
        b += 40

    # Return the 2-D list of both coordinates of each field
    return lst


# Function that takes a field id and returns its corresponding coordinates
def fieldCoords(x, y, fid):
    # Get the list of all the coordinates using the coords function and assign it to a variable
    fields = coords(x, y)
    # Return the element of the corresponding field id
    # (NOTE: Its fid - 1 b/c the element nums go from 0-35 instead of 1-36)
    return fields[fid - 1]


# Function that returns the field the click was made in; returns 0 if the click was outside
def checkClick(x, y, click):
    # Assign the x and y coordinates of the click to variables
    a = click.getX()
    b = click.getY()
    # Create a variable of type int
    field = -1

    # If the x or y coordinates are out of the appropriate range, return 0
    if a < x or b < y or a > x + 240 or b > y + 240:
        field = 0
    else:
        # If the coordinates are in the appropriate range, compare and check with coordinates
        # of each field
        for i in range(1, 37):
            TL_xCoord = fieldCoords(x, y, i)[0][0]
            TL_yCoord = fieldCoords(x, y, i)[0][1]
            BR_xCoord = fieldCoords(x, y, i)[1][0]
            BR_yCoord = fieldCoords(x, y, i)[1][1]

            # If the coordinates are in range of a specific field, assign that field number
            # to the field variable and break out of the loop
            if (a > TL_xCoord and a < BR_xCoord) and (b > TL_yCoord and b < BR_yCoord):
                field = i
                break

    # Return the field number the click was made in (or 0)
    return field


# Function that takes the field id, the color of the box and border, the type of the border
# and either highlights/unhighlights the corresponding field with the corresponding border
# or just colors the box with the corresponding color
def e(x, y, win, fid, color, border, btype, fields):
    # Get the corresponding top left and bottom right coordinates for the given field id
    # and assign them to variables
    TL_xCoord = fieldCoords(x, y, fid)[0][0]
    TL_yCoord = fieldCoords(x, y, fid)[0][1]
    BR_xCoord = fieldCoords(x, y, fid)[1][0]
    BR_yCoord = fieldCoords(x, y, fid)[1][1]

    # If the border type is '', then just create a rectangle in the fid'th field
    # with the color 'color' and set the fields[fid] values to [r]
    # Note: The outline is 'grey' so it looks like the box is "inside" the field
    if btype == '':
        r = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        r.setFill(color)
        r.setOutline("grey")
        r.draw(win)

        fields[fid] = [r]

    # If the border type is '[', then create a rectangle in the fid'th field with
    # the color 'border', create another rectangle inside so the bigger rectangle
    # looks like a '[' border and finally, set the fields[fid] value to [r,s]
    elif btype == '[':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline("grey")
        s.draw(win)

        r = Rectangle(Point(TL_xCoord + 5, TL_yCoord + 5), Point(BR_xCoord - 1, BR_yCoord - 5))
        r.setFill(color)
        r.setOutline(color)
        r.draw(win)

        fields[fid] = [r, s]

    # Also works in the same way, with the border looking like '=' (i.e. border on top and bottom)
    elif btype == '=':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline("grey")
        s.draw(win)

        r = Rectangle(Point(TL_xCoord + 1, TL_yCoord + 5), Point(BR_xCoord - 1, BR_yCoord - 5))
        r.setFill(color)
        r.setOutline(color)
        r.draw(win)

        fields[fid] = [r, s]

    # Works similarly as the '[' case, except this time the border looks like ']'
    elif btype == ']':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline("grey")
        s.draw(win)

        r = Rectangle(Point(TL_xCoord + 1, TL_yCoord + 5), Point(BR_xCoord - 5, BR_yCoord - 5))
        r.setFill(color)
        r.setOutline(color)
        r.draw(win)

        fields[fid] = [r, s]

    # Draws the top vertical border on the box (works similar to the cases above)
    elif btype == 'v[':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline("grey")
        s.draw(win)

        r = Rectangle(Point(TL_xCoord + 5, TL_yCoord + 5), Point(BR_xCoord - 5, BR_yCoord - 1))
        r.setFill(color)
        r.setOutline(color)
        r.draw(win)

        fields[fid] = [r, s]

    # Draws the middle vertical border on the box (works similar to the cases above)
    elif btype == 'v=':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline("grey")
        s.draw(win)

        r = Rectangle(Point(TL_xCoord + 5, TL_yCoord + 1), Point(BR_xCoord - 5, BR_yCoord - 1))
        r.setFill(color)
        r.setOutline(color)
        r.draw(win)

        fields[fid] = [r, s]

    # Draws the bottom vertical border on the box (works similar to the cases above)
    elif btype == 'v]':
        s = Rectangle(Point(TL_xCoord, TL_yCoord), Point(BR_xCoord, BR_yCoord))
        s.setFill(border)
        s.setOutline("grey")
        s.draw(win)

        r = Rectangle(Point(TL_xCoord + 5, TL_yCoord + 1), Point(BR_xCoord - 5, BR_yCoord - 5))
        r.setFill(color)
        r.setOutline(color)
        r.draw(win)

        fields[fid] = [r, s]


# The boxCheck function takes the list of the boxes and the field that was clicked and uses the information
# to hilite/unhilite the appropriate boxes
# Also returns True or False based on whether a box was clicked on (or if the click was made on an empty field)
def boxCheck(fclicked, boxes):
    # bclick represents whether a Block object was clicked or not
    bclick = False

    # A loop goes through all the boxes and checks if the click was made on a box and specifically which one
    for i in range(len(boxes)):
        # b2 represents the difference b/w the field id's of the first and second block of the box
        # (so for a box of length 2, this would be the last block)
        if boxes[i].orien == "vertical":
            b2 = 6
        else:
            b2 = 1

        # If any part of the box is clicked, hilite the entire thing and unhilite the previously hilited (if any)
        # box using the boxUnhilite function
        if fclicked == boxes[i].getLocation()[0] or fclicked == boxes[i].getLocation()[0] + b2 or fclicked == \
                boxes[i].getLocation()[-1]:
            boxes[i].switchHilite()
            boxUnhilite(i, boxes)
            bclick = True
            break
    return bclick


# The boxUnhilite function takes the list of boxes and a boxnum; it unhilites everything that is currently hilited
# except for the boxnum box (this allows for only one thing to be hilited at a time)
def boxUnhilite(boxnum, boxes):
    for i in range(len(boxes)):
        if i != boxnum and boxes[i].hilited == True: boxes[i].unhilite()


# The moveBox function moves the hilitedBox based on where the click was made and what the length/orientation
# of the box is
# It uses the move method from the Block class
def moveBox(fclicked, boxes, hilitedBox):
    if hilitedBox.orien == "vertical" and fclicked > hilitedBox.fid:
        if hilitedBox.length == 3:
            hilitedBox.move([fclicked - 12, fclicked - 6, fclicked])
        else:
            hilitedBox.move([fclicked - 6, fclicked])
    elif hilitedBox.orien == "vertical" and fclicked < hilitedBox.fid:
        if hilitedBox.length == 3:
            hilitedBox.move([fclicked, fclicked + 6, fclicked + 12])
        else:
            hilitedBox.move([fclicked, fclicked + 6])
    elif hilitedBox.orien == "horizontal" and fclicked > hilitedBox.fid:
        if hilitedBox.length == 3:
            hilitedBox.move([fclicked - 2, fclicked - 1, fclicked])
        else:
            hilitedBox.move([fclicked - 1, fclicked])
    elif hilitedBox.orien == "horizontal" and fclicked < hilitedBox.fid:
        if hilitedBox.length == 3:
            hilitedBox.move([fclicked, fclicked + 1, fclicked + 2])
        else:
            hilitedBox.move([fclicked, fclicked + 1])


# The checkOverlap function returns True if any invalid move is detected and False otherwise
def checkOverlap(fclicked, boxes, hilitedBox, click, x, y):
    ans = False

    # All the currently occupied fields are put into a list (excluding the the fields occupied by the
    # hilited box b/c that box is the one being moved)
    occupied = []
    for i in range(len(boxes)):
        if boxes[i] != hilitedBox: occupied.append(boxes[i].getLocation())

    # The fields covered by the hilitedBox are compared to the boxes around it to see whether the move being
    # made is legal (gotten using the getLocation method from the Block class)
    loc = hilitedBox.getLocation()
    for j in range(len(occupied)):
        for k in range(len(occupied[j])):
            # For horizontally oriented boxes...
            if hilitedBox.orien == "horizontal":
                # If the click is made in a different row, don't move
                if fclicked < hilitedBox.getRow()[0] or fclicked > hilitedBox.getRow()[1]:
                    ans = True
                    break
                # If there is an occupied field immediately to the right, don't move right
                elif loc[-1] + 1 == occupied[j][k] and loc[-1] % 6 != 0 and fclicked > loc[-1]:
                    ans = True
                    break
                # If there is an occupied field immediately to the left, don't move left
                elif loc[0] - 1 == occupied[j][k] and (loc[0] + 5) % 6 != 0 and fclicked < loc[0]:
                    ans = True
                    break
                # If there is an occupied field a block left of the field clicked, don't move right
                elif fclicked > loc[-1] and fclicked - 1 == occupied[j][k]:
                    ans = True
                    break
                # If there is an occupied field a block right of the field clicked, don't move left
                elif fclicked < loc[0] and fclicked + 1 == occupied[j][k]:
                    ans = True
                    break
                # For length 2 boxes, if there is an occupied field 2 blocks right of the field clicked, don't move left
                elif hilitedBox.length == 2 and fclicked < loc[0] and fclicked + 2 == occupied[j][k]:
                    ans = True
                    break
                # For length 2 boxes, if there is an occupied field 2 blocks left of the field clicked, don't move right
                elif hilitedBox.length == 2 and fclicked > loc[-1] and fclicked - 2 == occupied[j][k]:
                    ans = True
                    break
            else:  # For vertically oriented boxes...
                # If the click is made in a different column, don't move
                if fclicked % 6 != hilitedBox.getCol():
                    ans = True
                    break
                # If there is an occupied field immediately below, don't move down
                elif loc[-1] + 6 == occupied[j][k] and fclicked > loc[-1]:
                    ans = True
                    break
                # If there is an occupied field immediately above, don't move up
                elif loc[0] - 6 == occupied[j][k] and fclicked < loc[0]:
                    ans = True
                    break
                # If there is an occupied field a block above the field clicked, don't move down
                elif fclicked > loc[-1] and fclicked - 6 == occupied[j][k]:
                    ans = True
                    break
                # If there is an occupied field a block below the field clicked, don't move up
                elif fclicked < loc[0] and fclicked + 6 == occupied[j][k]:
                    ans = True
                    break
                # For length 2 boxes, if there is an occupied field 2 blocks below the field clicked, don't move up
                elif hilitedBox.length == 2 and fclicked < loc[0] and fclicked + 12 == occupied[j][k]:
                    ans = True
                    break
                # For length 2 boxes, if there is an occupied field 2 blocks above the field clicked, don't move down
                elif hilitedBox.length == 2 and fclicked > loc[-1] and fclicked - 12 == occupied[j][k]:
                    ans = True
                    break

    # If the click is made outside the grid, don't move the box
    if click.getX() < x or click.getY() < y or click.getX() > x + 240 or click.getY() > y + 240: ans = True

    # If any of the rules are violated, unhilite the box
    if ans == True: hilitedBox.unhilite()
    return ans


def main():
    # Set the x,y reference points
    x, y = 20, 20
    # Enter dimensions and title for the graphic window and assign it to a variable
    win = GraphWin("Unblock me", 280, 280)

    # Create a list of 36 empty lists using createFields function
    fields = grid.createFields(37)
    # Create the outer grey border using the outline function by passing the x,y reference points
    # and the graphic window
    grid.outline(x, y, win)
    # Create the grey gridlines using the gridlines function by passing the x,y reference points
    # and the graphic window
    grid.gridlines(x, y, win)

    # Create a small box in the top left corner (which will act as a close button)
    cbox = Rectangle(Point(1, 1), Point(x - 8, y - 8))
    cbox.draw(win)

    # Create a letter 'X' and place it inside the cbox to make it look more like a close button
    cross = Text(Point(6, 6), "X")
    cross.setSize(5)
    cross.draw(win)

    # Create a list which will store all the Block objects
    boxes = []

    # Create all the vertical boxes and append them into the list
    boxes.append(Block(x, y, win, 6, 3, "vertical", "brown", fields))
    boxes.append(Block(x, y, win, 9, 3, "vertical", "brown", fields))
    boxes.append(Block(x, y, win, 19, 2, "vertical", "brown", fields))
    boxes.append(Block(x, y, win, 29, 2, "vertical", "brown", fields))

    # Create all the horizontal boxes and append them into the list
    boxes.append(Block(x, y, win, 1, 3, "horizontal", "brown", fields))
    boxes.append(Block(x, y, win, 13, 2, "horizontal", "red", fields))
    boxes.append(Block(x, y, win, 23, 2, "horizontal", "brown", fields))
    boxes.append(Block(x, y, win, 31, 3, "horizontal", "brown", fields))

    # Go through all the Blocks in the boxes list and draw them all
    for b in range(len(boxes)):
        boxes[b].draw()

    # Initiate a while loop which only exits if the close button is clicked or the game is won
    while True:
        # If the game is won (i.e. red box covers fields 17 and 18), then that (red) block flashes 3 times
        # (using the flash method of the class Block) and the loop exits
        if boxes[5].fid == 17:
            boxes[5].flash(2.5)
            break

        # Store the coordinates of the click inside a variable
        click = win.getMouse()
        # Use the click to check which field the click was made in (using the checkClick function)
        fclicked = checkClick(x, y, click)

        # If the close button is clicked, then the loop exits
        if click.getX() < x - 8 and click.getY() < y - 8: break

        # boxCheck returns False if a click is made on an empty field
        if boxCheck(fclicked, boxes) == False:
            # Go through all the boxes until the hilited one is found
            for i in range(len(boxes)):
                # Check to see whether the move is valid using the checkOverlap function and move the block
                # using the moveBox function if it is, don't do anything otherwise
                if boxes[i].hilited == True and checkOverlap(fclicked, boxes, boxes[i], click, x, y) == False:
                    moveBox(fclicked, boxes, boxes[i])

    # Close the window (only happens when the loop exits)
    win.close()


main()
