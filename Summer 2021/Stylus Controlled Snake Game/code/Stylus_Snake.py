#importing requiered libraries
import cv2 as cv
import numpy as np
import pygame
import random

from pygame.display import set_caption


cap = cv.VideoCapture(0 + cv.CAP_DSHOW) #capturing video (+ cv.CAP_DSHOW is only used if using only 0 doesn't work)
kernel = np.ones((3, 3), np.uint8)      #this is the kernel for passing while "closing" and dilation
ncx = ncy=  2300000                     #assigning these value so that there is no condition check everytime for 1st and2nd iteration
key = 0                                 #condition for entering into the loop
font = cv.FONT_HERSHEY_SIMPLEX

# HSV backprojection
enter_key = False
while key != 27:
    _,fram = cap.read()
    frame = cv.flip(fram,1)
    x = np.copy(frame)
    roi = frame[226:255,306:335]
    cv.imshow("ROI",roi)
    cv.rectangle(frame,(302,222),(338,258),(0,255,0),3)
    cv.putText(frame,'Let the rectangle be inside the object, then press SpaceBar',(50,450), font, 0.5,(255,255,255),2,cv.LINE_AA)
    cv.imshow("frame",frame)
    key = cv.waitKey(1)
    if key == 32:
        enter_key = True
    if enter_key == True:
        hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)
        hsvt = cv.cvtColor(x,cv.COLOR_BGR2HSV)
        M = cv.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )
        I = cv.calcHist([hsvt],[0, 1], None, [180, 256], [0, 180, 0, 256] )
        R = M / I
        key = 27
        
# Code for Snake
cap.release()
cv.destroyAllWindows()

cap = cv.VideoCapture(0 + cv.CAP_DSHOW) #capturing video (+ cv.CAP_DSHOW is only used if using only 0 doesn't work)

# Code for Snake

# Screen Width and screen_height
screen_width = 600
screen_height = 680

# initializing pygame
pygame.init()
set_caption("Stylus Snake")
clock = pygame.time.Clock()
# Starting position of snake
start_pos_x = 300
start_pos_y = 390
# getting screen loading images and getting rect
screen = pygame.display.set_mode((screen_width,screen_height))
head = pygame.image.load('images/head.jpg').convert_alpha()
head_rect = head.get_rect(center = (start_pos_x,start_pos_y))
body = pygame.image.load('images/body.jpg').convert_alpha()
body_rect = body.get_rect(center = (335,240))
food = pygame.image.load('images/food.jpg').convert_alpha()
food_rect = food.get_rect(center = (300,300))

position = [(start_pos_x,start_pos_y)]
# rect's for snake body
snake_rectangles = [head_rect]
# giving arbitrary values for movements, doesn't move if input isn't given
movement = previous_movement = 33
# This is used to generate food after some number of loops
counter = 0
# condition for food to generate
condition = random.randint(50,80)
# Food display condition set to false
display_condition = False
# Condition to run this loop
run_condition = True
# time for snake to chase the food
grab_time = random.randint(150, 400)
# these are initiated to display information
rect_screen = pygame.Rect(0, 0, 600, 80)
text_font = pygame.font.Font('font/comic.ttf',50)
text_rect = text_font.render('Snake Game',True,'Green')
text_font = pygame.font.Font('font/comic.ttf',25)
after_text = pygame.font.Font('font/comic.ttf',25)
# Score set to Zero
score = 0
score_rect = text_font.render(f'Score = {score}',True,'Green')
after_text_rect = after_text.render('Press SpaceBar to start or ESC to exit',True,'Blue')
# Game status set to False turn True when spacebar is pressed
game_status = False
# Creating walls
blocks = pygame.image.load('images/wall.jpg').convert_alpha()
def create_blocks(count,intial_x,intial_y,x_in,y_in):
    tempblock_rect = blocks.get_rect(center = (intial_x,intial_y))
    tempblock_rectangles = [tempblock_rect]
    for i in range(count):
        tempblock_rectangles.append(blocks.get_rect(center = (tempblock_rect.x + 7 + (x_in * (i + 1)),tempblock_rect.y + 7 + (y_in * (i + 1)))))
    return tempblock_rectangles

