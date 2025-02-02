"""
This module contains the needed tools to train a Convolutive Neural Network to learn from
the MNIST images (a collection of handwritten digits images).
"""

import tensorflow as tf
import cv2

import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model

import sys
sys.path.append('.')
import vis

def load_data():
    """
    This function loads the data and keeps only the classes to use.
    """

    # We retrieve data from keras
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # We keep only the right classes
    idx_train = np.isin(y_train, CLASSES)
    idx_test = np.isin(y_test, CLASSES)

    return (x_train[idx_train], y_train[idx_train]), (x_test[idx_test], y_test[idx_test])


def prepare_input(x):
    """
    This function prepares the input.
    """
    x = x.reshape(x.shape+(1,))
    x = x/255.
    return x

def prepare_output(y):
    """
    This function prepares the labels
    """
    # First transformation
    for i, c in enumerate(CLASSES):
        y[y == c] = i
    # Second transformation
    y = to_categorical(y, len(CLASSES))
    return y

def build_model(input_shape, nb_classe):
    """
    This function builds the neural network that will be used for classification.
    """
    tf.random.set_seed(SEED)
    
    model = Sequential(name='lenet')

    ##################
    # YOUR CODE HERE #
    ##################

    

    return model

def train_model(model, data_train, data_test, batch_size, epoch=20):
    """This function trains the model using data train. 
       The trained model is tested at each epoch, 
       and automatically stops the traing to avoid overfit.
    """
    callbacks_list = [ 
        EarlyStopping(monitor='val_accuracy',  # the parameter to watch on
                      patience=3,              # max number of 'val_accuracy' decreases
                      verbose=1)
    ]
    tf.random.set_seed(SEED)

    x_train, y_train = data_train
    x_test, y_test   = data_test

    hist = model.fit(x_train, y_train,
                     validation_data=(x_test, y_test),
                     epochs=epoch, 
                     batch_size=batch_size, 
                     callbacks=callbacks_list)

    return hist

if __name__ == "__main__":

    BATCH_SIZE = 128
    CLASSES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    SEED = 12
    np.random.seed(SEED)      

    SHOW_SAMPLES = 1
    SHOW_WEIGHTS = 1
    SHOW_ACTIV   = 1

    print("\n1) Loading dataset:")
    print("-------------------")
    (x_train, y_train), (x_test, y_test) = load_data()
    print(f"x_train is a numpy array of shape {format(x_train.shape)}")
    print(f"y_train is a numpy array of shape {format(y_train.shape)}")
    input("Answer questions in 2.1 and press enter to continue...")

    if SHOW_SAMPLES:
        print("\n2) Previewing raw data")
        print("----------------------")
        vis.preview_samples(x_train, y_train, "Samples")
        input("Answer questions in 2.2 and press enter to continue...")

    print("\n3) Preparing data")
    print("------------------")
    x_train = prepare_input(x_train)
    x_test  = prepare_input(x_test)
    y_train_orig = y_train
    y_train = prepare_output(y_train)
    y_test  = prepare_output(y_test)
    print(f"x_train is a numpy array of shape {format(x_train.shape)}")
    print(f"y_train is a numpy array of shape {format(y_train.shape)}")
    input("Answer questions in 2.3 and press enter to continue...")

    if SHOW_SAMPLES:
        print("\n4) Previewing prepared data")
        print("---------------------------")
        vis.preview_samples(x_train, y_train_orig, "Samples")
        input("Answer questions in 2.4 and press enter to continue...")

    print("\n5) Instantiating the model")
    print("--------------------------")
    model = build_model((28, 28, 1), (len(CLASSES)))
    print("Model is: {}".format(model.summary()))
    input("Answer questions in 2.5 and press enter to continue...")

    print("\n6) Compiling model")
    print("------------------")
    tf.random.set_seed(SEED)
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    input("Answer questions in 2.6 and press enter to continue...")

    print("\n7) Training time !")
    print("------------------")
    hist = train_model(model, 
                      (x_train, y_train), (x_test, y_test), 
                      BATCH_SIZE)    
    vis.plot_loss_accuracy(hist)                      
    input("Answer questions in 2.7 and press enter to continue...")

    if SHOW_WEIGHTS:
        print("\n8) Visualising weights")
        print("----------------------")
        vis.preview_kernels(model.weights[0].numpy(), "First Layer kernels")
        vis.preview_kernels(model.weights[2].numpy(), "Second Layer kernels")
        input("Answer questions in 2.8 and press enter to continue...")

    if SHOW_ACTIV:
        print("\n9) Visualising activations")
        print("--------------------------")
        while True:
            inpt = input("Enter the sample index to preview (to skip, just press enter): ")
            if not inpt:
                break
            else:
                idx = int(inpt)
                vis.preview_activations(model, x_train[idx:idx+1], "Activations of neural network for one sample")

    print("\n10) Saving the network")
    print("---------------------")
    inpt = input("Enter the path to save the network to (to skip,, just press enter): ")
    if inpt:
        model.save(inpt)
