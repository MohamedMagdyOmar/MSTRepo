# -*- coding: utf-8 -*-
import csv
import MySQLdb
import MySQLdb.cursors
import glob
import ExcelFileProcessing


rnn_output_for_one_seq = []
neurons_locations_with_highest_output_for_a_seq = []
list_of_all_diacritized_letters = []
list_of_actual_letters = []
list_of_expected_letters = []
current_sentence = []

sentence_number = 0

path = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample'
extension = 'csv'

letters_of_fatha_correction = ['ة', 'ا', 'ى']


def connect_to_db():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="mstdb",  # name of the data base
                         cursorclass=MySQLdb.cursors.SSCursor,
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')
    global cur
    cur = db.cursor()


def get_sentence_from_db():
    connect_to_db()
    selected_sentence_query = "select Word from parseddocument where LetterType='testing' and SentenceNumber = " + \
                              str(sentence_number)

    cur.execute(selected_sentence_query)

    global current_sentence
    current_sentence = cur.fetchall()
    current_sentence = sorted(set(current_sentence), key=lambda x: current_sentence.index(x))


def read_csv_file(filename):
    path_of_file = 'D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\' + filename

    # with open('D:\CurrenntRepo\CurrenntVS\CURRENNT\ArabicDiacritizationExample\\1.csv', 'rb') as csvfile:

    with open(path_of_file, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        global rnn_output_for_one_seq
        rnn_output_for_one_seq = []
        for row in reader:
            rnn_output_for_one_seq.append(map(float, row))


def get_neurons_numbers_with_highest_output_value():
    global rnn_output_for_one_seq
    global neurons_locations_with_highest_output_for_a_seq
    neurons_locations_with_highest_output_for_a_seq = []
    for row in rnn_output_for_one_seq:
        neurons_locations_with_highest_output_for_a_seq.append(row.index(max(row)))


def get_actual_letters():
    global list_of_actual_letters
    list_of_actual_letters = []

    global neurons_locations_with_highest_output_for_a_seq
    for neuron_location in neurons_locations_with_highest_output_for_a_seq:
        list_of_actual_letters.append(list_of_all_diacritized_letters[neuron_location - 1])


def get_expected_letters():
    global sentence_number
    list_of_expected_diacritized_letters_query = "select DiacritizedCharacter from parseddocument where " \
                                                 "LetterType='testing' and SentenceNumber = " + str(sentence_number)

    cur.execute(list_of_expected_diacritized_letters_query)

    global list_of_expected_letters
    list_of_expected_letters = []
    list_of_expected_letters = cur.fetchall()


if __name__ == "__main__":
    connect_to_db()
    get_number_of_first_testing_sentence()
    result = [i for i in glob.glob('*.{}'.format(extension))]

    for file_name in result:
        connect_to_db()
        get_sentence_from_db()
        read_csv_file(file_name)
        get_neurons_numbers_with_highest_output_value()
        connect_to_db()
        get_actual_letters()
        get_expected_letters()
        sentence_number += 1