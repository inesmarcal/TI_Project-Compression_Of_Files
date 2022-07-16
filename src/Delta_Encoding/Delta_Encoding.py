import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt


def histograma(fonte, alfabeto):
    # Vai receber uma fonte de informação com um alfabeto e mostra o histograma de ocorrência dos seus símbolos
    ocorrencia = ocorrencias(fonte, alfabeto)

    plt.xlabel("Alfabeto")
    plt.ylabel("Número de Ocorrências")
    plt.bar(alfabeto, ocorrencia.values(),color='skyblue')  # Mostra o histograma -> no eixo dos Xx os símbolos do alfabeto e no eixo dos Yy o número de ocorrências destes na fonte
    plt.show()

def ocorrencias(fonte, alfabeto):
    ocorrencias = dict()
    for alf in alfabeto:
        ocorrencias.update({alf: 0})
    for i in fonte:
        if (i in ocorrencias.keys()):
            ocorrencias[i] += 1
    return ocorrencias


def entropia(fonte, alfabeto):
    ocorrencia = ocorrencias(fonte, alfabeto)
    prob = probabilidade(ocorrencia)
    entr = np.sum(prob * np.log2(1 / prob))

    return entr


def taxa(entr):
    tax = ((8 - entr) / 8) * 100
    return tax


def probabilidade(ocorrencias):
    valores = np.array(list(ocorrencias.values()))
    valores = valores[valores > 0]

    no_total = np.sum(valores)

    prob = valores / no_total
    return prob


def delta_encode(img, tam):
    last = 0
    for i in range(tam):
        current = img[i]
        img[i] = current - last
        last = current
    return img


def deltaDecode(buffer):
    delta = 0
    for i in range(len(buffer)):
        buffer[i] += delta
        delta = buffer[i]

    return buffer


def leitura_img(file):
    print(file)
    plt.title(file)
    img = mpimg.imread(file)
    img = img.flatten()

    histograma(img, alfa_img_som())
    entrPre = entropia(img, alfa_img_som())
    taxPre = taxa(entrPre)
    print("Entropia pré DELTA: ", entrPre)
    print("Potencial de Compressão Entrópica pré DELTA: ", taxPre)

    imgDelta = delta_encode(img, len(img))

    histograma(imgDelta, alfa_img_som())
    entrPos = entropia(imgDelta, alfa_img_som())
    taxPos = taxa(entrPos)
    print("Entropia após DELTA: ", entrPos)
    print("Potencial de Compressão Entrópica após DELTA: ", taxPos)

    print('tamanho original: %d, tamanho após Delta: %d' % (len(img), len(imgDelta)))

    print("---------------------------------------------")


def alfa_img_som():
    alfabeto = np.arange(0, 256)
    return alfabeto


if __name__ == "__main__":
    file = "egg.bmp"
    leitura_img(file)

