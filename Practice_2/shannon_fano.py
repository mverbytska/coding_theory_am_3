import json
import re


class ShannonFano:
    def __init__(self, letter_frequency_table):
        self.letter_frequency_table = letter_frequency_table
        # here the dictionary for every character and its frequency will be
        self.characters_codes = {}

    def build_shannon_tree(self, frequency_table, coded_line='', ):
        if len(frequency_table) == 1:
            key, value = frequency_table[0]
            # if we reached the leaf while traversing tree
            self.characters_codes[key] = coded_line
        elif len(frequency_table) > 1:
            left_minus_right = 1
            total = sum(frequency for char, frequency in frequency_table)
            partition = 1
            left_frequency = 0
            for i, (char, frequency) in enumerate(frequency_table):
                left_frequency += frequency
                right_frequency = total - left_frequency
                new_difference = abs(left_frequency - right_frequency)
                if new_difference < left_minus_right:
                    left_minus_right = new_difference
                    partition = i
            left_tree = frequency_table[:partition + 1]
            right_tree = frequency_table[partition + 1:]

            self.build_shannon_tree(left_tree, coded_line + '0')
            self.build_shannon_tree(right_tree, coded_line + '1')

        return self.characters_codes

    def encode(self, text):
        encoding = ''
        clean_text = ShannonFano.clean_input_text(text)
        # print(self.characters_codes)
        for char in clean_text:
            encoding += self.characters_codes.get(char.upper())
        return encoding

    @staticmethod
    def clean_input_text(raw_text):
        # this pattern will match all the characters, that are not alphabetical, spaces, dots or newline signs
        pattern = r'[^a-zA-Z \n\.]'
        cleaned = re.sub(pattern, '', raw_text)
        return cleaned

    def decode(self, encoded_info):
        decoded_info = ''
        current_code = ''

        # builds a sequence by adding 1 character from encoded string, until it matches the same pattern in
        # the dictionary in our ShannonFano class instance
        for c in encoded_info:
            current_code += c
            for char, char_code in self.characters_codes.items():
                if char_code == current_code:
                    decoded_info += char
                    current_code = ''
                    break

        return decoded_info

    @staticmethod
    def build_freq_dictionary(path_to_json_file):
        with open(path_to_json_file, 'r') as json_file:
            freq_table = json.load(json_file)
        frequencies_dict = [(char, freq) for char, freq in freq_table.items()]
        frequencies_dict.sort(key=lambda x: x[1], reverse=True)
        return frequencies_dict


if __name__ == "__main__":
    frequencies = ShannonFano.build_freq_dictionary('./letter_frequencies.json')
    sh = ShannonFano(frequencies)
    sh.characters_codes = sh.build_shannon_tree(frequencies)
    print(sh.characters_codes)
    with open('./text.txt', 'r') as text_file:
        text_to_encode = text_file.read()

    # encoding
    encoded_text = sh.encode(text_to_encode)
    with open('./output.txt', 'w') as output_file:
        output_file.write(encoded_text)
    print(encoded_text)

    # decoding
    with open('./output.txt', 'r') as decoded_file:
        text_to_decode = decoded_file.read()
    decoded_text = sh.decode(text_to_decode)
    with open('./decoded_output', 'w') as decoded_output_file:
        decoded_output_file.write(decoded_text)
