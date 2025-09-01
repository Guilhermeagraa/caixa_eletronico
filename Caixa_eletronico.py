menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """
saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUES = 3

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        print("=== Depósito ===")
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("Valor inválido! O depósito deve ser maior que zero.")

    elif opcao == "s":
        print("=== Saque ===")
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saque = numero_saque >= LIMITE_SAQUES

        if valor <= 0:
            print("Operação falhou, o valor informado é inválido.")
        elif excedeu_saldo:
            print("Operação falhou, saldo insuficiente.")
        elif excedeu_limite:
            print("Operação falhou, o valor do saque excede o limite.")
        elif excedeu_saque:
            print("Operação falhou, número de saques diário excedido.")
        else:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saque += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    elif opcao == "e":
        print("\n========== EXTRATO ==========")
        if not extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("==============================")

    elif opcao == "q":
        print("Encerrando o sistema. Até logo!")
        break

    else:
        print("Operação inválida, selecione novamente a opção desejada.")
