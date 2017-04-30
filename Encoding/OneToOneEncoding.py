# -*- coding: utf-8 -*-
import re
import unicodedata
import MySQLdb
import math
import os
import datetime

diacritizedCharacter = []
unDiacritizedCharacter = []
listOfDBWords = []
listOfDbSentenceNumber = []
listOfPunctuationBySymbol = [u' .', u'.', u' :', u'«', u'»', u'،', u'؛', u'؟', u'.(', u').', u':(', u'):', u'» .', u'».']

listOfArabicDiacriticsUnicode = [["064b", "064c", "064d", "064e", "064f", "0650", "0651", "0652"],
                                 [1, 2, 3, 4, 5, 6, 8, 7]]


def declareGlobalVariables():
    global wordCount
    wordCount = 0
    global sentenceCount
    sentenceCount = 1

def findFiles():
    global listOfFilesPathes
    global listOfDocName
    listOfFilesPathes = []
    listOfDocName = []
    for file in os.listdir("D:\MasterRepo\MSTRepo\PaperCorpus\Doc"):
        if file.endswith(".txt"):
            listOfFilesPathes.append(os.path.join("D:\MasterRepo\MSTRepo\PaperCorpus\Doc", file))
            listOfDocName.append(file)
            print(os.path.join("D:\MasterRepo\MSTRepo\PaperCorpus\Doc", file))


def readDoc(eachdoc):
    global read_data
    global docName
    f = open(listOfFilesPathes[eachdoc], 'r')
    docName = listOfDocName[eachdoc]
    read_data = f.readlines()
    f.close()


def extractAndCleanWordsFromDoc():
    global listOfWords
    listOfWords = []
    for eachSentence in read_data:
        wordsInSentence = eachSentence.split()
        for word in wordsInSentence:
            word = word.decode('utf-8', 'ignore') # variable line

            word = re.sub(u'[-;}()0123456789/]', '', word)
            word = re.sub(u'["{"]', '', word)
            word = re.sub(u'[:]', ' :', word)

            word = re.sub(u'[ـ]', '', word)
            word = re.sub(u'[`]', '', word)
            word = re.sub(u'[[]', '', word)
            word = re.sub(u'[]]', '', word)
            word = re.sub(u'[L]', '', word)
            if not (word == u''):
                listOfWords.append(word)


def extractSentencesFromDoc():
    global wordCount
    global listOfWordsInSent
    global ListOfWordsWithPunctuation
    global sentenceCount
    #wordCount = 0
    listOfWordsInSent = []
    ListOfWordsWithPunctuation = []
    #sentenceCount = 1

    if docName != 'quran-simple.txt':
        for word in listOfWords:

            if not (word in listOfPunctuationBySymbol):
                if word.find(u'.') != -1:
                    wordCount += 1

                    ListOfWordsWithPunctuation.append([word, sentenceCount])

                    word = re.sub(u'[.]', '', word)
                    if word != u'':
                        listOfWordsInSent.append([word, sentenceCount])
                    sentenceCount += 1
                else:
                    wordCount += 1
                    listOfWordsInSent.append([word, sentenceCount])
                    ListOfWordsWithPunctuation.append([word, sentenceCount])
            else:
                ListOfWordsWithPunctuation.append([word, sentenceCount])
                sentenceCount += 1
    else:
        sentenceCount = 0
        wordCount = 0
        for eachVersus in read_data:
            sentenceCount += 1
            eachWordInVersus = eachVersus.split()
            for eachWord in eachWordInVersus:
                wordCount += 1
                listOfWordsInSent.append([eachWord, sentenceCount])


def encodingDiacritizedCharacter():
    global listOfTargetSequenceEncodedWords
    global listOfInputSequenceEncodedWordsInHexFormat
    global listOfTargetSequenceEncodedWordsInHexFormat
    global listOfInputSequenceEncodedWords
    global listOfUnDiacritizedWord
    listOfInputSequenceEncodedWords = []
    listOfUnDiacritizedWord = []
    listOfTargetSequenceEncodedWords = []
    listOfInputSequenceEncodedWordsInHexFormat = []
    listOfTargetSequenceEncodedWordsInHexFormat = []

    for word in listOfWords:
        if not word in listOfPunctuationBySymbol:
            if word.find(u'.') != -1:
                word = re.sub(u'[.]', '', word)
