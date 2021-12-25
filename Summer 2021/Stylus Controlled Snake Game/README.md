# Stylus_Snake

Play the traditional Stylus Snake game with the help of any object as the stylus

## Libraries used
* opencv
* numpy
* pygame
* random

# Resources
* [opencv tutorials](https://docs.opencv.org/4.5.2/d6/d00/tutorial_py_root.html)
* [pygame documentation](https://www.pygame.org/docs/)

## Methods

* Using sprite class and hsv backprojection with opencv
* Without using sprite class and hsv backprojection with opencv

### Basic to Both the methods

* Use hsv backprojection to detect the object using numpy method
![gif2](https://user-images.githubusercontent.com/89838921/137094327-6bbdd862-ea0b-4c6c-aba7-7696680ef855.gif)
* Finding contour from the obtained mask
* Get the centoid value
* the camera is divided into four triangles
* If the triangle is in upper, lower, right, left triangle then snake moves upwards, downwards, rightwards, leftwards respectively


### Without using sprite class

* Initalize and load requiered for the game to run
* Creating walls
* Reading the centroid
* Filling the screen with white color
* Adding title and score-board
* Position is an array that stores positions of every part of the snake. If the snake has a body then it every part gets the position of its leading the element
* Depending in the direction the snake goes the program checks if it crosses the maze boundaries and brings it back to the start point of the other side
* Display the snake and check if the food generate collides with the snake body
* Displaying the walls, also checking if food isn't on the walls
* Displaying food until either snake eats or the chasing time is over
* Cheking if the snake eat the food 
    * Increasing the body length by 1
    * Setting the display condition for food as False
    * Increasing the time it will spawn the next food
    * Increasing the score
    * Updating the score
* Generate food it counter = condition for generation
* Checking if the head collided with any body part after the third part
* If the game_status turns False due to:
    * The collision of snake's head with the walls
    * The collision of snake's head with the body
This resets all the values to initial values
* If the game_status is False
    * The score gained is displayed with instruction
        * If the user pressed Esc the program exits
        * If the user pressed spacebar then the game restarts

### Using sprite class

* Creating Classes
    * Snake head
        * Includes the image rectangle
        * Position
        * Direction in which the snake moves. Initially set to 10 so that no movement takes place until stylus is detected
        * Array with functions needed to change position and check if it the head crosses the boundaries
        * Get_direction : a method to get the direction and change the position of the snake
        * Zero, one, two, three are methods that change move the snake to new position
    * Body
        * Includes the image rectangle
        * Position of individual part initially set to 13, 13(just randomly)
    * Food
        * Image rectangle
        * Display condition
        * Method generate: generates random position, sets display_condition to True
        * The generate function is called again if food lands on walls or body of the snake
    * walls
        * Includes the image rectangle
        * Position for individual walls

* Function update_body : used to update position of every part to its leading part and first body part to the snakes position
* Function collision food: used to increase length of body after it eats the food
* Function create_walls create a line of walls given input as the number of walls in row, first block position (initial_x,initial_y) and the increament to this position for next block

* Initialising all the varialbles requiered
* Creating walls
* Initializing time
* While game_stauts is true
    * Fill screen, diplay game name, score and the walls 
    * Finding the collision between the snake head and food
    * Updating the body
    * Getting snake direction and new position
    * Showing snake body and head
    * Finding collision between the snake and walls and snake and its body
    * Using hsv backprojection to find the centroid of the stylus
    * Drawing reference on the live video
    * Game_status turns False when snake head collides with the body or when it collides with the wall
    * When pressed Esc the game is exited
* While game_status is False
    * Frame window shows the live video
    * Score gained is displayed
    * Instrustion to restart the game or to exit is shown
    * Press spacebar to restart and Esc to exit
    * All the values are reset when spacebar is pressed
    * It works for both when the current working window is the live feed or the game
![gif1](https://user-images.githubusercontent.com/89838921/137094392-741e3c47-21d8-4ee9-aee4-a4afba16c8d5.gif)


## Notes

* First method does not have as many function as the second which makes the first code run faster.
* First method uses less lines of code.
* Second method is structured and any changes can be made in the classes whereas the first method changes have to made in several places.
* The hsv projection doesn't give great results as compared to alloting proper hsv values with hsv calculator and using hsv thresholding.
* For using a manual hsv calculator click [here](https://github.com/adityajivoji/manual_hsv_calc.git)
* The program uses opencv library for the input part. the capturing of the input takes a lot of time that is why the code may not work faster even if the f.p.s. is increased.
* The current f.p.s. is 8.3 when game_status is False and about the same when game_status is OFF this implies that the fps is dominated by the presence of code derived from opencv
* To see the demonstration video click [here](https://drive.google.com/file/d/1nCrvaIU630CwWT4bjs9g17-60CQr-s-b/view?usp=sharing)
