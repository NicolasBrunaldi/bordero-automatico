class NotaFiscal:

    def __init__(self, nome_da_empresa, numero_da_nota, cnpj_da_empresa, data_emissao, data_vencimento_1,
                 data_Vencimento_2):
        self.__nome_da_empresa = nome_da_empresa
        self.__numero_da_nota = numero_da_nota
        self.__cnpj_da_empresa = cnpj_da_empresa
        self.__data_emissao = data_emissao
        self.__data_vencimento_1 = data_vencimento_1
        self.__data_vencimento_2 = data_Vencimento_2
        self.__valor_factoring = ''
        self.__valor_a_vista = ''

    def __str__(self):
        return "Nome: {}, Nota: {}, CNPJ: {}, Data de Emissão: {}, Data de Vencimento: {}, Valor da Nota: {}".format(
            self.__nome_da_empresa,
            self.__numero_da_nota,
            self.__cnpj_da_empresa,
            self.__data_emissao,
            self.__data_vencimento_1,
            self.__data_vencimento_2,
            self.__valor_factoring,
            self.__valor_a_vista)

    def get_nome_da_empresa(self):
        return self.__nome_da_empresa

    def get_numero_da_nota(self):
        return self.__numero_da_nota

    def get_cnjp_da_empresa(self):
        return self.__cnpj_da_empresa

    def get_data_emissao(self):
        return self.__data_emissao

    def get_data_vencimento_1(self):
        return self.__data_vencimento_1

    def get_data_vencimento_2(self):
        return self.__data_vencimento_2

    def get_valor_factoring(self):
        return self.__valor_factoring

    def get_valor_a_vista(self):
        return self.__valor_a_vista

    def set_valor_factoring(self, valor):
        self.__valor_factoring = valor

    def set_valor_a_vista(self, valor):
        self.__valor_a_vista = valor