#            word = word.decode('utf-8', 'ignore') may be need to return itback

            nfkd_form = unicodedata.normalize('NFKD', word)

            unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
            listOfUnDiacritizedWord.append(unDiacritizedWord)

            letterFoundFlag = False
            prevCharWasDiac = False

            for c in word:

                if not unicodedata.combining(c):  # letter
                    letterFoundFlag = True

                    hexAsString = hex(ord(c))[2:].zfill(4)

                    binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
                    integer = int(hexAsString, 16)
                    maskedInt = integer & 255
                    maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
                    shiftedInt = maskedInt << 4
                    shiftedIntInBin = bin(shiftedInt)

                    listOfTargetSequenceEncodedWordsInHexFormat.append(hex(shiftedInt))
                    listOfTargetSequenceEncodedWords.append(bin(shiftedInt)[2:].zfill(16))
                    listOfInputSequenceEncodedWordsInHexFormat.append(hex(shiftedInt))
                    listOfInputSequenceEncodedWords.append(str(bin(shiftedInt)[2:].zfill(16)))

                elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':  # first diacritization
                    prevCharWasDiac = True
                    letterFoundFlag = False

                    hexDiacAsString = hex(ord(c))[2:].zfill(4)

                    binaryAsString = bin(int(hexDiacAsString, 16))[2:].zfill(16)

                    integerDiac = listOfArabicDiacriticsUnicode[1][
                        listOfArabicDiacriticsUnicode[0].index(hexDiacAsString)]
                    integerDiacAfterORing = shiftedInt | integerDiac
                    listOfTargetSequenceEncodedWords.pop()
                    listOfTargetSequenceEncodedWords.append(bin(integerDiacAfterORing)[2:].zfill(16))

                    listOfTargetSequenceEncodedWordsInHexFormat.pop()
                    listOfTargetSequenceEncodedWordsInHexFormat.append(hex(integerDiacAfterORing))
                elif prevCharWasDiac and c != u'ٔ' and c != u'ٕ':  # second diacritization

                    letterFoundFlag = False
                    prevCharWasDiac = False

                    hexSecDiacAsString = hex(ord(c))[2:].zfill(4)

                    integerSecDiac = listOfArabicDiacriticsUnicode[1][
                        listOfArabicDiacriticsUnicode[0].index(hexSecDiacAsString)]
                    integerSecDiacAfterORing = integerDiacAfterORing | integerSecDiac
                    listOfTargetSequenceEncodedWords.pop()
                    listOfTargetSequenceEncodedWords.append(bin(integerSecDiacAfterORing)[2:].zfill(16))
                    listOfTargetSequenceEncodedWordsInHexFormat.pop()
                    listOfTargetSequenceEncodedWordsInHexFormat.append(hex(integerSecDiacAfterORing))


# def encodingunDiacritizedCharacter():
#     global listOfUnDiacritizedWord
#     global listOfInputSequenceEncodedWords
#     listOfUnDiacritizedWord = []
#     listOfInputSequenceEncodedWords = []
#
#     for word in listOfWords:
#         if not word in listOfPunctuationBySymbol:
#
#             if word.find('.') != -1:
#                 word = re.sub('[.]', '', word)
#
#             word = word.decode('utf-8', 'ignore')
#             nfkd_form = unicodedata.normalize('NFKD', word)
#
#             unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
#             listOfUnDiacritizedWord.append(unDiacritizedWord)
#
#             for c in word:
#
#                 if not unicodedata.combining(c):  # letter
#                     letterFoundFlag = True
#
#                     hexAsString = hex(ord(c))[2:].zfill(4)
#
#                     binaryAsString = bin(int(hexAsString, 16))[2:].zfill(16)
#                     integer = int(hexAsString, 16)
#                     maskedInt = integer & 255
#                     maskedBinaryAsString = bin(integer & 255)[2:].zfill(16)
#                     shiftedInt = maskedInt << 4
#                     shiftedIntInBin = bin(shiftedInt)
#                     listOfInputSequenceEncodedWords.append(bin(shiftedInt)[2:].zfill(16))

