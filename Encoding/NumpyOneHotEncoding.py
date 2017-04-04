import numpy as np
import MySQLdb

def one_hot_encode(x, n_classes):
    """
    One hot encode a list of sample labels. Return a one-hot encoded vector for each label.
    : x: List of sample Labels
    : return: Numpy array of one-hot encoded labels
     """
    return np.eye(n_classes)

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="MSTDB",  # name of the data base
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')

cur = db.cursor()
listOfUnDiacritizedCharacter = "SELECT Distinct undiacritizedCharacter FROM ListOfPurifiedCharacters"
listOfDiacritizedCharacter = "SELECT diacritizedCharacter FROM ListOfPurifiedCharacters"

cur.execute(listOfUnDiacritizedCharacter);
rowsUnDiacritizedCharacter = cur.fetchall();

cur.execute(listOfDiacritizedCharacter);
rowsOfDiacritizedCharacter = cur.fetchall();

db.commit()

db.close()

n_UnDiacritizedClasses = len(rowsUnDiacritizedCharacter)
n_DiacritizedClasses = len(rowsOfDiacritizedCharacter)

one_hot_list_ForUnDiacritizedCharacters = one_hot_encode(listOfUnDiacritizedCharacter, n_UnDiacritizedClasses)
one_hot_list_ForDiacritizedCharacters = one_hot_encode(listOfDiacritizedCharacter, n_DiacritizedClasses)

print(one_hot_list_ForDiacritizedCharacters)
print(one_hot_list_ForUnDiacritizedCharacters)


