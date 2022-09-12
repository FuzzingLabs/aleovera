#!/usr/bin/env python3.9
from aleovera.disassembler import aleodisassembler
from random import randbytes
import random


def get_random_unicode(length):

    try:
        get_char = chr
    except NameError:
        get_char = chr

    # Update this to include code point ranges to be sampled
    include_ranges = [
        (0x0021, 0x0021),
        (0x0023, 0x0026),
        (0x0028, 0x007E),
        (0x00A1, 0x00AC),
        (0x00AE, 0x00FF),
        (0x0100, 0x017F),
        (0x0180, 0x024F),
        (0x2C60, 0x2C7F),
        (0x16A0, 0x16F0),
        (0x0370, 0x0377),
        (0x037A, 0x037E),
        (0x0384, 0x038A),
        (0x038C, 0x038C),
    ]

    alphabet = [
        get_char(code_point)
        for current_range in include_ranges
        for code_point in range(current_range[0], current_range[1] + 1)
    ]
    return bytes(
        "".join(random.choice(alphabet) for i in range(length)), "utf-8"
    )
\xc2\xb4\xe2\xb1\xba\xe2\xb

def fuzz():
    while True:
        # random_bytes = randbytes(200)
        random_bytes = get_random_unicode(200)
        print("-------------BYTES-----------")
        print(random_bytes)
        print("-------------RESULT------------")
        aleo = aleodisassembler(random_bytes)
        try:
            aleo.disassemble()
        except SystemExit:
            pass


fuzz()