# def convertToString():
#     for item in range(0, len(listOfInputSequenceEncodedWords)):
#         listOfInputSequenceEncodedWords[item] = str(listOfInputSequenceEncodedWords[item])


# first = ""
# second = ""
# third = ""
# overall = ""
# spaChar = unicodedata.normalize('NFC', word)

def extractEachCharacterFromWordWithItsDiacritization():
    letterFoundFlag = False
    prevCharWasDiac = False
    loopCount = 0
    first = ""
    second = ""
    third = ""
    overall = ""

    for word in listOfWords:

        if not word in listOfPunctuationBySymbol:

            if word.find(u'.') != -1:
                word = re.sub(u'[.]', '', word)

#            word = word.decode('utf-8', 'ignore') may be return back

            # removing diacritization from characters
            nfkd_form = unicodedata.normalize('NFKD', word)
            unDiacritizedWord = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

            sentenceNumber = listOfWordsInSent[loopCount][1]
            loopCount += 1
            spaChar = unicodedata.normalize('NFC', word)
            for c in spaChar:

                if not unicodedata.combining(c):
                    first = c
                    letterFoundFlag = True
                    overall = c
                    comp = unicodedata.normalize('NFC', c)
                    diacritizedCharacter.append(comp)

                    listOfDbSentenceNumber.append(sentenceNumber)

                    listOfDBWords.append(word)
                    listOfUnDiacritizedWord.append(unDiacritizedWord)
                    unDiacritizedCharacter.append(c)
                elif letterFoundFlag and c != u'ٔ' and c != u'ٕ':
                    second = c
                    prevCharWasDiac = True
                    letterFoundFlag = False
                    overall += c
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

                    # for word in listOfUnDiacritizedWord:
                    # for char in word:
                    #  unDiacritizedCharacter.append(char)


def connectToDB():
    global db
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="MSTDB",  # name of the data base
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')

    global cur
    cur = db.cursor()


