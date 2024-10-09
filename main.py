import time as t
import json
import random
from datetime import datetime

global cpf
global senha
global dadosU  # dados usuario


def jsonappend(novo, arquivo):
    with open(arquivo, "r+") as arquivo:
        valores = json.load(arquivo)
        valores.append(novo)
        arquivo.seek(0)
        json.dump(valores, arquivo, indent=4)


def login():
    global dadosU
    global cpf
    global senha

    print("-" * 20)
    print("Informe seu login!")

    cadastro = input("Você já possui cadastro? (sim/não): ")

    if cadastro.lower() == "não":
        nome = input("Informe seu nome: ")
        cpflogin = input("Informe seu CPF (apenas dígitos): ")
        senhalogin = input("Informe sua senha: ")

        novo_usuario = {
            "nome": nome,
            "cpf": cpflogin,
            "senha": senhalogin,
            "reais": 0.0,
            "bitcoin": 0.0,
            "ethereum": 0.0,
            "ripple": 0.0,
            "extrato": []
        }
        jsonappend(novo_usuario, "dados.json")
        print("Cadastro realizado com sucesso!")
        dadosU = novo_usuario
        cpf = cpflogin
        senha = senhalogin
        menu_investidor()
        return  

    elif cadastro.lower() == "sim":
        while True:
            cpf = input("CPF (apenas dígitos): ")
            senha = input("Senha (apenas dígitos): ")
            try:
                with open("dados.json", "r", encoding="utf-8") as file:
                    dados = json.load(file)
            except FileNotFoundError:
                print("Nenhum cadastro encontrado. Por favor, faça o cadastro primeiro.")
                login()
                return

            for i in dados:
                if i["cpf"] == cpf and i["senha"] == senha:
                    dadosU = i
                    print("Login feito com sucesso!")
                    menu_investidor()
                    return
            print("CPF e/ou senha incorretos!")
    else:
        print("Opção inválida.")
        login()


def consultarCpf(cpf):
    cpfDeco = "{:011}".format(cpf)
    cpf = f'{cpfDeco[:3]}.{cpfDeco[3:6]}.{cpfDeco[6:9]}-{cpfDeco[9:]}'
    return cpf


def consultar_saldo():
    global cpf
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario["cpf"] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            print(
                f"\nNome: {usuario_logado['nome']}\nReais: {usuario_logado['reais']:.2f}\nBitcoin: {usuario_logado['bitcoin']:.4f}\nEthereum: {usuario_logado['ethereum']:.2f}\nRipple: {usuario_logado['ripple']:.2f}\nCPF: {consultarCpf(int(usuario_logado['cpf']))}"
            )
        else:
            print("Usuário não encontrado.")

    t.sleep(3)
    menu_investidor()


def consultar_extrato():
    global cpf
    print("Extrato de transações:")
    with open("dados.json", "r") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario["cpf"] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            for transacao in usuario_logado.get("extrato", []):
                print(
                    f"Data: {transacao['data']}, Hora: {transacao['hora']}, Operação: {transacao['operacao']}, Valor: {transacao['valor']}, Moeda: {transacao['moeda']}"
                )
        else:
            print("Usuário não encontrado.")

    t.sleep(3)
    menu_investidor()


def depositar():
    global cpf
    depositoReais = int(input("Digite quantos reais você deseja depositar: "))

    with open("dados.json", "r+") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario['cpf'] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            usuario_logado['reais'] += depositoReais
            usuario_logado['extrato'].append({
                "data":
                datetime.today().strftime('%d-%m-%Y'),
                "hora":
                datetime.today().strftime('%H:%M'),
                "operacao":
                "+",
                "valor":
                depositoReais,
                "moeda":
                "REAL"
            })
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
            arquivo.truncate()
            print(
                f"\nSaldo atual:\nReais: {usuario_logado['reais']:.2f}\nBitcoin: {usuario_logado['bitcoin']:.4f}\nEthereum: {usuario_logado['ethereum']:.2f}\nRipple: {usuario_logado['ripple']:.2f}\n"
            )
        else:
            print("Usuário não encontrado.")

    t.sleep(3)
    menu_investidor()


def sacar():
    global cpf
    with open("dados.json", "r+") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario['cpf'] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            while True:
                sacarReais = float(
                    input("Digite quantos reais você deseja sacar: "))
                if usuario_logado['reais'] - sacarReais < 0:
                    print("Você tentou sacar mais do que possui!")
                    continue
                else:
                    usuario_logado['reais'] -= sacarReais
                    usuario_logado['extrato'].append({
                        "data":
                        datetime.today().strftime('%d-%m-%Y'),
                        "hora":
                        datetime.today().strftime('%H:%M'),
                        "operacao":
                        "-",
                        "valor":
                        sacarReais,
                        "moeda":
                        "REAL"
                    })
                    print(
                        f"\nReais: {usuario_logado['reais']:.2f}\nBitcoin: {usuario_logado['bitcoin']:.4f}\nEthereum: {usuario_logado['ethereum']:.2f}\nRipple: {usuario_logado['ripple']:.2f}\n"
                    )
                    break
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
            arquivo.truncate()
        else:
            print("Usuário não encontrado.")

    t.sleep(3)
    menu_investidor()


