import xml.etree.ElementTree as ET
import NotaFiscal as nf
import pandas as pd
import os
from BuscadorDeInformacoes import BuscadorDeInformacoes
from datetime import datetime
from validate_docbr import CPF
from validate_docbr import CNPJ
import xlsxwriter


def criaBordero():
    caminho = input("Insira o diretório das notas: ")
    # Lista que será usada pra criar o DataFrame
    lista_dicionario_completo = []

    for arquivo in os.listdir(caminho):
        tree = ET.parse(caminho + arquivo)
        root = tree.getroot()
        endereco = "{http://www.portalfiscal.inf.br/nfe}"

        buscador = BuscadorDeInformacoes(root, endereco)

        # Busca os valores no xml
        numero_da_nota = int(buscador.busca_informacao("ide", 5))
        nome_da_empresa = buscador.busca_informacao("dest", 1)
        cnpj_da_empresa = buscador.busca_informacao("dest", 0)
        data_emissao_da_nota = buscador.busca_informacao("ide", 6)
        valor_da_nota = float(buscador.busca_informacao("fat", 3))

        # Formata as variáveis para criar a nota_fiscal.
        cnpj_ou_cpf_formatado = valida(cnpj_da_empresa)
        data_emissao_sem_horas = str.split(data_emissao_da_nota, "T")
        data_emissao_formatada = formataData(data_emissao_sem_horas[0])
        data_vencimento_1_formatada = validaEhFormataDataVencimento1(buscador)
        data_vencimento_2_formatada = validaEhFormataDataVencimento2(buscador)
        data_vencimento_1_formatada = verifiaSeEhAvista(data_emissao_formatada, data_vencimento_1_formatada)

        # Cria a nota_fiscal
        nota_fiscal = nf.NotaFiscal(nome_da_empresa,
                                    numero_da_nota,
                                    cnpj_ou_cpf_formatado,
                                    data_emissao_formatada,
                                    data_vencimento_1_formatada,
                                    data_vencimento_2_formatada)
        if nota_fiscal.get_data_vencimento_1() == 'A VISTA' or verficaSeVaiParaFactoring(cnpj_ou_cpf_formatado):
            nota_fiscal.set_valor_a_vista(valor_da_nota)
        else:
            nota_fiscal.set_valor_factoring(valor_da_nota)

        # Preenche a lista_dicionario com cada nota_fiscal da pasta.
        lista_dicionario_completo.append(criaListaCompleta(nota_fiscal))

    dataframe1 = criaDataFrame_completo(lista_dicionario_completo)
    lista_dicionario_factoring = criaListaDicionarioParaFactoring(lista_dicionario_completo)
    dataframe2 = criaDataFrame_completo(lista_dicionario_factoring)
    try:
        criaPlanilhaExcel(dataframe1, dataframe2)
    except Exception as e:
        print("Parece que ocorreu algum erro!")
        print(e)
        input("Aperte Enter para encerrar!")


def verifiaSeEhAvista(data_emissao, data_vencimento):
    if data_emissao == data_vencimento:
        data_vencimento_1_formatada = 'A VISTA'
        return data_vencimento_1_formatada
    else:
        return data_vencimento


def formataData(data_string):
    data = datetime.strptime(data_string, "%Y-%m-%d")
    data_formatada = datetime.strftime(data, "%d/%m/%Y")
    return data_formatada


def valida(cnpj_ou_cpf):
    cnpj = CNPJ()
    cpf = CPF()
    cnpj_da_empresa_formatado = ''
    if cnpj.validate(cnpj_ou_cpf):
        cnpj_ou_cpf = cnpj.mask(cnpj_ou_cpf)
        return cnpj_ou_cpf

    else:
        cnpj_ou_cpf = cpf.mask(cnpj_ou_cpf)
        return cnpj_ou_cpf


def criaListaCompleta(nota_fiscal):
    lista_nota_completa = [nota_fiscal.get_nome_da_empresa(),
                           nota_fiscal.get_numero_da_nota(),
                           nota_fiscal.get_cnjp_da_empresa(),
                           nota_fiscal.get_data_emissao(),
                           nota_fiscal.get_data_vencimento_1(),
                           nota_fiscal.get_data_vencimento_2(),
                           nota_fiscal.get_valor_factoring(),
                           nota_fiscal.get_valor_a_vista()]
    return lista_nota_completa


def criaDataFrame_completo(lista_dicionario):
    data_frame = pd.DataFrame(lista_dicionario, index=None, columns=['CLIENTE',
                                                                     'NF',
                                                                     'CNPJ',
                                                                     'EMISSÃO',
                                                                     'VENC(1)',
                                                                     'VENC(2)',
                                                                     'FACTORING',
                                                                     'A VISTA'])
    return data_frame


def criaPlanilhaExcel(dataframe_1, dataframe_2):
    writer = pd.ExcelWriter('bordero.xlsx', engine='xlsxwriter')
    dataframe_1.to_excel(writer, sheet_name='Valores Completos')
    dataframe_2.to_excel(writer, sheet_name='Valores para Factoring')
    writer.save()
    print('Bordero Concluído')
    input("Aperte Enter para encerrar!")


def validaEhFormataDataVencimento1(buscador):
    try:
        data_de_vencimento_1_da_nota = buscador.busca_informacao_mais_precisa("cobr", 1, 1)
        data_vencimento_1_formatada = formataData(data_de_vencimento_1_da_nota)
        return data_vencimento_1_formatada
    except IndexError:
        data_vencimento_1_formatada = 'N/A'
        return data_vencimento_1_formatada


def validaEhFormataDataVencimento2(buscador):
    try:
        data_de_vencimento_2_da_nota = buscador.busca_informacao_mais_precisa("cobr", 2, 1)
        data_vencimento_2_formatada = formataData(data_de_vencimento_2_da_nota)
        return data_vencimento_2_formatada
    except IndexError:
        data_vencimento_2_formatada = 'N/A'
        return data_vencimento_2_formatada


def criaListaDicionarioParaFactoring(lista_dicionario):
    for lista in lista_dicionario:
        if lista[4] == 'A VISTA':
            lista_dicionario.remove(lista)
    return lista_dicionario


def verficaSeVaiParaFactoring(cnpj):
    lista_cnpj = ['11.627.933/0002-00', '28.453.688/0002-65', '61.479.002/0001-08']

    if cnpj in lista_cnpj:
        return True
    else:
        return False


if __name__ == "__main__":
    criaBordero()