def pushDataIntoDB():
    requiredPercentageForValidation = math.ceil((len(listOfInputSequenceEncodedWords) * 15) / 100)
    trainingCounter = len(listOfInputSequenceEncodedWords) - (requiredPercentageForValidation * 2)
    isTrainingDataIsFinished = False
    isValidationDataIsFinished = False
    # Part A : filling "Encoded Words" Table
    for x in range(0, len(listOfInputSequenceEncodedWords)):
        cur.execute(
            "INSERT INTO EncodedWords(InputSequenceEncodedWords,TargetSequenceEncodedWords,diacritizedCharacter,"
            "undiacritizedCharacter,InputSequenceEncodedWordsInHexFormat,TargetSequenceEncodedWordsInHexFormat) "
            "VALUES ( "
            "%s,%s,%s,%s,%s,%s)",
            (listOfInputSequenceEncodedWords[x], listOfTargetSequenceEncodedWords[x], diacritizedCharacter[x],
             unDiacritizedCharacter[x], listOfInputSequenceEncodedWordsInHexFormat[x],
             listOfTargetSequenceEncodedWordsInHexFormat[x]))

    #     if (trainingCounter >= 0 or prevSentenceNumber == listOfDbSentenceNumber[x]) and \
    #             (isTrainingDataIsFinished is False):
    #         prevSentenceNumber = listOfDbSentenceNumber[x]
    #         trainingCounter -= 1
    #         cur.execute(
    #             "INSERT INTO ParsedDocument(DocName, UnDiacritizedCharacter,DiacritizedCharacter,LetterType,"
    #             "SentenceNumber, "
    #             "Word, "
    #             "InputSequenceEncodedWords,TargetSequenceEncodedWords, InputSequenceEncodedWordsInHexFormat,"
    #             "TargetSequenceEncodedWordsInHexFormat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    #             (docName, unDiacritizedCharacter[x], diacritizedCharacter[x], 'training', listOfDbSentenceNumber[x],
    #              listOfDBWords[x], listOfInputSequenceEncodedWords[x], listOfTargetSequenceEncodedWords[x],
    #              listOfInputSequenceEncodedWordsInHexFormat[x], listOfTargetSequenceEncodedWordsInHexFormat[x]))
    #     else:
    #         isTrainingDataIsFinished = True
    #         if (requiredPercentageForValidation >= 0 or prevSentenceNumber == listOfDbSentenceNumber[x]) and\
    #                 (isValidationDataIsFinished is False):
    #             prevSentenceNumber = listOfDbSentenceNumber[x]
    #             requiredPercentageForValidation -= 1
    #             cur.execute(
    #                 "INSERT INTO ParsedDocument(DocName, UnDiacritizedCharacter,DiacritizedCharacter,LetterType,"
    #                 "SentenceNumber, "
    #                 "Word, "
    #                 "InputSequenceEncodedWords,TargetSequenceEncodedWords, InputSequenceEncodedWordsInHexFormat,"
    #                 "TargetSequenceEncodedWordsInHexFormat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    #                 (docName, unDiacritizedCharacter[x], diacritizedCharacter[x], 'validation', listOfDbSentenceNumber[x],
    #                 listOfDBWords[x], listOfInputSequenceEncodedWords[x], listOfTargetSequenceEncodedWords[x],
    #                 listOfInputSequenceEncodedWordsInHexFormat[x], listOfTargetSequenceEncodedWordsInHexFormat[x]))
    #
    #         else:
    #             isValidationDataIsFinished = True
    #             cur.execute(
    #                 "INSERT INTO ParsedDocument(DocName, UnDiacritizedCharacter,DiacritizedCharacter,LetterType,"
    #                 "SentenceNumber, "
    #                 "Word, "
    #                 "InputSequenceEncodedWords,TargetSequenceEncodedWords, InputSequenceEncodedWordsInHexFormat,"
    #                 "TargetSequenceEncodedWordsInHexFormat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    #                 (docName, unDiacritizedCharacter[x], diacritizedCharacter[x], 'testing',
    #                  listOfDbSentenceNumber[x],
    #                  listOfDBWords[x], listOfInputSequenceEncodedWords[x], listOfTargetSequenceEncodedWords[x],
    #                  listOfInputSequenceEncodedWordsInHexFormat[x], listOfTargetSequenceEncodedWordsInHexFormat[x]))
    #
    # for x in range(0, len(listOfWordsInSent)):
    #     cur.execute(
    #         "INSERT INTO ListOfWordsAndSentencesInEachDoc(word,SentenceNumber,DocName) VALUES (%s,%s,%s)",
    #         (listOfWordsInSent[x][0], listOfWordsInSent[x][1], docName))

    db.commit()
    db.close()

def resetAllLists():
    del unDiacritizedCharacter[:]
    del diacritizedCharacter[:]
    del listOfDbSentenceNumber[:]
    del listOfDBWords[:]
    del listOfInputSequenceEncodedWords[:]
    del listOfTargetSequenceEncodedWords[:]
    del listOfInputSequenceEncodedWordsInHexFormat[:]
    del listOfTargetSequenceEncodedWordsInHexFormat[:]
    del listOfWordsInSent[:]

if __name__ == "__main__":
    findFiles()
    declareGlobalVariables()
    for eachDoc in range(0, len(listOfFilesPathes)):
        readDoc(eachDoc)
        extractAndCleanWordsFromDoc()
        extractSentencesFromDoc()
        encodingDiacritizedCharacter()
        # encodingunDiacritizedCharacter()
        #  convertToString()
        extractEachCharacterFromWordWithItsDiacritization()
        connectToDB()
        pushDataIntoDB()
        resetAllLists()
