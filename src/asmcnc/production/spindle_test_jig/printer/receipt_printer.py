from escpos import printer
import sys


def print_unlock_receipt(code):
    p = printer.Usb(0x0416, 0x5011)
    p.text(str(code))


if __name__ == '__main__':
    code = sys.argv[1]

    print_unlock_receipt(code)