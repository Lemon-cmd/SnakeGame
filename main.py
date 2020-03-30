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

    trainX = np.array(trainX)
    trainY = np.array(trainY)
    
    #create model 
    model = Sequential()
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

if __name__ == "__main__":
    main()

