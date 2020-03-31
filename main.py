from train import *
from test import *
from game import *

import tensorflow
from keras.models import Sequential, model_from_json
from keras.layers import Dense


def train(games=1000, iterations=100000):
    display_width = 500
    display_height = 500

    pygame.init()
    display=pygame.display.set_mode((display_width,display_height))
    clock=pygame.time.Clock()

    game = Snake(display, clock)
    train = TrainSnake(game, games, iterations)
    trainX, trainY = train.generate_training_data()

    trainX = np.array(trainX)
    trainY = np.array(trainY)
    
    #create model 
    model = Sequential()
    model.add(Dense(units=12, input_dim=7, activation="relu"))
    model.add(Dense(units=12, input_dim=7, activation="relu"))
    model.add(Dense(units=12, input_dim=7, activation="relu"))
    model.add(Dense(units=12, input_dim=7, activation="relu"))
    model.add(Dense(units=12, input_dim=7, activation="relu"))
    model.add(Dense(units=12, input_dim=7, activation="relu"))
    model.add(Dense(units=12, input_dim=7, activation="relu"))

    #output
    model.add(Dense(3, input_dim=7, activation="softmax"))
    
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
    model.fit(trainX.reshape(-1,7), trainY.reshape(-1,3), epochs=50, batch_size=200, shuffle=10, use_multiprocessing=True )

    model.save_weights("train_weights.h5")
    model_json = model.to_json()

    with open('trained_model.json', 'w') as json:
        json.write(model_json)

def test():
    display_width = 500
    display_height = 500

    pygame.init()
    display=pygame.display.set_mode((display_width,display_height))
    clock=pygame.time.Clock()

    json_file = open('trained_model.json', 'r')
    load_json = json_file.read()

    game = Snake(display, clock)
    self_play_snake = TestSnake(game, display, clock)
    model = model_from_json(load_json)
    model.load_weights('train_weights.h5')
    
    best, avg = self_play_snake.self_play(model, 1000, 100000)

    print(best, avg)

def main():
    #train() 
    test()
if __name__ == "__main__":
    main()

