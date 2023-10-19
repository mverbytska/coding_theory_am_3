def encode(message, probabilities_dict):
    lower_bound, upper_bound = 0, 1
    for symbol in message:
        symbol_prob = probabilities_dict[symbol]
        range_size = upper_bound - lower_bound
        upper_bound = lower_bound + range_size * symbol_prob[1]
        lower_bound = lower_bound + range_size * symbol_prob[0]
    return lower_bound, upper_bound


def decode(encoded_value, probabilities_dict, message_length):
    message = []
    lower_bound, upper_bound = 0, 1

    for _ in range(message_length):
        for symbol, symbol_probability in probabilities_dict.items():
            range_size = upper_bound - lower_bound
            if symbol_probability[0] <= (encoded_value - lower_bound) / range_size < symbol_probability[1]:
                message.append(symbol)
                upper_bound = lower_bound + range_size * symbol_probability[1]
                lower_bound = lower_bound + range_size * symbol_probability[0]
                break

    return ''.join(message)


message_to_encode = "ABACABAB"
# length of the message = 8
# P(A) = 4/8 = 0.5
# P(B) = 3/8 = 0.375
# P(C) = 1/8 = 0.125

probabilities = {'A': (0, 0.5), 'B': (0.5, 0.875), 'C': (0.875, 1.0)}


encoded_low, encoded_high = encode(message_to_encode, probabilities)
decoded_message = decode(encoded_low, probabilities, len(message_to_encode))

print(f'Original Message: {message_to_encode}')
print(f'Coding interval: ({encoded_low}, {encoded_high})')
print(f'Encoded Value: {encoded_low}')
print(f'Decoded Message: {decoded_message}')
