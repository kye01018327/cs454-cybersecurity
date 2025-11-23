from AES import *
from utils import *


def test_int_to_matrix():
    input = 0x00112233445566778899aabbccddeeff
    output = [
        [0x00, 0x44, 0x88, 0xcc],
        [0x11, 0x55, 0x99, 0xdd],
        [0x22, 0x66, 0xaa, 0xee],
        [0x33, 0x77, 0xbb, 0xff],
    ]
    assert convert_int_to_matrix(input) == output
    assert convert_matrix_to_int(output) == input


def test_sub_bytes():
    input = convert_int_to_matrix(0x19a09ae93df4c6f8e3e28d48be2b2a08)
    expected_result = 0xd4e0b81e27bfb44111985d52aef1e530
    assert convert_matrix_to_int(sub_bytes(input)) == expected_result


def test_shift_rows():
    input = convert_int_to_matrix(0xd4e0b81e27bfb44111985d52aef1e530)
    expected_result = 0xd4bf5d30e0b452aeb84111f11e2798e5
    assert convert_matrix_to_int(shift_rows(input)) == expected_result
