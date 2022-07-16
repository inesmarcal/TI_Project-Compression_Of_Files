import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pickle


def delta_encode(img, tam):
    last = 0
    for i in range(tam):
        current = img[i]
        img[i] = current - last
        last = current
    return img


def write_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        f.close()


def byteEncode(data):
    encoded_data = bytearray()

    buffer = 0
    size = 0
    for s in data:
        b = 8
        buffer = (buffer << b) + s
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


def leitura_img(file):
    print(file)
    plt.title(file)
    img = mpimg.imread(file)
    img = img.flatten()
    encodedDelta = delta_encode(img, len(img))
    byteEncoded = byteEncode(encodedDelta)

    print('tamanho original: %d, tamanho após DELTA: %d' % (len(img), len(byteEncoded)))

    nome = file.split('.')
    nomeFich = nome[0] + 'DELTA.dat'
    write_file(nomeFich, byteEncoded)

    print("---------------------------------------------")


if __name__ == "__main__":
    file = "egg.bmp"
    leitura_img(file)

