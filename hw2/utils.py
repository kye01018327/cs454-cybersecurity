# Functions
def printb(block: list[list[int]]) -> None:
    for row in block:
        print("[", end="")
        for byte in row:
            print(hex(byte), end=" ")
        print("]")
    print()


def convert_int_to_block(input: int) -> list: 
    total_bytes = 16 
    block = []
    for i in range(4):
        row = []
        for j in range(4):
            byte_index = total_bytes - 1 - (i * 4 + j)
            shift_amount = byte_index * 8
            byte = (input >> shift_amount) & 0xff
            row.append(byte)
        block.append(row)
    return block

def convert_block_to_int(block: list[list[int]]) -> int:
    total_bytes = 16 
    output_int = 0
    for i in range(4):
        for j in range(4):
            byte = block[i][j]
            byte_index = total_bytes - 1 - (i * 4 + j)
            shift_amount = byte_index * 8
            output_int |= (byte << shift_amount)
    return output_int