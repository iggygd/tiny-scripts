import parse
import numpy as np

class mnist():
    def load():
        train_images_path = r"data/train-images-idx3-ubyte.gz"
        train_labels_path = r"data/train-labels-idx1-ubyte.gz"
        test_images_path = r"data/t10k-images-idx3-ubyte.gz"
        test_labels_path = r"data/t10k-labels-idx1-ubyte.gz"

        train_images = parse.mnist(train_images_path) 
        train_labels = parse.mnist(train_labels_path)
        test_images = parse.mnist(test_images_path)
        test_labels = parse.mnist(test_labels_path)
        
        return train_images, train_labels, test_images, test_labels

    def replace(a, i, v):
        a[i] = v
        return a

    def encode(i, defs):
        return defs[i.tostring()]

    def OneHot(labels, unique_list):
        base = np.zeros(len(unique_list))
        cat2vec = {i.to_bytes(1, byteorder='big'): mnist.replace(np.copy(base), unique_list.index(i), 1) for i in unique_list}
        return np.apply_along_axis(mnist.encode, 1, labels, cat2vec), cat2vec

    def Preprocessed():
        #Data Info
        width = 28
        height = 28
        input_size = width*height

        outputs = (0,1,2,3,4,5,6,7,8,9)
        output_size = len(outputs)

        #Loading
        train_images, train_labels, test_images, test_labels = mnist.load()

        #Preprocessing
        train_images = (train_images-127.5)/255.0
        test_images = (test_images-127.5)/255.0
        train_labels, _ = mnist.OneHot(train_labels, outputs)
        test_labels, encoding = mnist.OneHot(test_labels, outputs)

        return input_size, output_size, train_images, train_labels, test_images, test_labels, encoding

    def batch_generator(images, labels, batch_size):
        i = 0
        num = len(images)
        while i < num:
            to = i+batch_size
            if to <= num:
                yield images[i:to], labels[i:to]
                i = to
            else:
                yield images[i:num], labels[i:num]
                raise StopIteration

