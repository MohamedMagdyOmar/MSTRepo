import pandas as pd

s = pd.Series(list('abcaaaghfiaaaaaaakka'))

# print s
AList = []
BList = []

for x in range(0, 10000):
    AList.append(x);

for y in range(0,10000):
    BList.append(y)


# df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': ['x', 'a', 'c']})
df = pd.DataFrame({'A': AList, 'B': BList})
one_hot = pd.get_dummies(df['B'])
df = df.drop('B', axis = 1)
df = df.join(one_hot)
