# caixa_eletronico.py
from datetime import datetime

LIMITE_SAQUE = 500  # limite diário por saque

def depositar(saldo, extrato):
    while True:
        try:
            valor = float(input("Digite o valor para depósito e 0 para cancelar: "))
            if valor < 0:
                print("Valor inválido! Informe um valor maior que 0.")
            elif valor == 0:
                print("Depósito cancelado.")
                break
            else:
                saldo += valor
                extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Depósito: R$ {valor:.2f}")
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
                break
        except ValueError:
            print("Valor inválido! Informe apenas números.")
    return saldo

def sacar(saldo, extrato):
    while True:
        try:
            valor = float(input("Digite o valor para saque e 0 para cancelar: "))
            if valor < 0:
                print("Valor inválido! Informe um valor maior que 0.")
            elif valor == 0:
                print("Saque cancelado.")
                break
            elif valor > saldo:
                print("Saldo insuficiente!")
            elif valor > LIMITE_SAQUE:
                print(f"Limite de saque diário é R$ {LIMITE_SAQUE:.2f}")
            else:
                saldo -= valor
                extrato.append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Saque: R$ {valor:.2f}")
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
                break
        except ValueError:
            print("Valor inválido! Informe apenas números.")
    return saldo

def mostrar_extrato(extrato, saldo):
    print("\n===== EXTRATO =====")
    if not extrato:
        print("Nenhuma movimentação realizada.")
    else:
        for movimento in extrato:
            print(movimento)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("==================\n")

def menu():
    saldo = 0
    extrato = []

    while True:
        print("=== CAIXA ELETRÔNICO ===")
        print("[1] Depositar")
        print("[2] Sacar")
        print("[3] Extrato")
        print("[0] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            saldo = depositar(saldo, extrato)
        elif opcao == "2":
            saldo = sacar(saldo, extrato)
        elif opcao == "3":
            mostrar_extrato(extrato, saldo)
        elif opcao == "0":
            print("Obrigado por usar o Caixa Eletrônico!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