block_rectangles1 = [create_blocks(29,107,87,14,0)] # Create first block set
block_rectangles1.append(create_blocks(29,107,673,14,0)) # append to the block set
block_rectangles1.append(create_blocks(29,593,187,0,14))
block_rectangles1.append(create_blocks(29,7,187,0,14))
block_rectangles1.append(create_blocks(7,402,207,14,0))
block_rectangles1.append(create_blocks(7,100,573,14,0))
block_rectangles1.append(create_blocks(6,500,221,0,14))
block_rectangles1.append(create_blocks(6,100,559,0,-14))

block_rectangles2 = [create_blocks(20,127,217,0,14)]
block_rectangles2.append(create_blocks(20,500,217,0,14))
block_rectangles2.append(create_blocks(20,170,137,14,0))
block_rectangles2.append(create_blocks(20,170,577,14,0))


block_rectangles3 = [create_blocks(42,7,220,14,0)]
block_rectangles3.append(create_blocks(42,150,87,0,14))

block_rectangles4 = [create_blocks(42,7,520,14,0)]
block_rectangles4.append(create_blocks(42,450,87,0,14))

maze_list = [block_rectangles1,block_rectangles2,block_rectangles3,block_rectangles4]
maze = maze_list[random.randint(0,3)]
# Screen Colors
screen_color = (255,255,255)
Blue = (0,0,255)

