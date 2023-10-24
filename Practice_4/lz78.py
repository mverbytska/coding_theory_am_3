def encode(message):
    sequences_dict = {}
    # list of tuples with encodings
    encoded_list = []
    current_match = ''
    next_code = 1

    for char in message:
        current_match += char
        if current_match not in sequences_dict:
            sequences_dict[current_match] = next_code
            encoded_list.append((sequences_dict.get(current_match[:-1], 0), char))
            next_code += 1
            current_match = ''

    if current_match:
        encoded_list.append((sequences_dict[current_match], ''))
    return encoded_list


def decode(encoded_data):
    sequence_dict = {}
    decoded_message = ''
    next_code = 1
    for code, char in encoded_data:
        if code == 0:
            decoded_message += char
            sequence_dict[next_code] = char
            next_code += 1
        else:
            entry = sequence_dict[code]
            sequence_dict[next_code] = entry + char
            decoded_message += entry + char
            next_code += 1

    return decoded_message


message_to_encode = 'ABABACABC'
print(f'Original message: {message_to_encode}')
encoded = encode(message_to_encode)
print(f'Encoded: {encoded}')
decoded = decode(encoded)
print(f'Decoded: {decoded}')
