import numpy as np

newList = [];
for x in range(0, 100000):
    newList.append(x);
    print newList[x];
nb_classes = 100000
targets = np.newList.reshape(-1)
#targets = np.array([[2, 3, 4, 0]]).reshape(-1)
one_hot_targets = np.eye(nb_classes)[targets]
print one_hot_targets