def comprar_criptomoedas():
    global cpf
    with open("dados.json", "r+") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario['cpf'] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            valor = float(
                input("Digite o valor de criptomoedas que deseja comprar: "))
            cripto = input(
                "Digite a criptomoeda que deseja comprar (BTC, ETH, XRP): "
            ).upper()

            if valor <= usuario_logado['reais']:
                if cripto == 'BTC':
                    usuario_logado['bitcoin'] += valor
                elif cripto == 'ETH':
                    usuario_logado['ethereum'] += valor
                elif cripto == 'XRP':
                    usuario_logado['ripple'] += valor
                else:
                    print("Criptomoeda inválida.")
                    return

                usuario_logado['reais'] -= valor
                usuario_logado['extrato'].append({
                    "data":
                    datetime.today().strftime('%d-%m-%Y'),
                    "hora":
                    datetime.today().strftime('%H:%M'),
                    "operacao":
                    "compra",
                    "valor":
                    valor,
                    "moeda":
                    cripto
                })
                print(
                    f"\nReais: {usuario_logado['reais']:.2f}\nBitcoin: {usuario_logado['bitcoin']:.4f}\nEthereum: {usuario_logado['ethereum']:.2f}\nRipple: {usuario_logado['ripple']:.2f}\n"
                )
                arquivo.seek(0)
                json.dump(dados, arquivo, indent=4)
                arquivo.truncate()
            else:
                print("Saldo insuficiente para comprar criptomoedas.")
        else:
            print("Usuário não encontrado.")

    t.sleep(3)
    menu_investidor()

def vender_criptomoedas():
    global cpf
    with open("dados.json", "r+") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario['cpf'] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            cripto = input(
                "Digite a criptomoeda que deseja vender (BTC, ETH, XRP): "
            ).upper()
            valor = float(
                input("Digite o valor de criptomoedas que deseja vender: "))

            if cripto == 'BTC' and valor <= usuario_logado['bitcoin']:
                usuario_logado['bitcoin'] -= valor
                usuario_logado['reais'] += valor
            elif cripto == 'ETH' and valor <= usuario_logado['ethereum']:
                usuario_logado['ethereum'] -= valor
                usuario_logado['reais'] += valor
            elif cripto == 'XRP' and valor <= usuario_logado['ripple']:
                usuario_logado['ripple'] -= valor
                usuario_logado['reais'] += valor
            else:
                print(
                    "Saldo insuficiente para vender ou criptomoeda inválida.")
                return

            usuario_logado['extrato'].append({
                "data":
                datetime.today().strftime('%d-%m-%Y'),
                "hora":
                datetime.today().strftime('%H:%M'),
                "operacao":
                "venda",
                "valor":
                valor,
                "moeda":
                cripto
            })
            print(
                f"\nReais: {usuario_logado['reais']:.2f}\nBitcoin: {usuario_logado['bitcoin']:.4f}\nEthereum: {usuario_logado['ethereum']:.2f}\nRipple: {usuario_logado['ripple']:.2f}\n"
            )
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
            arquivo.truncate()
        else:
            print("Usuário não encontrado.")
        
    t.sleep(3)
    menu_investidor()



def atualizar_cotacoes():
    global cpf
    with open("dados.json", "r+") as arquivo:
        dados = json.load(arquivo)
        usuario_logado = None
        for usuario in dados:
            if usuario['cpf'] == cpf:
                usuario_logado = usuario
                break

        if usuario_logado:
            cotacoes = {
                "bitcoin": usuario_logado['bitcoin'],
                "ethereum": usuario_logado['ethereum'],
                "ripple": usuario_logado['ripple']
            }
            cotacoes_atualizadas = []
            for key, value in cotacoes.items():
                variation = random.uniform(-0.05, 0.05)
                new_value = value * (1 + variation)
                usuario_logado[key] = new_value
                cotacoes_atualizadas.append(f"{key.capitalize()}: {new_value:.2f}")
            print("Cotações atualizadas com sucesso!")
            print("Valores atualizados:")
            print("\n".join(cotacoes_atualizadas))
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
            arquivo.truncate()
        else:
            print("Usuário não encontrado.")

    t.sleep(3)
    menu_investidor()


def menu_investidor():
    print("-" * 20)
    print("1- Consultar Saldo")
    print("2- Consultar Extrato")
    print("3- Depositar")
    print("4- Sacar")
    print("5- Comprar Criptomoedas")
    print("6- Vender Criptomoedas")
    print("7- Atualizar Cotações")
    print("8- Sair")

    opcao = int(input("Escolha uma das opções: "))

    if opcao == 1:
        consultar_saldo()
    elif opcao == 2:
        consultar_extrato()
    elif opcao == 3:
        depositar()
    elif opcao == 4:
        sacar()
    elif opcao == 5:
        comprar_criptomoedas()
    elif opcao == 6:
        vender_criptomoedas()
    elif opcao == 7:
        atualizar_cotacoes()
    elif opcao == 8:
        print("Saindo...")
    else:
        print("Opção inválida!")
        menu_investidor()


login()