while run_condition:                        #comes out of the program when escape is pressed
    
    if game_status == True:

        _, fram = cap.read()                #reading the camera
        frame = cv.flip(fram, 1)            #flipping the camera along the vertical axis
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  #converting frame from bgr to hsv
        h,s,v = cv.split(hsv)
        B = R[h.ravel(),s.ravel()]
        B = np.minimum(B,1)
        B = B.reshape(hsvt.shape[:2])
        disc = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
        cv.filter2D(B,-1,disc,B)
        B = np.uint8(B)
        cv.normalize(B,B,0,255,cv.NORM_MINMAX)
        _,mask = cv.threshold(B,50,255,0) 
        #applying closing operation on mask to remove noise from the image
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel) 
        #dilation is done to remove some of the dark spot inside the mask
        dilation_after_closing = cv.dilate(closing,kernel,iterations = 3)
        if (dilation_after_closing[:] == 255).any():                  #if there is object in the mask at least 1 white spot will be there only then proceed to find contours
            contours, _ = cv.findContours(dilation_after_closing, 1, 2) #detecting contours
            areas = [cv.contourArea(c) for c in contours]   #finding areas of all the contourand putting them in a list
            #finding the index of the largest contour in the above list
            cnt=contours[np.argmax(areas)]
            cv.drawContours(dilation_after_closing, [cnt] , 0, (0,255,0), 3)
            #using the contour with larget area to draw it on the original frame
            M = cv.moments(cnt)                             #finding moments and centroid of the largest contour
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            #copying the values of the old coordinated for the end points of next line
            diffx = cx - 320
            diffy = cy - 240
            absx = abs(diffx)
            absy = abs(diffy)
            if(absx > 30 or absy > 30):
                previous_movement = movement
                if absx > absy:
                    if diffx > 0:
                        movement = 0 # Right
                    else:
                        movement = 2 # Left
                else:
                    if diffy < 0:
                        movement = 3 # Up
                    else:
                        movement = 1 # Down
                # Condition checks if the 
                if(abs(previous_movement - movement) == 2):
                    movement = previous_movement
        key = cv.waitKey(1)             #waiting for one millisecond for some input from the user
        
        # Drawing reference messages and boundaries
        cv.line(frame,(80,0),(560,480),(0,0,0),5)
        cv.line(frame,(80,480),(560,0),(0,0,0),5)
        cv.putText(frame,'UP',(280,50), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'DOWN',(280,400), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'RIGHT',(420,240), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'LEFT',(100,240), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.imshow("Wireless Joystick!",frame)

        # screen
        screen.fill(screen_color)
        pygame.draw.rect(screen, Blue, rect_screen)
        screen.blit(text_rect,(30,0))
        screen.blit(score_rect,(400,45))
        
        # Updating the postion array of the body
        length = len(position)
        limit = length - 1
        if(limit > 0):
            for i in range(limit):
                position[limit - i] = position[limit - i - 1]
        
        # Updating the postion of the head
        if movement == 0:
            position[0] = (position[0][0] + 14 , position[0][1])
            if( position[0][0] > screen_width):
                position[0] = (14 , position[0][1])
        elif movement == 1:
            position[0] = (position[0][0], position[0][1] + 14)
            if position[0][1] > screen_height:
                position[0] = (position[0][0] , 94)
        elif movement == 2:
            position[0] = (position[0][0] - 14 , position[0][1])
            if position[0][0] < 0:
                position[0] = (screen_width - 14 , position[0][1])
        elif movement == 3:
            position[0] = (position[0][0], position[0][1] - 14)
            if position[0][1] < 80:
                position[0] = (position[0][0] , screen_height-14)
        
        # setting the position to the rectangles
        for i in range(length):
            snake_rectangles[i].center = (position[i][0],position[i][1])
        
        # Displaying snake
        for rect in snake_rectangles:
            if(rect == head_rect):
                screen.blit(head,rect)
            else:
                screen.blit(body,rect)
                if display_condition and food_rect.colliderect(rect):
                    display_condition = False
                    condition = counter # new food will be generated now

        # displaying Wallls and checking if the snake head collided with walls or if the generated food is on the walls
        for B in maze:
            for x in B:
                screen.blit(blocks,x)
                if head_rect.colliderect(x):
                    game_status = False
                    display_condition = False
                    condition = random.randint(50,80)
                elif food_rect.colliderect(x):
                    display_condition = False
                    condition = counter # new food will be generated now
        
        # displaying food until its either eaten or the allowed time is finished
        if display_condition and counter < grab_time:
            screen.blit(food, food_rect)
        
        # If snake head collides with the food
        # Display condition is a condition here because if not set sometimes two collisions happen
        if display_condition and counter < grab_time and head_rect.colliderect(food_rect):
            position.append(position[length-1])
            snake_rectangles.append(body.get_rect(center = position[length - 1]))
            display_condition = False
            condition = condition + random.randint(10,25)
            score = score + 1
            score_rect = text_font.render(f'Score = {score}',True,'Green')
            pygame.draw.rect(screen, Blue, rect_screen)
            screen.blit(text_rect,(30,0))
            screen.blit(score_rect,(400,45))
            
        # Food Generation
        if counter == condition:
            food_rect.center = (random.randint(15,screen_width),random.randint(115, screen_height))
            condition = random.randint(50,80)
            counter = 0
            grab_time = random.randint(150, 185)
            display_condition = True
        
        # Checing if the snake collides with its body
        for i in range (3,length):
            if head_rect.colliderect(snake_rectangles[i]):
                game_status = False
        # Updating all drawing
        pygame.display.flip()
        pygame.display.update()
        counter = counter + 1
        
        # if game status = False then setting position to start emptying the body part from rectangles
        if game_status == False:
            position = [(start_pos_x,start_pos_y)]
            snake_rectangles = [head_rect]
        for events in pygame.event.get():
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    key = 27
        
        # If Esc is pressed then run condition turns to False
        if(key == 27):
            run_condition = False
        clock.tick(30)
    else:
        _, fram = cap.read()                #reading the camera
        frame = cv.flip(fram, 1) 
        cv.imshow("Wireless Joystick!",frame)
        screen.fill(screen_color)
        pygame.draw.rect(screen, Blue, rect_screen)
        score_rect = text_font.render(f'Score = {score}',True,'Green') 
        screen.blit(text_rect,(30,0))
        screen.blit(score_rect,(400,45))
        screen.blit(after_text_rect,(50,300))
        pygame.display.flip()
        pygame.display.update()
        key = cv.waitKey(1)
        for events in pygame.event.get():
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    key = 27
                elif(events.key == pygame.K_SPACE):
                    game_status = True
                    score = 0
                    score_rect = text_font.render(f'Score = {score}',True,'Green')
                    after_text_rect = after_text.render('Press SpaceBar to Restart or ESC to exit',True,'Blue')

        if(key == 27):
            run_condition = False
        elif key == 32:
            game_status = True
            score = 0
            score_rect = text_font.render(f'Score = {score}',True,'Green')
            after_text_rect = after_text.render('Press SpaceBar to Restart or ESC to exit',True,'Blue')

#releasing the capture and destroying all the windows
cap.release()
cv.destroyAllWindows()
