import random
import pygame
import cv2 as cv
import numpy as np
from pygame.display import set_caption

# Initial opencv declarations

cap = cv.VideoCapture(0 + cv.CAP_DSHOW) #capturing video (+ cv.CAP_DSHOW is only used if using only 0 doesn't work)
kernel = np.ones((3, 3), np.uint8)      #this is the kernel for passing while "closing" and dilation
ncx = ncy=  2300000                     #assigning these value so that there is no condition check everytime for 1st and2nd iteration
key = 0                                 #condition for entering into the loop
font = cv.FONT_HERSHEY_SIMPLEX
movement = 10

# HSV backprojection
enter_key = False
show_key = False
while key != 27:
    _,fram = cap.read()
    frame = cv.flip(fram,1)
    x = np.copy(frame)
    roi = frame[226:255,306:335]
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

# Snake Initial Declarations
pygame.init()
set_caption("Stylus Snake")
score = 0
start_pos = (300,300)
screen_width = 600
screen_height = 680
screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()

# Sprite Classes

class Snake(pygame.sprite.Sprite):
    movement = 10
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load('images/head.jpg').convert()
        self.rect = self.image.get_rect()
        self.position = start_pos
        self.rect.center = self.position
        self.direction = 10
        self.array = [self.zero,self.one,self.two,self.three]

    # This methods get the direction then changes position of rectangle
    # Also checks if the snake is outside the screen if yes then brings it back through the opposite side
    def get_direction(self):
        if self.movement != 10:
            if abs(self.direction - self.movement) != 2:
                self.direction = self.movement
            if self.direction < 4:
                self.array[self.direction]()
            self.rect.center = self.position

    # These methods are called depending on the input from the Stylus
    def zero(self):
        self.position = (self.position[0] + 14 , self.position[1])
        if( self.position[0] > screen_width):
            self.position = (14 , self.position[1])

    def one(self):
        self.position = (self.position[0] , self.position[1] + 14)
        if self.position[1] > screen_height:
            self.position = (self.position[0] , 94)

    def two(self):
        self.position = (self.position[0] - 14 , self.position[1])
        if self.position[0] < 0:
            self.position = (screen_width - 14 , self.position[1])

    def three(self):
        self.position = (self.position[0], self.position[1] - 14)
        if self.position[1] < 80:
                self.position = (self.position[0] , screen_height-14)

class Body(pygame.sprite.Sprite):
    # Keeps the record of the length of the body of Snake
    length = 0
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("images/body.jpg").convert()
        self.rect = self.image.get_rect()
        self.position = (13,13)

class Food(pygame.sprite.Sprite):
    variable = 7
    display_condition = False
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load('images/food.jpg').convert()
        self.rect = self.image.get_rect()
        self.display_condition = False
    
    def generate(self):
        self.rect.center = (random.randint(1,600),random.randint(80,600))
        self.display_condition = True
        if pygame.sprite.spritecollide(food,walls_group,False) or pygame.sprite.spritecollide(food,body_group,False):
            food.generate()
        if pygame.sprite.spritecollide(food,body_group,False) or pygame.sprite.spritecollide(food,body_group,False):
            food.generate()

class Walls(pygame.sprite.Sprite):
    def __init__(self,position_x,position_y) -> None:
        super().__init__()
        self.image = pygame.image.load("images/wall.jpg").convert()
        self.rect = self.image.get_rect()
        self.position = (position_x,position_y)
        self.rect.center = self.position

# Updating snake body
def update_body():
    # Helps store the value of the first body part 
    # Then all the remaining body part change position
    first_term = True
    for x in body_group:
        if first_term == True:
            variable = x.position
            first_term = False
        else:
            temp = x.position
            x.position = variable
            variable = temp
            x.rect.center = x.position 
    # Changing the position of first Body part
    first_body.position = snake.position
    first_body.rect.center = first_body.position

# Collision with food
def collision_food():
    # increases Body length by 1 and adds a body part to the snake
    if Body.length == 0:
        body_group.add(first_body)
        Body.length += 1
    else:
        body_group.add(Body())
        Body.length += 1
    # Once food is eaten Food should disappear
    food.display_condition = False        

# Creating Walls
def create_Walls(position,count,initial_x,initial_y,x_increament,y_increament):
    for i in range(count):
        x = initial_x + (x_increament * i)
        y = initial_y + (y_increament * i)
        walls_group_list[position].add(Walls(x,y))

# Creating group for body parts
first_body = Body()
body_group = pygame.sprite.Group()

# Creating group for Walls
walls_group_list = [pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group(),pygame.sprite.Group()]
walls_group = walls_group_list[random.randint(0,3)]
# Creating group for Food
food = Food()
food_group = pygame.sprite.GroupSingle()
food_group.add(food)

# Creating group for Snake
snake = Snake()
snake_group = pygame.sprite.GroupSingle()
snake_group.add(snake)

# Initializing all the writen text
text_font = pygame.font.Font('font/comic.ttf',50)
display_screen = pygame.Rect(0, 0, 600, 80)
text_font_50 = pygame.font.Font('font/comic.ttf',50)
title = text_font_50.render('Snake Game',True,'Green')
text_font_25 = pygame.font.Font('font/comic.ttf',25)
score_display = text_font_25.render(f'Score = {score}',True,'Green')
restart_text = text_font_25.render('Press SpaceBar to start or ESC to exit',True,'Blue')

# Creating Walls
create_Walls(0,29,107,87,14,0)
create_Walls(0,29,107,673,14,0)
create_Walls(0,29,593,187,0,14)
create_Walls(0,29,7,187,0,14)
create_Walls(0,8,402,207,14,0)
create_Walls(0,8,100,573,14,0)
create_Walls(0,7,500,221,0,14)
create_Walls(0,7,100,559,0,-14)

