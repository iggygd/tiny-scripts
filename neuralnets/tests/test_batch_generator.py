import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import data

def test_batch_generator():
    _, _, train_images, train_labels, _, _, _ = data.mnist.Preprocessed()

    for image, label in data.mnist.batch_generator(train_images, train_labels, 32):
        print(image, label)

if __name__ == '__main__':
    test_batch_generator()