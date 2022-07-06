class BuscadorDeInformacoes:

    def __init__(self, root, endereco_fixo):
        self.__root = root
        self.__endereco_fixo = endereco_fixo

    def busca_informacao(self, nome_tag, numero_elemento):
        for element in self.__root.iter(self.__endereco_fixo + nome_tag):
            atributo = element[numero_elemento]
            return atributo.text

    def busca_informacao_mais_precisa(self, nome_tag, numero_elemento_1, numero_elemento_2):
        for element in self.__root.iter(self.__endereco_fixo + nome_tag):
            atributo = element[numero_elemento_1]
            data = atributo[numero_elemento_2].text
            return data

