# -*- coding: utf-8 -*-
import re
import unicodedata
import MySQLdb
import os, fnmatch

# looping over all txt documents in a folder
#def findFiles (path, filter):
#    for root, dirs, files in os.walk(path):
#        for file in fnmatch.filter(files, filter):
#            yield os.path.join(root, file)

#for textFile in findFiles(r'/home/mohamed/Desktop/MSTRepo/MSTRepo/PaperCorpus', '*.txt'):
    #print(textFile)

f = open('/home/mohamed/Desktop/الجامع الصحيح المسمى صحيح مسلم.txt', 'r')
read_data = f.readlines()
f.close()

listOfPunctuationBySymbol = [' .', ' :', '«', '»', '،', '؛', '؟', '.(', ').', ':(', '):', '» .']

listOfArabicDiacriticsUnicode = [["064b", "064c", "064d", "064e", "064f", "0650", "0651", "0652"],
                                 [1, 2, 3, 4, 5, 6, 8, 7]]

listOfWords = []
listOfWordsInSent = []
ListOfWordsWithPunctuation = []
wordCount = 0

for eachSentence in read_data:
    wordsInSentence = eachSentence.split()
    for word in wordsInSentence:
        word = re.sub('[-;}()0123456789/]', '', word)
        word = re.sub('[.]', ' .', word)
        word = re.sub('["{"]', '', word)
        word = re.sub('[:]', ' :', word)

        if not (word == ''):
            listOfWords.append(word)

sentenceCount = 1

for word in listOfWords:

    if not (word in listOfPunctuationBySymbol):
        wordCount += 1
        listOfWordsInSent.append([word, sentenceCount])
        ListOfWordsWithPunctuation.append([word, sentenceCount])
    else:
        ListOfWordsWithPunctuation.append([word, sentenceCount])
        sentenceCount += 1

prevCharWasDiac = False
letterFoundFlag = False

listOfTargetSequenceEncodedWords = []

# Encoding Target Sequence [Diacritized Character]
for word in listOfWords:
    if not word in listOfPunctuationBySymbol:
        word = word.decode('utf-8', 'ignore')

        letterFoundFlag = False
        prevCharWasDiac = False

        for c in word:

            if not unicodedata.combining(c):  # letter
                letterFoundFlag = True

                hexAsString = hex(ord(c))[2:].zfill(4)

                binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
                integer = int(hexAsString, 16)
                maskedInt = integer & 255;
                maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
                shiftedInt = maskedInt << 4
                shiftedIntInBin = bin(shiftedInt)
                listOfTargetSequenceEncodedWords.append(bin(shiftedInt)[2:].zfill(16))

            elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':  # first diacritization
                prevCharWasDiac = True
                letterFoundFlag = False

                hexDiacAsString = hex(ord(c))[2:].zfill(4)

                binaryAsString = bin(int(hexDiacAsString, 16))[2:].zfill(16)

                integerDiac=listOfArabicDiacriticsUnicode[1][listOfArabicDiacriticsUnicode[0].index(hexDiacAsString)]
                integerDiacAfterORing = shiftedInt | integerDiac
                listOfTargetSequenceEncodedWords.pop()
                listOfTargetSequenceEncodedWords.append(bin(integerDiacAfterORing)[2:].zfill(16))

            elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization

                letterFoundFlag = False
                prevCharWasDiac = False

                hexSecDiacAsString = hex(ord(c))[2:].zfill(4)

                integerSecDiac = listOfArabicDiacriticsUnicode[1][listOfArabicDiacriticsUnicode[0].index(hexSecDiacAsString)]
                integerSecDiacAfterORing = integerDiacAfterORing | integerSecDiac
                listOfTargetSequenceEncodedWords.pop()
                listOfTargetSequenceEncodedWords.append(bin(integerSecDiacAfterORing)[2:].zfill(16))


listOfUnDiacritizedWord = []
listOfInputSequenceEncodedWords = []

# Encoding Input Sequence [unDiacritized Character]
for word in listOfWords:
    if not word in listOfPunctuationBySymbol:

        word = word.decode('utf-8', 'ignore')
        nfkd_form = unicodedata.normalize('NFKD', word)

        unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        listOfUnDiacritizedWord.append(unDiacritizedWord)

        for c in word:

            if not unicodedata.combining(c):  # letter
                letterFoundFlag = True

                hexAsString = hex(ord(c))[2:].zfill(4)

                binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
                integer = int(hexAsString, 16)
                maskedInt = integer & 255;
                maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
                shiftedInt = maskedInt << 4
                shiftedIntInBin = bin(shiftedInt)
                listOfInputSequenceEncodedWords.append(bin(shiftedInt)[2:].zfill(16))


for item in range(0,len(listOfInputSequenceEncodedWords)):
    #print hex(int(item,2))
    listOfInputSequenceEncodedWords[item] = str(listOfInputSequenceEncodedWords[item])
    print listOfInputSequenceEncodedWords[item]



letterFoundFlag = False
prevCharWasDiac = False

first = ""
second = ""
third = ""
overall = ""
spaChar = unicodedata.normalize('NFC', word)
diacritizedCharacter = []
unDiacritizedCharacter = []

# extracting each character from words with its diacritization
for word in listOfWords:
    if not word in listOfPunctuationBySymbol:
        word = word.decode('utf-8', 'ignore')

        # removing diacritization from characters
        nfkd_form = unicodedata.normalize('NFKD', word)
        unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        listOfUnDiacritizedWord.append(unDiacritizedWord)

        spaChar = unicodedata.normalize('NFC', word)
        for c in spaChar:
            if not unicodedata.combining(c):
              first = c
              letterFoundFlag = True
              overall = c
              comp = unicodedata.normalize('NFC', c)
              diacritizedCharacter.append(comp)
            elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':
                second = c
                prevCharWasDiac = True
                letterFoundFlag = False
                overall +=c
                comp = unicodedata.normalize('NFC', overall + c)
                diacritizedCharacter.pop()
                diacritizedCharacter.append(comp)
            elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization
                third = c
                letterFoundFlag = False
                prevCharWasDiac = False
                overall += c
                comp = unicodedata.normalize('NFC', overall + c)
                diacritizedCharacter.pop()
                diacritizedCharacter.append(comp)


for word in listOfUnDiacritizedWord:
    for char in word:
        unDiacritizedCharacter.append(char)

db = MySQLdb.connect(host="127.0.0.1",    # your host, usually localhost
                     user="root",         # your username
                     passwd="Islammega88",  # your password
                     db="MSTDB", # name of the data base
                     use_unicode=True,
                     charset="utf8",
                     init_command='SET NAMES UTF8')

cur = db.cursor()

for x in range(0,len(listOfInputSequenceEncodedWords)):
    cur.execute("INSERT INTO EncodedWords(InputSequenceEncodedWords,TargetSequenceEncodedWords,diacritizedCharacter,undiacritizedCharacter) VALUES (%s,%s,%s,%s)",
                (listOfInputSequenceEncodedWords[x],listOfTargetSequenceEncodedWords[x],diacritizedCharacter[x],unDiacritizedCharacter[x]))

db.commit()

db.close()