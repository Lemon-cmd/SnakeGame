from train import *
from game import *

from keras.models import Sequential
from keras.layers import Dense

def main():
    display_width = 500
    display_height = 500

    pygame.init()
    display=pygame.display.set_mode((display_width,display_height))
    clock=pygame.time.Clock()

    game = Snake(display, clock)
    train = TrainSnake(game, 100, 1000)
    trainX, trainY = train.generate_training_data()

if __name__ == "__main__":
    main()

