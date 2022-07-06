import main

def iniciar():
    print("****************************")
    print('BEM VINDO AO BORDERÔ AUTOMÁTICO')
    print("****************************")
    print('\n')
    print("Selecione uma das opções abaixo" "\n 1-Criar borderô" "\n 2-Ajuda" "\n 3-Sair")
    print('\n')

    opcao = input('digite a opção desejada:')
    print('\n')

    counter = True
    while counter:
        try:
            opcao = int(opcao)
        except ValueError:
            print("Insira apenas números")

            print("Selecione uma das opções abaixo" "\n 1-Criar borderô" "\n 2-Ajuda" "\n 3-Sair")
            print('\n')
            opcao = input('digite a opção desejada:')

        if opcao == 1:
            print('\n' * 130)
            main.criaBordero()
            counter = False
        elif opcao == 2:
            print('Se estiver com dúvidas em como usar o sitema, basta ler o arquivo chamado LEIA-ME')
            print('caso precise entrar em contato com o desenvolvedor do sistema utilizar um dos meios abaixo:')
            print('Email: devnicolas.brunaldi@gmail.com')
            print('Whatsapp: (11) 97710-7586')
            input('\nAperte Enter para voltar!')
            print('\n' * 130)
            iniciar()
        elif opcao == 3:
            exit()
        else:
            print('\n' * 130)
            print("Opção selecionada inválida")

            print("Selecione uma das opções abaixo" "\n 1-Criar borderô" "\n 2-Ajuda" "\n 3-Sair")
            print('\n')
            opcao = input('digite a opção desejada:')

if __name__ == "__main__":
    iniciar()