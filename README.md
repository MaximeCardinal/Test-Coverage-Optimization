# Test-Coverage-Optimization

Final project ECSE-420 Fall2020

Group Members:
    * Alexa Normandin   [GitHub](https://github.com/alexnorms)
    * Alexis Franche    [GitHub](https://github.com/alexisfranche)
    * Maxime Cardinal   [GitHub](https://github.com/MaximeCardinal)
    * Oliver Murphy     [GitHub](https://github.com/OliverMurphy)

## Project Description:

test_coverage_optimization.py is a python program that can be used to quickly generate a list of inputs for a python program that achieves maximal test coverage.

## Dependencies

Coverage.py (Ver. 5.3) [Link](https://coverage.readthedocs.io/en/coverage-5.3/)

## Arguments

python test_coverage_optimization.py *path_to_program* *arg1* *arg2* *arg3* *...*

*path_to_program* : Path to python program on which the optimization will be performed

*arg1*,*arg2*,*arg3*,*...*: List of the types of arguments of the program on which the optimization will be performed. Possible values are: string, integer, float, boolean. It is also possible to specify a specific list of inputs rather than its type for an argument. The format is a comma separated list of the possible inputs. Ex:  "3,4,5".

### Examples

Python program: "/MyFolder/program.py"
Inputs: "string" "integer" "boolean"

Example 1 (default inputs):

    python test_coverage_optimization.py /MyFolder/program.py string integer boolean

Example 2 (personalized inputs): 

    python test_coverage_optimization.py /MyFolder/program.py string 0,1,2 true