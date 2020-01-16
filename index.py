# generates ngrams file in ./output/ngrams.csv
from nltk import word_tokenize
from collections import Counter
from nltk.util import ngrams
import itertools
from nltk import ngrams
import sys
import nltk
import csv
backoff = 0


def get_probs_from_csv(filepath):
    all_probs = ''
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        probs = list(csv_reader)
    return probs


def get_data_list(filepath, case_sensitive=False):
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        songs = []
        for row in csv_reader:
            if not case_sensitive:
                songs.append(row[1].lower())
            else:
                songs.append(row[1])
            line_count += 1
    return songs


def get_data_string(filepath, date='all', case_sensitive=False, backwards = False):
    all_songs = ''
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        songs = []
        if date == 'all':
            for row in csv_reader:
                song = row[1]
                if backwards:
                    song = song[::-1]
                if not case_sensitive:
                    songs.append(song.lower().replace('0', ''))
                else:
                    songs.append(song)
                line_count += 1
        else:
            for row in csv_reader:
                if date in row[0]:
                    songs.append(row[1])
                line_count += 1
        all_songs = ('/').join(songs)
    return all_songs


def token(x):
    return nltk.word_tokenize(x)


def nc(string, n):
    return Counter(ngrams(token(string), n))


def ncounts(string, n):
    return Counter(ngrams(token(" ".join(string)), n))


def get_ngrams(filepath, n, backwards=False):
    songs_string = get_data_string(filepath,backwards = backwards)
    return ncounts(songs_string, n)


def findlast(haystack, needle):
    parts = haystack.split(needle)
    return parts[-1]


def save_to_file(data_dict, filepath, n, name='probabilities'):
    with open("./output/probabilities.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in data_dict.items():
            songs_string = get_data_string(filepath)
            row = []
            concat = ''
            for item in key:
                row.append(item)
                concat = concat + item
            row.append(concat)
            for item in value:
                row.append(item)
            writer.writerow(row)


def get_probs(filepath, nrange, backwards=False,):
    metaresult = {}
    nlist = []
    for i in range(nrange[0], nrange[1]):
        nlist.append(i)
    for n in nlist:
        nGrams = get_ngrams(filepath, n, backwards = backwards)
        result_with_slashes = {}
        if n == 1:
            prior = sum(nGrams.values())
            for gram in nGrams:
                key = gram[0:n - 1]
                probability = float(nGrams[gram]) / float(prior)
                result_with_slashes[gram] = (probability, nGrams[gram])
        else:
            nMinusOne = get_ngrams(filepath, n - 1)
            for gram in nGrams:
                key = gram[0:n - 1]
                prior = nMinusOne[key]
                probability = float(nGrams[gram]) / float(prior)
                result_with_slashes[gram] = (probability, nGrams[gram])
        result = {}
        for key, value in result_with_slashes.items():
            if '/' not in key:
                result[key] = value
        save_to_file(result, filepath, n)
        metaresult[n] = result
    return metaresult


def get_probs_from_string(string, nrange):
    metaresult = {}
    nlist = []
    for i in range(nrange[0], nrange[1]):
        nlist.append(i)
    for n in nlist:
        nGrams = ncounts(string, n)
        nMinusOne = ncounts(string, n - 1)
    for n in nlist:
        nGrams = get_ngrams(filepath, n)
        nMinusOne = get_ngrams(filepath, n - 1)
        result_with_slashes = {}
        for gram in nGrams:
            key = gram[0:n - 1]
            prior = nMinusOne[key]
            probability = float(nGrams[gram]) / float(prior)
            result_with_slashes[gram] = (probability, nGrams[gram])
        result = {}
        for key, value in result_with_slashes.items():
            if '/' not in key:
                result[key] = value
        metaresult[n] = result
    return metaresult


def get_probs_from_string(string, nrange):
    metaresult = {}
    nlist = []
    for i in range(nrange[0], nrange[1]):
        nlist.append(i)
    for n in nlist:
        nGrams = ncounts(string, n)
        nMinusOne = ncounts(string, n - 1)
        result_with_slashes = {}
        for gram in nGrams:
            key = gram[0:n - 1]
            prior = nMinusOne[key]
            probability = float(nGrams[gram]) / float(prior)
            result_with_slashes[gram] = (probability, nGrams[gram])
        result = {}
        for key, value in result_with_slashes.items():
            if '/' not in key:
                result[key] = value
        metaresult[n] = result
    return metaresult

    '''test_ngrams=n_grams(test_string,n)
    test_result={}
    for gram in test_ngrams:
        if gram in result:
            test_result[gram]=result[gram]
        else:
            test_result[gram]='not_found
    return result

class Parser:

    n_ranges = {}

    def __init__(self,filepath):
        self.filepath=filepath

    def getProbs(self, nrange):
        print(filepath)

        result = get_probs(filepath,nrange)

        n_ranges[nrange] = result'''
