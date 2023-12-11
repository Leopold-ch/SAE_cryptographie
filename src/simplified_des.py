"""
Fichier d'un DES simplifier

Author: Joao H de A Franco (jhafranco@acm.org)

Description: Simplified DES implementation in Python 3

Date: 2012-02-10

License: Attribution-NonCommercial-ShareAlike 3.0 Unported
          (CC BY-NC-SA 3.0)
"""
from sys import exit
from time import time

KEY_LENGTH = 10
SUB_KEY_LENGTH = 8
DATA_LENGTH = 8
F_LENGTH = 4

# Tables for initial and final permutations (b1, b2, b3, ... b8)
IPtable = (2, 6, 3, 1, 4, 8, 5, 7)
FPtable = (4, 1, 3, 5, 7, 2, 8, 6)

# Tables for sub_key generation (k1, k2, k3, ... k10)
P10table = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8table = (6, 3, 7, 4, 8, 5, 10, 9)

# Tables for the feistel_function function
EPtable = (4, 1, 2, 3, 2, 3, 4, 1)
S0table = (1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2)
S1table = (0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3)
P4table = (2, 4, 3, 1)

def perm(input_byte, perm_table):
    """Permute input byte according to permutation table"""
    output_byte = 0
    for index, elem in enumerate(perm_table):
        if index >= elem:
            output_byte |= (input_byte & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            output_byte |= (input_byte & (128 >> (elem - 1))) << ((elem - 1) - index)
    return output_byte

def init_permutation(input_byte):
    """Perform the initial permutation on data"""
    return perm(input_byte, IPtable)

def final_permutation(input_byte):
    """Perform the final permutation on data"""
    return perm(input_byte, FPtable)

def swap_nibbles(input_byte):
    """Swap the two nibbles of data"""
    return (input_byte << 4 | input_byte >> 4) & 0xff

def key_gen(key):
    """Generate the two required subkeys"""
    def left_shift(key_bit_list):
        """Perform a circular left shift on the first and second five bits"""
        shifted_key = [None] * KEY_LENGTH
        shifted_key[0:9] = key_bit_list[1:10]
        shifted_key[4] = key_bit_list[0]
        shifted_key[9] = key_bit_list[5]
        return shifted_key

    # Converts input key (integer) into a list of binary digits
    key_list = [(key & 1 << i) >> i for i in reversed(range(KEY_LENGTH))]
    perm_key_list = [None] * KEY_LENGTH
    for index, elem in enumerate(P10table):
        perm_key_list[index] = key_list[elem - 1]
    shifted_once_key = left_shift(perm_key_list)
    shifted_twice_key = left_shift(left_shift(shifted_once_key))
    sub_key_1 = sub_key_2 = 0
    for index, elem in enumerate(P8table):
        sub_key_1 += (128 >> index) * shifted_once_key[elem - 1]
        sub_key_2 += (128 >> index) * shifted_twice_key[elem - 1]
    return (sub_key_1, sub_key_2)

def feistel_function(sub_key, input_data):
    """Apply Feistel function on data with given sub_key"""
    def sub_function(sub_key_2, right_nibble):
        aux = sub_key_2 ^ perm(swap_nibbles(right_nibble), EPtable)
        index1 = ((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                 ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
        index2 = ((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                 ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
        sbox_outputs = swap_nibbles((S0table[index1] << 2) + S1table[index2])
        return perm(sbox_outputs, P4table)

    left_nibble, right_nibble = input_data & 0xf0, input_data & 0x0f
    return (left_nibble ^ sub_function(sub_key, right_nibble)) | right_nibble

def encrypt(key, plaintext):
    """Encrypt plaintext with given key"""
    data = feistel_function(key_gen(key)[0], init_permutation(plaintext))
    return final_permutation(feistel_function(key_gen(key)[1], swap_nibbles(data)))

def decrypt(key, ciphertext):
    """Decrypt ciphertext with given key"""
    data = feistel_function(key_gen(key)[1], init_permutation(ciphertext))
    return final_permutation(feistel_function(key_gen(key)[0], swap_nibbles(data)))

if __name__ == '__main__':
    # Test vectors described in "Simplified DES (SDES)"
    # (http://www2.kinneret.ac.il/mjmay/ise328/328-Assignment1-SDES.pdf)

    try:
        assert encrypt(0b0000000000, 0b10101010) == 0b00010001
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b0000000000, 0b10101010), "Expected: ", 0b00010001)
        exit(1)
    try:
        assert encrypt(0b1110001110, 0b10101010) == 0b11001010
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1110001110, 0b10101010), "Expected: ", 0b11001010)
        exit(1)
    try:
        assert encrypt(0b1110001110, 0b01010101) == 0b01110000
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1110001110, 0b01010101), "Expected: ", 0b01110000)
        exit(1)
    try:
        assert encrypt(0b1111111111, 0b10101010) == 0b00000100
    except AssertionError:
        print("Error on encrypt:")
        print("Output: ", encrypt(0b1111111111, 0b10101010), "Expected: ", 0b00000100)
        exit(1)

    t1 = time()
    for i in range(1000):
        encrypt(0b1110001110, 0b10101010)
    t2 = time()
    print(f"Elapsed time for 1,000 encryptions: {t2-t1}s")
    exit()
