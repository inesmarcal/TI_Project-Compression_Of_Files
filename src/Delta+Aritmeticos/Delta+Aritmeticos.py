import contextlib, sys
import arithmeticcoding
import matplotlib.image as mpimg
import pickle


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


def delta_encode(img, tam):
    last = 0
    for i in range(tam):
        current = img[i]
        img[i] = current - last
        last = current
    return img


# Command line main application function.
def main(inputfile, outputfile):
    freqs = get_frequencies(inputfile)
    freqs.increment(256)  # EOF symbol gets a frequency of 1

    # Read input file again, compress with arithmetic coding, and write output file
    with open(inputfile, "rb") as inp, \
            contextlib.closing(arithmeticcoding.BitOutputStream(open(outputfile, "wb"))) as bitout:
        write_frequencies(bitout, freqs)
        compress(freqs, inp, bitout)


# Returns a frequency table based on the bytes in the given file.
# Also contains an extra entry for symbol 256, whose frequency is set to 0.
def get_frequencies(filepath):
    freqs = arithmeticcoding.SimpleFrequencyTable([0] * 257)
    with open(filepath, "rb") as input:
        while True:
            b = input.read(1)
            if len(b) == 0:
                break
            freqs.increment(b[0])
    return freqs


def write_frequencies(bitout, freqs):
    for i in range(256):
        write_int(bitout, 32, freqs.get(i))


def compress(freqs, inp, bitout):
    enc = arithmeticcoding.ArithmeticEncoder(32, bitout)
    while True:
        symbol = inp.read(1)
        if len(symbol) == 0:
            break
        enc.write(freqs, symbol[0])
    enc.write(freqs, 256)  # EOF
    enc.finish()  # Flush remaining code bits


# Writes an unsigned integer of the given bit width to the given stream.
def write_int(bitout, numbits, value):
    for i in reversed(range(numbits)):
        bitout.write((value >> i) & 1)  # Big endian


def write_file(filename, data):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
        f.close()


# Main launcher
if __name__ == "__main__":
    nome = "egg.bmp"
    print(nome)
    img3 = mpimg.imread(nome)
    img3 = img3.flatten()
    inputfile3 = delta_encode(img3, len(img3))
    inputfile3 = byteEncode(inputfile3)
    nome_in = nome.split(".")
    aux = nome_in[0]+"aux_DELTA+ARITMETICO.dat"
    write_file(aux, inputfile3)
    final = nome_in[0]+"DELTA+ARITMETICO.dat"
    main(aux, final)
    print("------------------------")
