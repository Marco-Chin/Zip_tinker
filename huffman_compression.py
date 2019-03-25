import operator
import os
import time

INPUT_FILE = 'small_input.txt'
OUTPUT_FILE = 'output.txt'


class Node():
    def __init__(self,
                 label=None,
                 value=None,
                 left=None,
                 right=None,
                 parent=None):
        self.label = label
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.code = None


class HuffmanTree():
    def __init__(self, freq):
        self.freq = freq
        self.root = self.build_tree()
        self.assign_code(self.root, '', '')

    def build_tree(self):
        nodes = []

        for v in self.freq:
            nodes.append(Node(label=v[0], value=v[1]))

        root = None

        while True:
            # get 2 least frueqent nodes
            node1 = nodes.pop(0)
            node2 = nodes.pop(0)

            f1 = node1.value
            f2 = node2.value

            (node1, node2) = (node1, node2) if f1 <= f2 else (node2, node1)

            internal_node = Node(label='internal_node', value=(f1 + f2))
            root = internal_node

            internal_node.left = node1
            internal_node.right = node2

            node1.parent = internal_node
            node2.parent = internal_node

            root_node = internal_node

            # insert back into self.freq
            nodes.append(internal_node)
            nodes = sorted(nodes, key=lambda node: node.value)

            if len(nodes) == 1:
                break

        return root

    def assign_code(self, node, symbol, running_code):
        if node == None:
            return

        left_symbol = '0'
        right_symbol = '1'
        running_code += symbol

        self.assign_code(node.left, left_symbol, running_code)
        self.assign_code(node.right, right_symbol, running_code)

        node.code = running_code

    def get_encoded_alphabet(self):
        nodes = []
        node_stack = [self.root]

        while len(node_stack) != 0:
            current_node = node_stack.pop(0)

            if current_node.left != None:
                node_stack.append(current_node.left)

            if current_node.right != None:
                node_stack.append(current_node.right)

            nodes.append(current_node)
        self.encoded_alphabet = nodes

        alphabet_list = []

        for node in nodes:
            if node.label != 'internal_node':
                alphabet_list.append((node.label, node.code))

        self.encoded_alphabet = dict([])

        for item in alphabet_list:
            self.encoded_alphabet[item[0]] = item[1]

        return self.encoded_alphabet


class HuffmanCompressor():
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

        self.original_size = os.path.getsize(self.input_file)

        self.encoded_alphabet = self.encode_file_alphabet()

    def encode_file_alphabet(self):
        self.alphabet_frequenies = self.get_alphabet_frequencies()
        encoded_alphabet = self.assign_huffman_codes(self.alphabet_frequenies)

        return encoded_alphabet

    def get_alphabet_frequencies(self):
        """get freq of each symbol in file"""
        freq = dict({})
        self.total_char = 0

        with open(self.input_file, encoding='utf-8-sig') as ifile:
            while True:
                self.total_char += 1
                c = ifile.read(1)

                if not c:
                    break

                if c not in freq:
                    freq[c] = 1
                else:
                    freq[c] += 1
            ifile.close()

        freq = sorted(freq.items(), key=lambda x: x[1])

        return freq

    def assign_huffman_codes(self, freq):
        huffman_tree = HuffmanTree(freq)
        encoded_alphabet = huffman_tree.get_encoded_alphabet()

        return encoded_alphabet

    def quick_calc(self):
        original_cost = self.total_char * 8
        new_cost = self.get_cost()

        return original_cost / new_cost

    def get_cost(self):
        total_cost = 0

        for item in self.alphabet_frequenies:
            amount = item[1]
            l = len(self.encoded_alphabet[item[0]])
            cost = amount * l
            total_cost += cost

        return total_cost

    def write_encoded_file(self):
        with open(self.input_file, encoding='utf-8-sig') as ifile:
            while True:
                c = ifile.read(1)

                if not c:
                    break
                with open(self.output_file, 'w') as ofile:
                    ofile.write(self.encoded_alphabet[c])
        print("DONE WRITING")


def main():
    hc = HuffmanCompressor(INPUT_FILE, OUTPUT_FILE)
    breakpoint()
    # hc.write_encoded_file()
    print(hc.quick_calc())


if __name__ == "__main__":
    main()
