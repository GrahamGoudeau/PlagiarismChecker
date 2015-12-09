from __future__ import print_function
import sys
import argparse
import itertools

default_tuple_size = 3

# holds the root word, as well as all synonyms of that word
class Word:
    def __init__(self, root_word, synonym_map):
        self.root_word = root_word
        self.synonyms = [root_word] + synonym_map.get(root_word, [])

# separate the text into tuples of Words, which contain the root word
# as well as the list of its synonyms for easy access
def tuple_separate(file_name, tuple_size, synonym_map):
    tuples = []
    try:
        with open(file_name, 'r') as file:
            text = file.read()
            text = text.strip()
            split_text = text.split()
            split_len = len(split_text)
            if tuple_size >= split_len:
                print('Warning - tuple size equals or exceeds text length in \'{}\''
                    .format(file_name), file=sys.stderr)

                # return a single tuple which has the same length as the text
                return [[Word(word, synonym_map) for word in split_text]]

            # get every grouping of tuple_size from the text
            for index in range(len(split_text)):
                new_tuple = []
                for q in range(tuple_size):
                    if index + q >= split_len: break
                    new_tuple.append(Word(split_text[index + q], synonym_map))

                # if at the end of the string, some new_tuples will have less
                # than tuple_size elements; if that is the case, don't append
                if len(new_tuple) == tuple_size:
                    tuples.append(new_tuple)

        return tuples

    except IOError:
        print('Problem opening file \'{}\''.format(file_name), file=sys.stderr)
        sys.exit(1)

def build_synonyms(file_name):
    synonym_map = {}
    try:
        with open(file_name, 'r') as open_file:
            synonym_lines = [line for line in open_file]
            for synonym_set in synonym_lines:
                synonym_set = synonym_set.strip()
                current_synonyms = synonym_set.split(' ')

                for word in current_synonyms:
                    # add all synonyms to the dict that are not the current word
                    synonym_map[word] = [w for w in current_synonyms\
                                        if w != word]
    except IOError:
        print('Problem opening \'{}\''.format(file_name), file=sys.stderr)
        sys.exit(1)

    return synonym_map

# given lists of tuples of Words, find the percentage of tuples1 appear in
# tuples2, based on the contents of synonym_map
def determine_plagiarize(tuples1, tuples2, synonym_map):
    num_duplicates = 0
    tuple_length = len(tuples1)

    # list of all the tuples holding root words from tuples2
    original_tuple2 = [[word.root_word for word in sub_tuple] for sub_tuple in tuples2]

    for tuple in tuples1:
        # base case - original tuple in tuples2
        if tuple in tuples2:
            num_duplicates += 1
            continue

        # find all possible variants of the current tuple in tuples1,
        # based on the synonyms; find the Cartesian product of all the words
        # of the text and their synonyms
        all_possible_tuples = [list(group) for group in itertools.product(
                                        *([word.synonyms for word in tuple]))]

        # get a count of all the duplicates
        num_duplicates += len([duplicate for duplicate in all_possible_tuples\
                                if duplicate in original_tuple2])

    return float(num_duplicates) / float(tuple_length)

def parse_args():
    parser = argparse.ArgumentParser(description='Plagiarism checker')
    parser.add_argument('synonym_file',
        help='the file containing synonym associations')
    parser.add_argument('input_1', help='the first input text')
    parser.add_argument('input_2', help='the second input text')
    parser.add_argument('-N', type=int, default=3,
        help='set the sizes of tuples to be compared (must be positive)')

    args = parser.parse_args()
    if args.N < 1:
        parser.print_help()
        sys.exit(1)

    return args

def main():
    args = parse_args()

    synonym_file = args.synonym_file
    input_1 = args.input_1
    input_2 = args.input_2
    tuple_size = args.N

    synonym_map = build_synonyms(synonym_file)
    plagiarize_percent = determine_plagiarize(tuple_separate(input_1, tuple_size, synonym_map),
                                              tuple_separate(input_2, tuple_size, synonym_map),
                                              synonym_map)

    percent_string = str(int(plagiarize_percent * 100)) + '%'

    print(percent_string)

if __name__ == '__main__':
    main()
