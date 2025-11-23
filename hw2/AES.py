from utils import S_BOX, M, printb, convert_int_to_matrix, convert_matrix_to_int


"""
AES functions
"""
# TODO: verify each function works

def sub_bytes(input_matrix: list[list[int]]) -> list[list[int]]:
    print('SUB BYTES')
    printb(input_matrix, 'INPUT')
    # Accept a 4 by 4 matrix representing the state
    # Use the AES S-box to substitute each byte in the state
    transformed_matrix = []
    for row in input_matrix:
        transformed_row = []
        for byte in row:
            # Use left and right nibbles for selecting rows and columns
            left_byte = byte >> 4
            right_byte = byte & 0xf
            transformed_row.append(S_BOX[left_byte][right_byte])
        transformed_matrix.append(transformed_row)
    printb(transformed_matrix, 'OUTPUT')
    return transformed_matrix


def shift_rows(input_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 state matrix as input
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

def multiply_by_2(byte: int) -> int:
        byte <<= 1
        if byte & 0x100:
            byte ^= 0x11b

        byte &= 0xff
        return byte


def multiply(factor: int, byte: int) -> int:
    if factor == 1:
        return byte

    if factor == 2:
        return multiply_by_2(byte)
    
    if factor == 3:
        return multiply_by_2(byte) ^ byte
    
    return 0


def mix_columns(input_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 state matrix as input
    # Multiply each column of the state by a fixed polynomial matrix in the Galois Field (GF(2^8))
    transformed_matrix = []
    for column in zip(*input_matrix):
        transformed_col = []
        for factors in M:
            transformed_byte = 0
            for factor, byte in zip(factors, column):
                transformed_byte ^= multiply(factor, byte)
            transformed_col.append(transformed_byte)
        transformed_matrix.append(transformed_col)

    # Transpose matrix to row form
    transformed_matrix = [list(row) for row in zip(*transformed_matrix)]
    return transformed_matrix
    

def add_round_key(input_matrix: list[list[int]], key_matrix: list[list[int]]) -> list[list[int]]:
    # Accept a 4 by 4 state matrix as input
    # Perform a bitwise XOR between the state and the round key.
    transformed_matrix = []
    for state_row, key_row in zip(input_matrix, key_matrix):
        transformed_row = []
        for state_byte, key_byte in zip(state_row, key_row):
            transformed_byte = state_byte ^ key_byte
            transformed_row.append(transformed_byte)
        transformed_matrix.append(transformed_row)
    return transformed_matrix


def key_expansion(key_matrix: list[list[int]]) -> list[list[int]]:
    # Copy original key into first 4 words of expanded key
    w = []
    for word in key_matrix:
        w.append(word)

    # Generate rcon
    rc = 0x01
    rcon = []
    for i in range(0, 10):
        rcon.append([rc, 0, 0, 0])
        rc <<= 1
        if rc & 0x100:
            rc ^= 0x11b

    # Generate next 40 words
    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            print("UNCHANGED")
            print(temp)
            temp = rot_word(temp)
            print("ROTWORD")
            print(temp)
            temp = sub_word(temp)
            print("SUBWORD")
            print(temp)
            temp = [a ^ b for a, b in zip(temp, rcon[i // 4 - 1])]
            print("XOR with rcon")
            print(temp)
        temp = [a ^ b for a, b in zip(w[i - 4], temp)]
        print("FINAL WORD")
        print(temp)
        w.append(temp)
    return w
    

def rot_word(input_word: list[int]) -> list[int]:
    # Circular left shift one time
    transformed_word = input_word[1:] + input_word[:1]
    return transformed_word


def sub_word(input_word: list[int]) -> list[int]:
    # Substitute each byte using S-Box
    transformed_word = []
    for byte in input_word:
        left_nibble = byte >> 4
        right_nibble = byte & 0xf
        transformed_word.append(S_BOX[left_nibble][right_nibble])
    return transformed_word


def aes_encrypt(plaintext_int: int, key_int: int) -> int:
    plaintext_matrix = convert_int_to_matrix(plaintext_int)
    key_matrix = convert_int_to_matrix(key_int)
    words = key_expansion(key_matrix)
    round_keys = []
    for i in range(11):
        key_words = words[i*4 : i*4 + 4]
        round_key_matrix = [list(row) for row in zip(*key_words)]
        round_keys.append(round_key_matrix)

    state_matrix = plaintext_matrix
    state_matrix = add_round_key(state_matrix, round_keys[0])

    for i in range(1, 10):
        state_matrix = sub_bytes(state_matrix)
        state_matrix = shift_rows(state_matrix)
        state_matrix = mix_columns(state_matrix)
        state_matrix = add_round_key(state_matrix, round_keys[i])

    state_matrix = sub_bytes(state_matrix)
    state_matrix = shift_rows(state_matrix)
    state_matrix = add_round_key(state_matrix, round_keys[10])

    return convert_matrix_to_int(state_matrix)


def aes_test():
    pass


def demo_avalanche_effect():
    pass


def aes_decrypt():
    pass

