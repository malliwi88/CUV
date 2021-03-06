import sys
from multi_layer_perceptron import MLP
from switchtohost import switchtohost
from MNIST_data import MNIST_data
import numpy as np
import cuv_python as cp

if __name__ == "__main__":
    try:
        if sys.argv[2] == "--host":
            switchtohost()
    except: pass

    try:
        mnist = MNIST_data(sys.argv[1]);
    except:
        print('Usage: %s {path of MNIST dataset} [--host]' % sys.argv[0])
        sys.exit(1)

    cp.initialize_mersenne_twister_seeds(0)

    # obtain training/test data
    train_data, train_labels = mnist.get_train_data()
    test_data,  test_labels  = mnist.get_test_data()

    # set layer sizes
    sizes = [train_data.shape[0], 128, train_labels.shape[0]]

    print('Initializing MLP...')
    mlp = MLP(sizes, 100)

    print('Training MLP...')
    try:
        mlp.fit(train_data, train_labels, 200)
    except KeyboardInterrupt:
        pass

    print('Testing MLP...')
    predictions = mlp.predict(test_data)
    print("test error: %f" % np.mean((predictions != np.argmax(test_labels, axis=0))))

    print('done.')
