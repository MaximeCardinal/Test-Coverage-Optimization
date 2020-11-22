import itertools
import multiprocessing
import sys
import os
import json
import multiprocessing
import subprocess
import time

# Modify the following line to preset the command line arguments
default_input = ["prog.py", "default_test_program.py", "float", "float"]

# Modify the following parameters to tune the optimization
coverage_optimization_threshold = 98.0
coverage_optimization_min_improvement = 1.0
nbr_threads = 1 # bounded by the number of cores

file_name = ""
string_inputs_def = []
integer_inputs_def = []
float_inputs_def = []
boolean_inputs_def = []

def generateStringInputsDef():
    generated = []
    # Could be greatly improved to cover more cases
    generated = ["", "a", "abc def", " abc def", "abcdefghijklmnopqrstuvwxyz"]

    return generated
    
def generateIntegerInputsDef():
    generated = []
    # Could be greatly improved to cover more cases
    generated = [-sys.maxsize * 2, -100000, -10000, -1000, -100, -10, -1, 0, 1, 10, 100, 1000, 10000, 100000, sys.maxsize * 2 + 1]

    generated = [str(i) for i in generated]
    return generated

def generateFloatInputsDef():
    generated = []
    # Could be greatly improved to cover more cases
    generated = [float('-inf'), -100000.0, -1000.0, -100.0, -10.0, -1.0, 0.0, 1.0, 10.0, 100.0, 1000.0, 100000.0, float('inf')]

    generated = [str(i) for i in generated]
    return generated

def generateBooleanInputsDef():
    generated = []
    # Could be greatly improved to cover more cases
    generated = [0, 1]

    generated = [str(i) for i in generated]
    return generated

    # Parse a comma separated list to a Python list (array)
def parseArrayInput(string_input):
    string_list = list(string_input.split(','))
    return string_list

    # Run the coverage run command (from coverage.py)
def coverage(index, file_name, combinations, threadIndex):
    while(threadIndex[index] < len(combinations)):
        # print(threadIndex[index])
        process1 = "coverage run --parallel-mode --context={1} {0} ".format(file_name, index) + ' '.join(j for j in combinations[threadIndex[index]])
        subprocess.run(process1)
        threadIndex[index] = threadIndex[index] + nbr_threads
    return

    # Run the coverage json command (from coverage.py)
def reportJSON(index, combinations, threadIndex):
    while(threadIndex[index] < len(combinations)):
        subprocess.run("coverage json --context={0} -o {0}.json".format(threadIndex[index]))
        threadIndex[index] = threadIndex[index] + nbr_threads
    return

    # Find the next test set that adds the most executed lines to a test suite 
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

    # Print a report of the coverage optimization in report.txt
def printReport(coverage, test_suite, hits, hit_lines, misses, missed_lines):
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
    """.format(coverage, test_suite, hits, hit_lines, misses, missed_lines))
    f.close()
    return


if __name__ == '__main__':

    # Use default input if no command line arguments were provided
    # TODO: Check for command line args, if none then use default
    inputs = sys.argv if (default_input == None) else default_input
    file_name = sys.argv[1] if (default_input == None) else default_input[1]

    args = []
    combinations = []

    string_inputs_def = generateStringInputsDef()
    integer_inputs_def = generateIntegerInputsDef()
    float_inputs_def = generateFloatInputsDef()
    boolean_inputs_def = generateBooleanInputsDef()

    # iterate through the set of inputs and add them to the list of arguments (all their possible values are stored here)
    for i in range(2, len(inputs)):
        input_type = inputs[i]
        print(input_type)
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

    # Produce the combinations of all the different arguments (ex: [[1,0],[0,1]] -> [[1,0], [1,1], [0,0], [0,1]])
    combinations = list(itertools.product(*args))
    combinations = [list(x) for x in combinations]

    start_time = time.time()
    # Parallelization: Run the coverage of the input program with all the test combinations
    threads = []
    threadIndex = []
    for i in range(nbr_threads):
        threadIndex.append(i)
        p = multiprocessing.Process(target=coverage, args=(i, file_name, combinations, threadIndex,))
        threads.append(p)
        p.start()

    # Wait for all threads to complete their task
    for p in threads:
        p.join()

    # Combine all the coverage analysis produced by the threads
    subprocess.run("coverage combine")

    # Parallelization: Produce the reports of the coverage
    threads = []
    threadIndex = []
    for i in range(nbr_threads):
        threadIndex.append(i)
        p = multiprocessing.Process(target=reportJSON, args=(i, combinations, threadIndex,))
        threads.append(p)
        p.start()

    # Wait for all threads to complete their task
    for p in threads:
        p.join()
    print("--- %s seconds ---" % (time.time() - start_time))
    print(len(combinations))

    #Ffetch all coverage results
    lst_coverage = ['{0}.json'.format(i) for i in range(len(combinations))]

    # Load all JSON files to dictionaries
    lst_dict = []
    for cov in lst_coverage:
        json_name = cov
        with open(json_name) as f:
            cov_dict = json.load(f)
            lst_dict.append(cov_dict)

    # Delete the report files
    for i in range(len(combinations)):
        os.remove('{0}.json'.format(i))
    os.remove('.coverage')

    # Get best code coverage's test combination
    i = 0
    biggest_cov = [None, None, [], []] # biggest_cov = [percentage, index, missing_lines, hit_lines]
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

    while ((current_coverage < coverage_optimization_threshold) and (current_coverage - previous_coverage > coverage_optimization_min_improvement)):

        # nextBest: [index, new_hits]
        nextBest = findNextBest(current_misses, lst_dict)

        # update variables
        best_test_suite_indexes.append(nextBest[0])
        current_hits.extend(nextBest[1])
        current_misses = list(set(current_misses) - set(nextBest[1]))
        previous_coverage = current_coverage
        current_coverage = len(current_hits) / (len(current_hits) + len(current_misses))
        

    # Format results
    test_suite = []
    for x in best_test_suite_indexes:
        test_suite.append(combinations[x])
    
    current_hits.sort()
    current_misses.sort()

    # Print report
    printReport(len(current_hits)/len(current_hits+current_misses), test_suite, len(current_hits), current_hits, len(current_misses), current_misses)