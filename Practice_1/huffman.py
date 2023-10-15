import json
import re


class HuffmanCode:
    class Node:
        def __init__(self, left_child=None, right_child=None):
            self.left_child = left_child
            self.right_child = right_child

        def children(self):
            return self.left_child, self.right_child

    def __init__(self, letter_frequency_table):
        self.letter_frequency_table = letter_frequency_table
        self.character_codes = {}

    @staticmethod
    def make_heap(nodes):
        while len(nodes) > 1:
            (char_1, freq_1) = nodes[-1]
            (char_2, freq_2) = nodes[-2]
            nodes = nodes[:-2]
            new_node = HuffmanCode.Node(char_1, char_2)
            nodes.append((new_node, freq_1 + freq_2))
            nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        return nodes[0][0]

    def build_huffman_tree(self, node, coded_string=''):
        if type(node) is str:
            return {node: coded_string}
        (left, right) = node.children()
        self.character_codes.update(self.build_huffman_tree(left, coded_string + '0'))
        self.character_codes.update(self.build_huffman_tree(right, coded_string + '1'))
        return self.character_codes

    def encode(self, text):
        encoded_string = ''
        clean_text = HuffmanCode.clean_input_text(text)
        for char in clean_text:
            encoded_string += self.character_codes.get(char.upper())
        return encoded_string

    def decode(self, encoded_info):
        decoded_info = ''
        current_char_code = ''
        for c in encoded_info:
            current_char_code += c
            for char, char_code in self.character_codes.items():
                if char_code == current_char_code:
                    decoded_info += char
                    current_char_code = ''
                    break
        return decoded_info

    @staticmethod
    def clean_input_text(raw_text):
        # this pattern will match all the characters, that are not alphabetical, spaces, dots or newline signs
        pattern = r'[^a-zA-Z \n\.]'
        cleaned = re.sub(pattern, '', raw_text)
        return cleaned

    @staticmethod
    def build_freq_dictionary(path_to_json_file):
        with open(path_to_json_file, 'r') as json_file:
            freq_table = json.load(json_file)
        frequencies_dict = [(char, freq) for char, freq in freq_table.items()]
        frequencies_dict.sort(key=lambda x: x[1], reverse=True)
        return frequencies_dict


if __name__ == '__main__':
    frequencies = HuffmanCode.build_freq_dictionary('./letter_frequencies.json')
    huffman = HuffmanCode(frequencies)
    root = huffman.make_heap(frequencies)
    chars_encodings = huffman.build_huffman_tree(root)
    print(chars_encodings)

    # encode text file
    with open('./text.txt', 'r') as text_file:
        text_to_encode = text_file.read()

    encoded_text = huffman.encode(text_to_encode)
    with open('./output_file.txt', 'w') as output_file:
        output_file.write(encoded_text)

    print(encoded_text)

    # decode text file
    with open('./output_file.txt', 'r') as encoded_output_file:
        text_to_decode = encoded_output_file.read()
    decoded_text = huffman.decode(text_to_decode)
    with open('./decoded_output.txt', 'w') as decoded_output_file:
        decoded_output_file.write(decoded_text)
