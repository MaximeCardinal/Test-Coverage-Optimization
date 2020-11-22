import sys

def test():
    if (len(sys.argv) != 3):
        print("Wrong number of arguments.")
        return 

    number1 = float(sys.argv[1])
    number2 = float(sys.argv[2])

    if (number1 >= number2):
        biggest = number1 
    else:
        biggest = number2
        biggest = biggest + 1
        biggest = biggest + 1
        biggest = biggest + 1
        biggest = biggest + 1
        biggest = biggest + 1
        biggest = biggest + 1

    return biggest

if __name__ == "__main__":
    test()