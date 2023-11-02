# calculate the number of redundant bits for this code
# formula: 2^r ≥ m + r + 1 where, r = redundant bit, m = data bit

def calculate_redundant(input_data):
    m = len(input_data)
    for r in range(m):
        if 2 ** r >= r + m + 1:
            return r


# determine the parity bits
def determine_red_b_positions(input_data, r):
    m = len(input_data)
    j = 0
    k = 1
    res = ''
    for i in range(1, r + m + 1):
        if i == 2 ** j:
            res = res + '0'
            j += 1
        else:
            res = res + input_data[-1 * k]  # since we are counting from the right side
            k += 1
    return res[::-1]


# calculate parity bits value for correct case
def calculate_parity_bits(red_b_positions, r):
    n = len(red_b_positions)
    for i in range(r):
        par_value = 0
        for j in range(1, n + 1):
            if j & 2 ** i == 2 ** i:
                par_value = par_value ^ int(red_b_positions[-1 * j])  # since we are counting from the right side
        red_b_positions = red_b_positions[:n - (2 ** i)] + str(par_value) + red_b_positions[n - (2 ** i) + 1:]
    return red_b_positions


# detect error
def detect_error(red_b_positions, r):
    n = len(red_b_positions)
    res = 0

    for i in range(r):
        parity_val = 0
        for j in range(1, n + 1):
            if j & 2 ** i == 2 ** i:
                parity_val = parity_val ^ int(red_b_positions[-1 * j])  # since we are counting from the right side

        res = res + parity_val * (10 ** i)
    left_side_position = n - int(str(res), 2)
    return left_side_position


def correct_error(red_b_positions, error_place):
    if error_place < len(red_b_positions):
        char_to_change = red_b_positions[error_place]
        if char_to_change == '0':
            red_b_positions = red_b_positions[:error_place] + '1' + red_b_positions[error_place + 1:]
        else:
            red_b_positions = red_b_positions[:error_place] + '0' + red_b_positions[error_place + 1:]
    return red_b_positions


data = '10011101110'
print(f'Input data: {data}')
m = len(data)
r = calculate_redundant(data)
print(f'Redundant bits number: {r}')
redundant_bits_positions = determine_red_b_positions(data, r)
redundant_bits_positions = calculate_parity_bits(redundant_bits_positions, r)
print(f'Data to be transmit: {redundant_bits_positions}')

# correct data to transmit: 100111001111010
# let's make a mistake on the third position from left: 101111001111010

redundant_bits_positions = '101111001111010'
print(f'Error data: {redundant_bits_positions}')
detected_error = detect_error(redundant_bits_positions, r)
print(f'Detected error place {detected_error + 1} from the left')
redundant_bits_positions = correct_error(redundant_bits_positions, detected_error)
print(f'Restored data: {redundant_bits_positions}')
