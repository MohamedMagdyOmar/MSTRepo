# -*- coding: utf-8 -*-
import re
import unicodedata
import binascii
# s = "ثُمَّ"
f = open("/home/mohamed/Desktop/Game3Sa7e7.txt", 'r')
read_data = f.readlines()
f.close()

listOfPunctuationBySymbol = [' .', ' :', '«', '»', '،', '؛', '؟', '.(', ').', ':(', '):', '» .']

listOfArabicDiacriticsUnicode = [["064b", "064c", "064d", "064e", "064f", "0650", "0651", "0652"],
                                 [1, 2, 3, 4, 5, 6, 8, 7]]

listOfArabicDiacriticsUnicode2 = [("064b", 1), ("064c", 2), ("064d", 3), ("064e", 4), ("064f", 5), ("0650", 6),
                                  ("0651", 8), ("0652", 7)]
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

listOfUnDiacritizedWord = []
letterCount = 0
prevCharWasDiac = False
letterFoundFlag = False
lettersWithNoDiac = 0
lettersWithOneDiac = 0
lettersWithTwoDiac = 0

listOfLettersWith2Diac = []
listOfEncodedWords = []
x = 0b10001

for word in listOfWords:
    if not word in listOfPunctuationBySymbol:
        word = word.decode('utf-8', 'ignore')
        nfkd_form = unicodedata.normalize('NFKD', word)
        unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        listOfUnDiacritizedWord.append(unDiacritizedWord)

        letterFoundFlag = False
        prevCharWasDiac = False

        for c in nfkd_form:

            if not unicodedata.combining(c):  # letter
                letterFoundFlag = True
                lettersWithNoDiac += 1

                hexAsString = hex(ord(c))[2:].zfill(4)
                binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
                integer = int(hexAsString, 16)
                maskedInt = integer & 255;
                maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
                shiftedInt = maskedInt << 4
                shiftedIntInBin = bin(shiftedInt)
                listOfEncodedWords.append(bin(shiftedInt)[2:].zfill(16))

            elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':  # first diacritization
                lettersWithOneDiac += 1
                prevCharWasDiac = True
                lettersWithNoDiac -= 1
                letterFoundFlag = False

                hexDiacAsString = hex(ord(c))[2:].zfill(4)
                binaryAsString = bin(int(hexDiacAsString, 16))[2:].zfill(16)

                integerDiac=listOfArabicDiacriticsUnicode[1][listOfArabicDiacriticsUnicode[0].index(hexDiacAsString)]
                integerDiacAfterORing = shiftedInt | integerDiac
                listOfEncodedWords.pop()
                listOfEncodedWords.append(bin(integerDiacAfterORing)[2:].zfill(16))

            elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization
                lettersWithTwoDiac += 1
                lettersWithOneDiac -= 1
                letterFoundFlag = False
                prevCharWasDiac = False
                listOfLettersWith2Diac.append(c)

                hexSecDiacAsString = hex(ord(c))[2:].zfill(4)
                integerSecDiac = listOfArabicDiacriticsUnicode[1][listOfArabicDiacriticsUnicode[0].index(hexSecDiacAsString)]
                integerSecDiacAfterORing = integerDiacAfterORing | integerSecDiac
                listOfEncodedWords.pop()
                listOfEncodedWords.append(bin(integerSecDiacAfterORing)[2:].zfill(16))


for item in listOfEncodedWords:
    print item












