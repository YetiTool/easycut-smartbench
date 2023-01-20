from escpos.printer import Usb
import sys


def print_unlock_receipt(code):
    p = Usb(0x0416, 0x5011)
    p.text("Precision Pro+ Activation Code\n")