create_Walls(1,20,127,217,0,14)
create_Walls(1,20,500,217,0,14)
create_Walls(1,20,170,137,14,0)
create_Walls(1,20,170,577,14,0)

create_Walls(2,43,7,220,14,0)
create_Walls(2,43,150,87,0,14)

create_Walls(3,43,7,520,14,0)
create_Walls(3,43,450,87,0,14)

# Setting game_status to False so that introductory window opens
game_status = False

# Colors
Blue = (0,0, 255)
white = (255,255,255)

# times to manage the food generation
start_time = 0
time_to_chase = random.randint(15,20)

# Condition for the loop to run
run_condition = True

while run_condition:
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
                if absx > absy:
                    if diffx > 0:
                        snake.movement = 0 # Right
                    else:
                        snake.movement = 2 # Left
                else:
                    if diffy < 0:
                        snake.movement = 3 # Up
                    else:
                        snake.movement = 1 # Down
        # Some reference on the video
        cv.line(frame,(80,0),(560,480),(0,0,0),5)
        cv.line(frame,(80,480),(560,0),(0,0,0),5)
        cv.putText(frame,'UP',(280,50), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'DOWN',(280,400), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'RIGHT',(420,240), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.putText(frame,'LEFT',(100,240), font, 1,(255,255,255),2,cv.LINE_AA)
        cv.imshow("Wireless Joystick",frame)
        
        # Filling screen with white color drawing walls and pasting information
        screen.fill(white)
        walls_group.draw(screen)
        pygame.draw.rect(screen,Blue,display_screen)
        screen.blit(title,(30,0))
        screen.blit(score_display,(400,45))

        #food_group.update()
        curr_time = int(pygame.time.get_ticks() / 1000)

        # If food is present the check for collision and set time to generate new food
        # If there is no food generate after Food.variable seconds later
        if food.display_condition == True:
            if snake.rect.colliderect(food.rect):
                start_time = curr_time
                score += 1
                score_display = text_font_25.render(f'Score = {score}',True,'Green')
                Food.variable = random.randint(5,10)
                collision_food()
            elif curr_time - start_time > time_to_chase:
                food.display_condition = False
                Food.variable = random.randint(5,10)
                time_to_chase = random.randint(17,25)
                start_time  = curr_time
        else:
            if curr_time - start_time > Food.variable:
                start_time = curr_time
                food.generate()

        # Drawing body if length is greater than 1
        if Body.length > 0:
            update_body()
            body_group.draw(screen)
        if food.display_condition == True:
            food_group.draw(screen)
        
        # After the body is updated Snake position can be changed
        snake.get_direction()
        
        # Drawing Snake and updating screen
        snake_group.draw(screen)
        pygame.display.flip()
        pygame.display.update()

        # Opencv code for getting movement

        
        
        key = cv.waitKey(1)

        # If snake collides with its body
        if pygame.sprite.spritecollide(snake, body_group, False):
            game_status = False
            food.display_condition = False
        
        # If snake collided with the walls
        if pygame.sprite.spritecollide(snake,walls_group,False):
            game_status = False
            food.display_condition = False

        # If ESC is pressed exit from the game
        if key == 27:
            pygame.quit()
            run_condition = False

        # Frame rate
        clock.tick(30)

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                run_condition = False
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    run_condition = False
            
    else:
        _, fram = cap.read()                #reading the camera
        frame = cv.flip(fram, 1) 

        cv.imshow("Wireless Joystick",frame)
        screen.fill(white)
        pygame.draw.rect(screen,Blue,display_screen)
        screen.blit(title,(30,0))
        screen.blit(score_display,(400,45))
        screen.blit(restart_text,(50,300))
        

        key = cv.waitKey(1)
        if key == 27:
            pygame.quit()
            run_condition = False
        

        # If the Space Bar is pressed then Game restarts with all values set to initial values
        elif key == 32:
            snake.movement = 10
            snake.direction = 10
            snake.position = start_pos
            snake.rect.center = snake.position
            pygame.sprite.Group.empty(body_group)
            game_status = True
            score = 0
            Body.length = 0
            score_display = text_font_25.render(f'Score = {score}',True,'Green')
            restart_text = text_font_25.render('Press SpaceBar to start or ESC to exit',True,'Blue')
            screen.fill(white)
            pygame.draw.rect(screen,Blue,display_screen)
            screen.blit(title,(30,0))
            screen.blit(score_display,(400,45))
            screen.blit(restart_text,(50,300))
            
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                    pygame.quit()
                    run_condition = False
            if(events.type == pygame.KEYDOWN):
                if(events.key == pygame.K_ESCAPE):
                    pygame.quit()
                    run_condition = False
                elif(events.key == pygame.K_SPACE):
                    snake.movement = 10
                    snake.direction = 10
                    snake.position = start_pos
                    snake.rect.center = snake.position
                    pygame.sprite.Group.empty(body_group)
                    Body.length = 0
                    game_status = True
                    score = 0
                    Food.variable = random.randint(7,12)
                    score_display = text_font_25.render(f'Score = {score}',True,'Green')
                    restart_text = text_font_25.render('Press SpaceBar to start or ESC to exit',True,'Blue')
                    screen.fill(white)
                    pygame.draw.rect(screen,Blue,display_screen)
                    screen.blit(title,(30,0))
                    screen.blit(score_display,(400,45))
                    screen.blit(restart_text,(50,300))
        pygame.display.flip()
        pygame.display.update()
                    

# Releasing the camera
cap.release()
cv.destroyAllWindows()
