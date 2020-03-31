from game import * 

class TestSnake():
    def __init__(self, snake, display, clock):
         self.display = display
         self.clock = clock 
         self.snake = snake

    def self_play(self, model, games=1000, steps=2000):
        max_score = 3
        avg_score = 0

        for _ in range(games):
            print("Game: ", _)
            current_snake, snake_pos, food_pos, score = self.snake.starting_positions()

            count_same_dir = 0
            prev_dir = 0

            for _ in range (steps):
                #array for predictions
                predictions = []

                current_dirv, is_front_blocked, is_left_blocked, is_right_blocked = self.snake.blocked_directions(snake_pos)

                #grab angle, snake direction, normalized food & snake direction vectors
                angle, snake_dirv, norm_food_dirv, norm_snake_dirv  = self.snake.angle_with_food(snake_pos, food_pos)

                pred_direction = np.argmax(np.array(model.predict
                (np.array([is_left_blocked, is_front_blocked, is_right_blocked, norm_food_dirv[0], norm_snake_dirv[0], norm_food_dirv[1], norm_snake_dirv[1]]).reshape(-1, 7)))) - 1

                if (pred_direction == prev_dir):
                    count_same_dir += 1
                
                else: 
                    count_same_dir = 0
                    prev_dir = pred_direction
                
                new_direction = np.array(snake_pos[0]) - np.array(snake_pos[1])

                if (pred_direction == -1):
                    new_direction = np.array([new_direction[1], -new_direction[0]])
                
                if (pred_direction == 1):
                    new_direction = np.array([-new_direction[1], new_direction[0]])

                button = self.snake.gen_button(new_direction)

                next_step = snake_pos[0] + current_dirv

                #check collision
                if (self.snake.collision_with_boundaries(snake_pos[0]) == 1 or self.snake.collision_with_self(next_step.tolist(), snake_pos) == 1):
                    break 

                snake_pos, food_pos, score = self.snake.play_game(current_snake, snake_pos, food_pos, button, score)

                if (score > max_score):
                    max_score = score 
                    
            print("current max score: ", max_score)
            avg_score += score 
        
        return max_score, avg_score / games