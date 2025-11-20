from utils import S_BOX, M


"""
AES functions
"""


def sub_bytes(input_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 matrix representing the state
    # Use the AES S-box to substitute each byte in the state
    transformed_matrix = []
    for row in input_matrix:
        transformed_row = []
        for word in row:
            # Use left and right bytes for selecting rows and columns
            left_byte = word >> 4
            right_byte = word & 0xf
            transformed_row.append(S_BOX[left_byte][right_byte])
        transformed_matrix.append(transformed_row)
    return transformed_matrix


def shift_rows(input_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 matrix state matrix as input
    transformed_matrix = []
    # Shift the rows as per AES specification
    # Leave the 1st row of State unaltered
    
    first_row = input_matrix[0]
    # Circular left shift 1 time for 2nd row
    second_row = input_matrix[1]
    second_row = second_row[1:] + second_row[:1]
    
    # Circular left shift 2 times for 3rd row
    third_row = input_matrix[2]
    third_row = third_row[2:] + third_row[:2]

    # Circular left shift 3 times for 4th row
    fourth_row = input_matrix[3]
    fourth_row = fourth_row[3:] + fourth_row[:3]

    # Construct transformed block
    transformed_matrix.append(first_row)
    transformed_matrix.append(second_row)
    transformed_matrix.append(third_row)
    transformed_matrix.append(fourth_row)

    return transformed_matrix

def mix_columns(input_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 state matrix as input
    # Multiply each column of the state by a fixed polynomial matrix in the Galois Field (GF(2^8))
    for column in zip(*input_matrix):
        pass
    

def add_round_key(input_matrix: list[list[int]], key_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 state matrix as input
    # Perform a bitwise XOR between the state and the round key.
    transformed_matrix = []
    for state_row, key_row in zip(input_matrix, key_matrix):
        transformed_row = []
        for state_word, key_word in zip(state_row, key_row):
            transformed_word = state_word ^ key_word
            transformed_row.append(transformed_word)
        transformed_matrix.append(transformed_row)
    return transformed_matrix



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

