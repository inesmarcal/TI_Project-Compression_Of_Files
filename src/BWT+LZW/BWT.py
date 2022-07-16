import matplotlib.image as mpimg
import pickle

'''
Exemplo:
    
    [1,2,3,4,5,6,7]
    
    [1,2,3,4,5,6,7]
    [7,1,2,3,4,5,6]
    [6,7,1,2,3,4,5]
    [5,6,7,1,2,3,4]
    [4,5,6,7,1,2,3]
    [3,4,5,6,7,1,2]
    [2,3,4,5,6,7,1]
    

    [1,2,3,4,5,6,7]
    [2,3,4,5,6,7,1]
    [3,4,5,6,7,1,2]
    [4,5,6,7,1,2,3]
    [5,6,7,1,2,3,4]
    [6,7,1,2,3,4,5]
    [7,1,2,3,4,5,6]

    
    [7,1,2,3,4,5,6]
    
'''


def bwt_encoder(bloco):
    lista = list()
    bloco = list(bloco)
    tam = len(bloco)
    for i in range(tam):
        new = bloco[-1:] + bloco[:-1]
        lista.append(new)
        bloco = new
    lista_st = list()
    for linha in lista:
        res = ""
        for i in range(len(linha)):
            res += "/" + str(linha[i])
        lista_st.append(res)
    lista_st = sorted(lista_st)

    lista = list()
    for linha in lista_st:
        s = ""
        l1 = linha[::-1]
        for c in l1:
            if (c != "/"):
                s += c
            else:
                break
        lista.append(int(s[::-1]))
    return lista


def bw(img):
    intervalo = 1024
    inicio = 0
    newimg = list()
    flag = 0
    while (flag == 0):
        if ((inicio + intervalo) < len(img)):
            bloco = img[inicio:inicio + intervalo]
            encoded = bwt_encoder(bloco)
            newimg.extend(encoded)
            inicio += intervalo
        else:
            bloco = img[inicio:len(img)]
            encoded = bwt_encoder(bloco)
            newimg.extend(encoded)
            inicio += intervalo
            flag = 1

    return newimg


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
    img = mpimg.imread(file)
    img = img.flatten()
    encodedBW = bw(img)

    byteEncoded = byteEncode(encodedBW)

    print('tamanho original: %d, tamanho após BWT: %d' % (len(img), len(byteEncoded)))

    nome = file.split('.')
    nomeFich = nome[0] + 'BWT.dat'
    write_file(nomeFich, byteEncoded)

    print("---------------------------------------------")


if __name__ == "__main__":
    file = "egg.bmp"
    leitura_img(file)

    file = "landscape.bmp"
    leitura_img(file)

    file = "pattern.bmp"
    leitura_img(file)

    file = "zebra.bmp"
    leitura_img(file)
