import pygame
import random
import time
import math
from tqdm import tqdm
import numpy as np

class Snake():
    def __init__(self, display, clock):
        self.display = display 
        self.clock = clock 

    def display_snake(self, snake_position, display):
        """Draw snake body"""
        for position in snake_position:
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(position[0], position[1], 10, 10))

    def display_food(self, food_position, display):
        """Draw food position"""
        pygame.draw.rect(display, (10, 10, 120), pygame.Rect(food_position[0], food_position[1], 10, 10))

    def starting_positions(self):
        """Generate starting positions of snake and food"""
        #snake starts with three parts!
        snake_start = [100, 100]                                                        #head position
        snake_position = [[100, 100], [90, 100], [80, 100]]                             #all of positions of the bodies
        food_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]    #position of current food 
        score = 0                                                                       #score

        return snake_start, snake_position, food_position, score

    def food_from_snake(self, food_position, snake_position):
        #calculate distance from food to snake
        return np.linalg.norm(np.array(food_position) - np.array(snake_position[0]))

    def move_snake(self, snake_start, snake_position, food_position, button_direction, score):
        """A Method for updating position of snake and checking collision with food"""
        if button_direction == 1:
            snake_start[0] += 10
        elif button_direction == 0:
            snake_start[0] -= 10
        elif button_direction == 2:
            snake_start[1] += 10
        else:
            snake_start[1] -= 10

        if snake_start == food_position:     #when head touches food
            food_position, score = self.collision_with_food(food_position, score)      #generate new food and add score
            snake_position.insert(0, list(snake_start))                           #add body      

        else:                                #no collision 
            snake_position.insert(0, list(snake_start))
            snake_position.pop()

        return snake_position, food_position, score


    def collision_with_food(self, food_position, score):
        #update score and generate new position for food
        food_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
        score += 1
        return food_position, score


    def collision_with_boundaries(self, snake_start):
        #check to see if the snake is still within the walls
        if snake_start[0] >= 500 or snake_start[0] < 0 or snake_start[1] >= 500 or snake_start[1] < 0:
            return 1
        else:
            return 0


    def collision_with_self(self, snake_start, snake_position):
        #when the head collides with other parts of its body
        if snake_start in snake_position[1:]:
            return 1
        else: #if no collision
            return 0


    def blocked_directions(self, snake_position):
        """Calculate directions vector for checking which direction is blocked"""
        #direction is calculated relative from head to its second part
        current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

        left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
        right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

        is_front_blocked = self.is_direction_blocked(snake_position, current_direction_vector)
        is_left_blocked = self.is_direction_blocked(snake_position, left_direction_vector)
        is_right_blocked = self.is_direction_blocked(snake_position, right_direction_vector)

        return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked


    def is_direction_blocked(self, snake_position, current_direction_vector):
        #create a next step 
        next_step = snake_position[0] + current_direction_vector
        #check collision of the educated guess on next step
        if self.collision_with_boundaries(next_step) == 1 or self.collision_with_self(next_step.tolist(), snake_position) == 1:
            return 1
        else:
            return 0


    def randDirection(self, snake_position, angle_with_apple):
        """Generate a random direction based on relative angle from snake's head to apple"""
        direction = 0
        if angle_with_apple > 0:
            direction = 1
        elif angle_with_apple < 0:
            direction = -1
        else:
            direction = 0

        return self.direction_vector(snake_position, angle_with_apple, direction)


    def direction_vector(self, snake_position, angle_with_apple, direction):
        """Calculate direction vector between snake and apple"""
        current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
        left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
        right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

        new_direction = current_direction_vector

        if direction == -1:
            new_direction = left_direction_vector
        if direction == 1:
            new_direction = right_direction_vector

        button_direction = self.gen_button(new_direction)

        return direction, button_direction


    def gen_button(self, new_direction):
        """Generate an arrow-key direction"""
        button_direction = 0
        if new_direction.tolist() == [10, 0]:
            button_direction = 1
        elif new_direction.tolist() == [-10, 0]:
            button_direction = 0
        elif new_direction.tolist() == [0, 10]:
            button_direction = 2
        else:
            button_direction = 3

        return button_direction


    def angle_with_food(self, snake_position, food_position):
        """Calculate relative angle from snake to food"""
        #grab direction vectors
        food_dirv = np.array(food_position) - np.array(snake_position[0])
        snake_dirv = np.array(snake_position[0]) - np.array(snake_position[1])

        #normalize the direction vectors
        norm_food_dirv = np.linalg.norm(food_dirv)
        norm_snake_dirv = np.linalg.norm(snake_dirv)

        #if normalized value is 0 => set to 10
        if norm_food_dirv == 0:
            norm_food_dirv = 10
        if norm_snake_dirv == 0:
            norm_snake_dirv = 10

        #grab actual normalized vectors
        norm_food_dirv = food_dirv / norm_food_dirv
        norm_snake_dirv = snake_dirv / norm_snake_dirv

        #calulate angle from normalized vectors
        angle = self.Angle(norm_food_dirv, norm_snake_dirv)

        return angle, snake_dirv, norm_food_dirv, norm_snake_dirv

    def Angle(self, a, b):
        #sub method for calculating angle
        result = math.atan2(a[1] * b[0] - a[0] *  b[1], a[1] * b[1] + a[0] * b[0]) / math.pi 
        return result

    def play_game(self, snake_start, snake_position, food_position, button_direction, score):
        crashed = False
        while crashed is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    crashed = True

            self.display.fill((0, 100, 0))

            self.display_food(food_position, self.display)
            self.display_snake(snake_position, self.display)

            snake_position, food_position, score = self.move_snake(snake_start, snake_position, food_position,
                                                                button_direction, score)
            pygame.display.set_caption("SCORE: " + str(score))
            pygame.display.update()
            self.clock.tick(50000)

            return snake_position, food_position, score