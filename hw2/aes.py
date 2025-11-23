from utils import S_BOX, M, printb, convert_int_to_matrix, convert_matrix_to_int


"""
AES functions
"""
# TODO: verify each function works

def sub_bytes(input_matrix: list[list[int]]) -> list[list[int]]:
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

    # Transpose
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


def key_expansion(key_matrix: list[list[int]]) -> list[list[list[int]]]:
    # Create key words matrix as the tranpose of key matrix
    key_words = [list(row) for row in zip(*key_matrix)]

    # w[0..3] as keywords
    w = [word for word in key_words]

    # Generate rcon
    rc = 0x01
    rcon = []
    for i in range(0, 10):
        rcon.append([rc, 0, 0, 0])
        rc <<= 1
        if rc & 0x100:
            rc ^= 0x11b

    # Auxiliary Function
    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp = [a ^ b for a, b in zip(temp, rcon[i // 4 - 1])]
        w.append([a ^ b for a, b in zip(w[i - 4], temp)])

    # Convert to list of 4x4 column major keys
    keys = []
    for i in range(0, 11):
        key = []
        for j in range(0, 4):
            key.append(w[i*4 + j])
        key = [list(word) for word in zip(*key)]
        keys.append(key)
    return keys


def aes_encrypt(plaintext: int, key: int) -> int:
    # Initialize state and initial key
    state = convert_int_to_matrix(plaintext)
    init_key = convert_int_to_matrix(key)
    # Generate key schedule
    keys = key_expansion(init_key)
    # Add round key
    state = add_round_key(state, keys[0])
    # 9 rounds of SubBytes, ShiftRows, MixColumns, AddRoundKey
    for round_key in keys[1:10]:
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_key)
    # 10th round without MixColumns
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, keys[10])
    # Convert state to integer form
    state = convert_matrix_to_int(state)
    return state


def demo_avalanche_effect(plaintext: int, key: int):
    # Change a single bit in the plaintext while keeping the key constant
    # Flip right most bit
    modified_plaintext = plaintext ^ 0x01000000000000000000000000000000
    # Initialize state and initial key
    original_state = convert_int_to_matrix(plaintext)
    modified_state = convert_int_to_matrix(modified_plaintext)
    init_key = convert_int_to_matrix(key)
    # Generate key schedule
    keys = key_expansion(init_key)
    # Add round key
    original_state = add_round_key(original_state, keys[0])
    modified_state = add_round_key(modified_state, keys[0])
    print('BEFORE ROUNDS ---------------------------------------')
    printb(original_state, 'ORIGINAL STATE')
    printb(modified_state, 'MODIFIED STATE')
    num_bits_different(original_state, modified_state)

    # 9 rounds of SubBytes, ShiftRows, MixColumns, AddRoundKey
    for i, round_key in enumerate(keys[1:10]):
        original_state = sub_bytes(original_state)
        original_state = shift_rows(original_state)
        original_state = mix_columns(original_state)
        original_state = add_round_key(original_state, round_key)

        modified_state = sub_bytes(modified_state)
        modified_state = shift_rows(modified_state)
        modified_state = mix_columns(modified_state)
        modified_state = add_round_key(modified_state, round_key)
        print(f'ROUND {i + 1} ---------------------------------------')
        printb(original_state, 'ORIGINAL STATE')
        printb(modified_state, 'MODIFIED STATE')
        num_bits_different(original_state, modified_state)
    # 10th round without MixColumns
    original_state = sub_bytes(original_state)
    original_state = shift_rows(original_state)
    original_state = add_round_key(original_state, round_key)

    modified_state = sub_bytes(modified_state)
    modified_state = shift_rows(modified_state)
    modified_state = add_round_key(modified_state, round_key)
    print(f'ROUND 10 ---------------------------------------')
    printb(original_state, 'ORIGINAL STATE')
    printb(modified_state, 'MODIFIED STATE')
    num_bits_different(original_state, modified_state)
    

def num_bits_different(original_state: list[list[int]], modified_state: list[list[int]]):
    different_bits = 0
    for original_word, modified_word in zip(original_state, modified_state):
        for a, b in zip(original_word, modified_word):
            # Comparison bit by bit
            for _ in range(0,8):
                if a & 0x1 != b & 0x1:
                    different_bits += 1
                a >>= 1
                b >>= 1
    print(f'Number of bits different: {different_bits}')
    print()

    


def aes_decrypt():
    pass

