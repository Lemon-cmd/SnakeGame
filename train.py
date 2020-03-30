from tqdm import tqdm

class TrainSnake():
    def __init__(self, game, epochs=1, batch=10):
        self.epochs = epochs
        self.batches = batch
        self.snake = game
        self.trainY = []
        self.trainX = []
    def generate_training_data_y(self, snake_position, angle_with_food, button, direction, training_data_y,
                                is_front_blocked, is_left_blocked, is_right_blocked):
        if direction == -1:
            if is_left_blocked == 1:
                if is_front_blocked == 1 and is_right_blocked == 0:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, 1)
                    self.trainY.append([0, 0, 1])
                elif is_front_blocked == 0 and is_right_blocked == 1:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, 0)
                    self.trainY.append([0, 1, 0])
                elif is_front_blocked == 0 and is_right_blocked == 0:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, 1)
                    self.trainY.append([0, 0, 1])

            else:
                self.trainY.append([1, 0, 0])

        elif direction == 0:
            if is_front_blocked == 1:
                if is_left_blocked == 1 and is_right_blocked == 0:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, 1)
                    self.trainY.append([0, 0, 1])
                elif is_left_blocked == 0 and is_right_blocked == 1:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, -1)
                    self.trainY.append([1, 0, 0])
                elif is_left_blocked == 0 and is_right_blocked == 0:
                    self.trainY.append([0, 0, 1])
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, 1)
            else:
                self.trainY.append([0, 1, 0])
        else:
            if is_right_blocked == 1:
                if is_left_blocked == 1 and is_front_blocked == 0:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, 0)
                    self.trainY.append([0, 1, 0])
                elif is_left_blocked == 0 and is_front_blocked == 1:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, -1)
                    self.trainY.append([1, 0, 0])
                elif is_left_blocked == 0 and is_front_blocked == 0:
                    direction, button = self.snake.direction_vector(snake_position, angle_with_food, -1)
                    self.trainY.append([1, 0, 0])
            else:
                self.trainY.append([0, 0, 1])

        return direction, button, self.trainY

    def generate_training_data(self):
        for _ in tqdm(range(self.epochs)):
            snake_start, snake_position, food_position, score = self.snake.starting_positions()
            prev_apple_distance = self.snake.food_from_snake(food_position, snake_position)

            for _ in range(self.batches): 
                #grab angle, snake direction, normalized food & snake direction vectors
                angle, snake_dirv, norm_food_dirv, norm_snake_dirv  = self.snake.angle_with_food(snake_position, food_position)

                #grab direction and button direction
                direction, button = self.snake.randDirection(snake_position, angle)

                #grab current direction vector, and boolean values for checking front,left, and right
                current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = self.snake.blocked_directions(snake_position)

                #grab direction, button and output
                direction, button, self.trainY = self.generate_training_data_y(snake_position, angle,
                                                                                        button, direction,
                                                                                        self.trainY, is_front_blocked,
                                                                                        is_left_blocked, is_right_blocked)

                #if there is no where to go; front, left, right are all blocked; terminate
                if is_front_blocked == 1 and is_left_blocked == 1 and is_right_blocked == 1:
                    break

                self.trainX.append(
                    [is_left_blocked, is_front_blocked, is_right_blocked, norm_food_dirv[0], \
                    norm_snake_dirv[0], norm_food_dirv[1], norm_snake_dirv[1]])

                snake_position, food_position, score = self.snake.play_game(snake_start, snake_position, food_position,
                                                                button, score)

        return self.trainX, self.trainY


