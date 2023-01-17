from escpos.printer import Usb

# this logic being in the source means anyone could release unlock codes?


def print_unlock_receipt(unlock_code):
    try:
        p = Usb(0x0416, 0x5011)
        p.text("\n\n\n")
        p.image("Yeti logo.png")
        p.set("CENTER", "A", "normal", 2, 2, True, False)
        p.text("\n\n\nPrecisionPro +")
        p.set("CENTER", "A", "B", 2, 2, True, False)
        p.text("\nUnlock Code:\n\n")
        p.set("CENTER", "A", "B", 2, 2, True, True)
        p.text(" " + str(unlock_code) + " " + "\n\n\n")
        p.image("do not discard.png")
        p.text("\n\n\n\n")
        p.close()
        print("Printing complete")
    except:
        print("Failed to print")
