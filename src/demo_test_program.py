import sys
import math

def test():
    if (len(sys.argv) != 4):
        print("Wrong number of arguments.")
        return 

    number1 = float(sys.argv[1])
    number2 = float(sys.argv[2])
    number3 = number1 + 100
    arg4 = sys.argv[3]

    biggest = 0

    if (number1 >= number2):
        biggest = number1 
    elif number3 > number1 and number3 > number1:
        myStr = "I AM THE" 
        myStr = myStr + "BIGGEST"
        for i in range(100000):
            myStr = myStr + "i"
    elif number3 < number1 and number3 < number1:
        myStr = "I AM THE" + arg4
        myStr = myStr + "SMALLEST"
        for i in range(100000):
            myStr = myStr + "i"
    elif number1 > number2 and number1 > number3:
        result = math.pi * math.ceil(897468156) + math.comb(50,5) + math.acos(0.5)
        result = result + math.pi**2**2 - math.atan2(0.015, .99)
        result = abs(result)
        result = math.sqrt(result) / (result % 9999999)
        for i in range(1000):
            result = result + 1
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