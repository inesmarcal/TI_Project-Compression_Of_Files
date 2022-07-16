import matplotlib.image as mpimg
import huffmancodec
import pickle

def huffmanEncode(data, table):
    encoded_data = bytearray()

    buffer = 0
    size = 0
    for s in data:
        b, v = table[s]
        buffer = (buffer << b) + v
        size += b

        while size >= 8:
            byte = buffer >> (size - 8)
            encoded_data.append(byte)
            buffer = buffer - (byte << (size - 8))
            size -= 8
    if size > 0:
        byte = buffer << (8 - size)
        encoded_data.append(byte)

    return encoded_data


# escreve bytrarray para ficheiro
def write_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        f.close()


def leitura_img(file):
    print(file)
    img = mpimg.imread(file)
    img = img.flatten()

    img = list(img) + [256]

    codec = huffmancodec.HuffmanCodec.from_data(img)
    table = codec.get_code_table()

    imgHuffman = huffmanEncode(img, table)
    nome = file.split('.')
    nomeFich = nome[0] + 'HUFFMAN.dat'

    encoded = {'t': table, 'd': imgHuffman}

    write_file(nomeFich, encoded)

    print('tamanho original: %d, tamanho após Huffman: %d' % (len(img), len(imgHuffman)))

    print("---------------------------------------------")


if __name__ == "__main__":
    file = "egg.bmp"
    leitura_img(file)

