from utils import *

# Functions
def sub_bytes(input_block: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 matrix representing the state
    # Use the AES S-box to substitute each byte in the state
    output_block = []
    for row in input_block:
        output_row = []
        for word in row:
            # Use left and right bytes for selecting rows and columns
            left_byte = word >> 4
            right_byte = word & 0xf
            output_row.append(S_BOX[left_byte][right_byte])
        output_block.append(output_row)
    return output_block


def shift_rows():
    pass

def mix_columns():
    pass

def add_round_key():
    pass

def key_expansion():
    pass

def aes_encrypt():
    pass

def aes_test():
    pass

def demo_avalanche_effect():
    pass

def aes_decrypt():
    pass

