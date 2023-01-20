#!/usr/bin/python
from escpos.printer import Usb
import sys


def print_unlock_receipt(unlock_code):
    try:
        # Establish connection with printer
        p = Usb(0x0416, 0x5011)
        # Add spacing for stapling
        p.text("\n\n\n")
        # Print top logo
        p.image("asmcnc/production/spindle_test_jig/printer/img/logo.png")
        # Print "PrecisionPro + Unlock code"
        p.set("CENTER", "A", "normal", 2, 2, True, False)
        p.text("\n\n\nPrecisionPro +")
        p.set("CENTER", "A", "B", 2, 2, True, False)
        p.text("\nUnlock Code:\n\n")
        # Print Unlock code
        p.set("CENTER", "A", "B", 2, 2, True, True)
        p.text(" " + str(unlock_code) + " " + "\n\n\n")
        # Print do not descard warning
        p.image("asmcnc/production/spindle_test_jig/printer/img/do_not_discard.png")
        p.text("\n\n\n\n")
        # Close connection with printer
        p.close()
        print("Printing complete")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    code = sys.argv[1]

    print_unlock_receipt(code)