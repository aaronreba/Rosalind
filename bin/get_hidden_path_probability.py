#! pyenv/bin/python

import sys
import re

# test data file: data/hidden_path_probability.txt
# call like:
# ./bin/get_hidden_path_probability.py data/hidden_path_probability.txt

class HiddenPathProbabilityFile:
    def __init__(self, file_object):
        self.observed_path = file_object.readline().strip()

        file_object.readline() # skip

        states = file_object.readline().strip()
        states = re.sub(' +', ' ', states).split(' ')
        self.observed_states = states # don't need right now, but store it anyway

        file_object.readline() # skip

        self.hidden_path = file_object.readline().strip()

        file_object.readline() # skip

        states = file_object.readline().strip()
        states = re.sub(' +', ' ', states).split(' ')
        self.hidden_states = states # don't need right now, but store it anyway

        file_object.readline() # skip

        transition_states = file_object.readline().strip()
        transition_states = re.sub('^ +', '', transition_states)
        transition_states = re.sub(' +', ' ', transition_states).split(' ')
        self.transition_states = transition_states

        # self.observable_map is in the format of:
        # self.observable_map[hidden_state] = {
        #   hidden_state_1: {observed_state_1: observed_probability_1, ...}
        #   hidden_state_2: {observed_state_1: observed_probability_1, ...}
        # }
        self.observable_map = {}

        for line in file_object:
            line = line.strip()
            line = re.sub(' +', ' ', line)
            split_line = line.split(' ')
            self.observable_map[split_line[0]] = {}
            for i, probability in enumerate(split_line[1:]):
                self.observable_map[split_line[0]][self.transition_states[i]] = float(probability)

    def get_path_probability(self):
        probability = self.observable_map[self.hidden_path[0]][self.observed_path[0]]

        for hidden_state, observed_state in zip(self.hidden_path[1:], self.observed_path[1:]):
            probability *= self.observable_map[hidden_state][observed_state]

        return probability

def main(args):
    file_name = args
    with open(file_name, 'r') as f:
        ppf = HiddenPathProbabilityFile(f)

    print(ppf.get_path_probability())

if __name__ == '__main__':
    main(sys.argv[1])
