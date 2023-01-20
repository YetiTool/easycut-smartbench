from escpos import *

def print_unlock_receipt(code):
    p = printer.Serial('COM2')
    p.text(str(code))



if __name__ == '__main__':
    code = sys.argv[1]

    print_unlock_receipt(code)