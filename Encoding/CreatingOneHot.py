# -*- coding: utf-8 -*-

import MySQLdb
import NumpyOneHotEncoding as encoding
import numpy as np

db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                     user="root",  # your username
                     passwd="Islammega88",  # your password
                     db="MSTDB",  # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

sqlQuery = "select distinct InputSequenceEncodedWords,TargetSequenceEncodedWords,diacritizedCharacter," \
           "undiacritizedCharacter " \
           "from EncodedWords order by undiacritizedCharacter asc"

cur.execute(sqlQuery)

rowsOfEncodedWordsInDB = cur.fetchall()
rowsOfEncodedWordsInDB = np.array(rowsOfEncodedWordsInDB)

listOfUnDiacritizedCharacter = np.array(rowsOfEncodedWordsInDB)
listOfUnDiacritizedCharacter = listOfUnDiacritizedCharacter[:, 3]
listOfUniqueUnDiacritizedCharacter = list(set(list(listOfUnDiacritizedCharacter)))

for x in range(0, len(listOfUniqueUnDiacritizedCharacter)):
    listOfUniqueUnDiacritizedCharacter[x] = (listOfUniqueUnDiacritizedCharacter[x]).encode('utf-8')

listOfDiacritizedCharacter = np.array(rowsOfEncodedWordsInDB)
listOfDiacritizedCharacter = listOfDiacritizedCharacter[:, 2]
listOfDiacritizedCharacter = list(listOfDiacritizedCharacter);

for x in range(0, len(listOfDiacritizedCharacter)):
    listOfDiacritizedCharacter[x] = (listOfDiacritizedCharacter[x]).encode('utf-8')

one_hot_list__for_un_diacritized_characters, one_hot_list__for_diacritized_characters = \
    encoding.encodeMyCharacter(listOfUniqueUnDiacritizedCharacter, listOfDiacritizedCharacter)

# filling "UnDiacOneHotEncoding and DiacOneHotEncoding" Tables
print len(one_hot_list__for_un_diacritized_characters);
print len(one_hot_list__for_diacritized_characters);
'''
for x in range(0, len(one_hot_list__for_un_diacritized_characters)):
    cur.execute("insert into UnDiacOneHotEncoding (UnDiacritizedCharacter,UnDiacritizedCharacterOneHotEncoding)"
                " VALUES (%s,%s)",
                (listOfUniqueUnDiacritizedCharacter[x], one_hot_list__for_un_diacritized_characters[x]))

for x in range(0, len(one_hot_list__for_diacritized_characters)):
    cur.execute("insert into DiacOneHotEncoding (DiacritizedCharacter,DiacritizedCharacterOneHotEncoding)"
                " VALUES (%s,%s)",
                (listOfDiacritizedCharacter[x], one_hot_list__for_diacritized_characters[x]))

db.commit()

db.close()
'''