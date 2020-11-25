import sys
import math

def biggest(number1, number2):
    biggest = 0

    if (number1 >= number2):
        biggest = number1
    else:
        biggest = number2

    return biggest

if __name__ == "__main__":

    if (len(sys.argv) != 3):
        print("Wrong number of arguments.")
    else: 
        number1 = float(sys.argv[1])
        number2 = float(sys.argv[2])    

        biggest = biggest(number1, number2)
    