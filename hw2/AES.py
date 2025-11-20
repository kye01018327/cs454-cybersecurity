from utils import *

# Functions
def sub_bytes(input_block: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 matrix representing the state
    # Use the AES S-box to substitute each byte in the state
    transformed_block = []
    for row in input_block:
        output_row = []
        for word in row:
            # Use left and right bytes for selecting rows and columns
            left_byte = word >> 4
            right_byte = word & 0xf
            output_row.append(S_BOX[left_byte][right_byte])
        transformed_block.append(output_row)
    return transformed_block

def shift_rows(input_block: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 matrix state matrix as input
    transformed_block = []
    # Shift the rows as per AES specification
    # Leave the 1st row of State unaltered
    
    first_row = input_block[0]
    # Circular left shift 1 time for 2nd row
    second_row = input_block[1]
    second_row = second_row[1:] + second_row[:1]
    
    # Circular left shift 2 times for 3rd row
    third_row = input_block[2]
    third_row = third_row[2:] + third_row[:2]

    # Circular left shift 3 times for 4th row
    fourth_row = input_block[3]
    fourth_row = fourth_row[3:] + fourth_row[:3]

    # Construct transformed block
    transformed_block.append(first_row)
    transformed_block.append(second_row)
    transformed_block.append(third_row)
    transformed_block.append(fourth_row)

    return transformed_block



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

