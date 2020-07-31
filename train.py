from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import pickle
import time
from sklearn.model_selection import train_test_split
import numpy as np


def trainn(X, y, name):
    # pickle_in = open("X-real.pickle","rb")
    # X = pickle.load(pickle_in)

    # pickle_in = open("y-real.pickle","rb")
    # y = pickle.load(pickle_in)

    X=np.array(X/255.0)
    y=np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

    dense_layers = [0]
    layer_sizes = [64]
    conv_layers = [3]


    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = "{}-conv-{}-nodes-{}-dense-{}".format(conv_layer, layer_size, dense_layer, int(time.time()))
                print(NAME)

                model = Sequential()

                model.add(Conv2D(layer_size, (3, 3), input_shape=X_train.shape[1:]))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))

                for l in range(conv_layer-1):
                    model.add(Conv2D(layer_size, (3, 3)))
                    model.add(Activation('relu'))
                    model.add(MaxPooling2D(pool_size=(2, 2)))

                model.add(Flatten())

                for _ in range(dense_layer):
                    model.add(Dense(layer_size))
                    model.add(Activation('relu'))

                model.add(Dense(1))
                model.add(Activation('sigmoid'))

                model.compile(loss='binary_crossentropy',
                            optimizer='adam',
                            metrics=['accuracy'],
                            )

                model.fit(X_train, y_train,
                        batch_size=32,
                        epochs=5,
                        validation_split=0.3)


    _, accuracy = model.evaluate(X_test, y_test, verbose=0)

    print('Accuracy: %.2f' % (accuracy*100))
    model.save(str(name) + '.model')