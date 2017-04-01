import numpy as np

def one_hot_encode(x, n_classes):
    """
    One hot encode a list of sample labels. Return a one-hot encoded vector for each label.
    : x: List of sample Labels
    : return: Numpy array of one-hot encoded labels
     """
    return np.eye(n_classes)[x]

def main():
    newList = [];
    for x in range (0,1000):
        newList.append(x);
        print newList[x];
    list = [0,1,2,3,4,3,2,1,0]
    n_classes = 1000
    one_hot_list = one_hot_encode(newList, n_classes)
    print(one_hot_list)

if __name__ == "__main__":
    main()

