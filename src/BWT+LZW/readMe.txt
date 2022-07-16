Para implementar este algoritmo, ou seja, aplicar a Transformada de Burrows-Wheeler (BWT) associado ao LZW em fontes de informação, basta ter os ficheiros que se pretendem transformar no mesmo diretório do código Python e colocar na main deste o nome de cada ficheiro a seguir ao "file = " que lá consta. Após isto, o ficheiro relativo à BWT vai gerar um outro ficheiro que terá de estar no mesmo diretório da pasta .idea referente ao LZW para se aplicar este algoritmo.

Como geralmente as fontes de informação a comprimir são demasiado grandes para os recursos de hardware e software que possuímos, temos de aplicar a Transformada BW por partes. No código fornecido, está-se a efetuar a implemetação da BWT em blocos de 1024. Porém, esse número pode ser alterado. Basta modificar na função bw do ficheiro .py onde está "intervalo = 1024" para um valor que se adeque ao contexto.

No final, o ficheiro terá um nome do tipo "nome do original.lzw"
