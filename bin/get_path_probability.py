#! pyenv/bin/python

import sys
import re

# test data file: data/path_probability.txt
# call like:
# ./bin/get_path_probability.py data/path_probability.txt

class PathProbabilityFile:
    def __init__(self, file_object):
        self.path = file_object.readline().strip()

        file_object.readline() # skip

        states = file_object.readline().strip()
        states = re.sub(' +', ' ', states).split(' ')
        self.states = states # don't need right now, but store it anyway

        file_object.readline() # skip

        transition_states = file_object.readline().strip()
        transition_states = re.sub('^ +', '', transition_states)
        transition_states = re.sub(' +', ' ', transition_states).split(' ')
        self.transition_states = transition_states

        # self.transition_map is in the format of:
        # self.transition_map['A'] = {'A': 0.1, 'B': 0.9}
        # self.transition_map['B'] = {'A': 0.2, 'B': 0.8}
        self.transition_map = {}

        for line in file_object:
            line = line.strip()
            line = re.sub(' +', ' ', line)
            split_line = line.split(' ')
            self.transition_map[split_line[0]] = {}
            for i, probability in enumerate(split_line[1:]):
                self.transition_map[split_line[0]][self.transition_states[i]] = float(probability)

    def get_path_probability(self):
        previous_character = self.path[0]
        next_character = self.path[1]
        probability = 0.5 * self.transition_map[previous_character][next_character]

        previous_character = self.path[1]
        for c in self.path[2:]:
            next_character = c
            probability *= self.transition_map[previous_character][next_character]
            previous_character = next_character

        return probability

def main(args):
    file_name = args
    with open(file_name, 'r') as f:
        ppf = PathProbabilityFile(f)

    print(ppf.get_path_probability())

if __name__ == '__main__':
    main(sys.argv[1])
