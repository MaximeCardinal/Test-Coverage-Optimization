import itertools
from multiprocessing.process import current_process
import sys
import os
import json
import multiprocessing
import subprocess


file_name = ""

    # Get user input for inputs preferences
def parseArrayInput(string_input):
    string_list = list(string_input.split(','))
    return string_list

    
def coverage(index, file_name, combinations):
    process1 = "coverage run --parallel-mode --context={1} {0} ".format(file_name, index) + ' '.join(j for j in combinations[index])
    subprocess.run(process1)
    # subprocess.run("coverage json --context={0} -o {0}.json".format(index))
    return

def reportJSON(index):
    subprocess.run("coverage json --context={0} -o {0}.json".format(index))
    return

def findNextBest(current_misses, list_dict):
    next_best_index = -1
    next_best_hits = []
    for i in range(len(list_dict)):
        curr_hits = list_dict[i]["files"][file_name]["executed_lines"]
        matches = set(current_misses)&set(curr_hits)
        if(len(matches) > len(next_best_hits)):
            next_best_hits = matches
            next_best_index = i
    return (next_best_index, next_best_hits)


if __name__ == '__main__':
    # Global variables
    default_input = ["prog.py", "test.py", "1,0", "0,1"]
    directory = "json_files"
    inputs = sys.argv if (default_input == None) else default_input

    file_name = sys.argv[1] if (default_input == None) else default_input[1]

    args = []
    combinations = []

    # Define list of inputs to test for path coverage
    # Here, only simple data types were tested. A wider listing of data types would be required for this program 
    # to be of use to a program using more complex data types (arrays of strings, arrays of integers, etc.)

    string_inputs_def = ["", "a", "abc def", " abc def", "abcdefghijklmnopqrstuvwxyz"]
    integer_inputs_def = [-sys.maxsize * 2, -1000, -100, -10, -1, 0, 1, 10, 100, 1000, sys.maxsize * 2 + 1]
    float_inputs_def = [float('-inf'), -1000.0, -100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0, 1000.0, float('inf')]
    boolean_inputs_def = [0, 1]

    integer_inputs_def = [str(i) for i in integer_inputs_def]
    float_inputs_def = [str(i) for i in float_inputs_def]
    boolean_inputs_def = [str(i) for i in boolean_inputs_def]

    for i in range(2, len(inputs)):
        input_type = inputs[i]
        if (input_type == "string"):
            args.append(string_inputs_def)
        elif (input_type == "integer"):
            args.append(integer_inputs_def)
        elif (input_type == "float"):
            args.append(float_inputs_def)
        elif (input_type == "boolean"):
            args.append(boolean_inputs_def)
        else:
            args.append(parseArrayInput(inputs[i]))


    # Produce the combinations of all the different arguments
    combinations = list(itertools.product(*args))
    combinations = [list(x) for x in combinations]

    # Create file 'combinations.txt' with one combination per line
    with open('combinations.txt', 'w') as f:
        for sub_lst in combinations:
            line = ','.join(str(e) for e in sub_lst)
            f.write("%s\n" % line)

    # Launch parallelization
    threads = []
    for i in range(len(combinations)):
        p = multiprocessing.Process(target=coverage, args=(i, file_name, combinations,))
        threads.append(p)
        p.start()

    for p in threads:
        p.join()

    subprocess.run("coverage combine")

    threads = []
    for i in range(len(combinations)):
        p = multiprocessing.Process(target=reportJSON, args=(i,))
        threads.append(p)
        p.start()

    for p in threads:
        p.join()

    # fetch all coverage results
    lst_coverage = ['{0}.json'.format(i) for i in range(len(combinations))]

    # load all json files to dictionaries
    lst_dict = []
    for cov in lst_coverage:
        json_name = cov
        with open(json_name) as f:
            cov_dict = json.load(f)
            lst_dict.append(cov_dict)

    for i in range(len(combinations)):
        os.remove('{0}.json'.format(i))
    os.remove('.coverage')

    # Get best code coverage
    i = 0
    biggest_cov = [None, None, [], []] # percentage, index, missing lines
    for cov in lst_dict:
        if ((biggest_cov[0] == None and biggest_cov[1] == None) or (cov["totals"]["percent_covered"] > biggest_cov[0])):
            biggest_cov[0] = cov["totals"]["percent_covered"]
            biggest_cov[1] = i
            biggest_cov[2] = cov["files"][file_name]["missing_lines"]
            biggest_cov[3] = cov["files"][file_name]["executed_lines"] 
        i = i + 1

    # Optimize test suite
    best_test_suite_indexes = []
    best_test_suite_indexes.append(biggest_cov[1])

    previous_coverage = 0.0
    current_coverage = biggest_cov[0]
    current_misses = biggest_cov[2]
    current_hits = biggest_cov[3]

    while ((current_coverage < 98.0) and (current_coverage - previous_coverage > 1.0)):

        # nextBest: [index, new_hits]
        nextBest = findNextBest(current_misses, lst_dict)

        # update variables
        best_test_suite_indexes.append(nextBest[0])
        current_hits.extend(nextBest[1])
        current_misses = list(set(current_misses) - set(nextBest[1]))
        previous_coverage = current_coverage
        current_coverage = len(current_hits) / (len(current_hits) + len(current_misses))
        

    # Print test suite
    test_suite = []
    for x in best_test_suite_indexes:
        test_suite.append(combinations[x])
    
    current_hits.sort()
    current_misses.sort()

    f = open("report.txt", "w")
    f.write("""
        Test Suite Coverage Optimization
        -----------------------------------

        Code coverage: {0}
        With inputs: {1}\n
        Total lines covered: {2}
        Lines covered: {3}\n
        Total lines missed: {4}
        Lines missing: {5}\n
    """.format(len(current_hits)/len(current_hits+current_misses), test_suite, len(current_hits), current_hits, len(current_misses), current_misses))
    f.close()