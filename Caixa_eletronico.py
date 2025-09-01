from datetime import datetime

# -------------------------
# Configurações iniciais
# -------------------------
LIMITE_SAQUE = 500
AGENCIA_PADRAO = "0001"
proximo_numero_conta = 1

usuarios = []
contas = []

# -------------------------
# Funções de usuário
# -------------------------
def criar_usuario():
    nome = input("Nome: ")
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
    cpf = ''.join(filter(str.isdigit, input("CPF: ")))
    endereco = input("Endereço (logradouro - nº - bairro - cidade/UF): ")

    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("Erro: CPF já cadastrado!")
            return None

    usuario = {
        'nome': nome,
        'data_nascimento': data_nasc,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(usuario)
    print(f"Usuário {nome} criado com sucesso!")
    return usuario

# -------------------------
# Funções de conta
# -------------------------
def criar_conta_corrente():
    global proximo_numero_conta

    if not usuarios:
        print("Não há usuários cadastrados! Crie um usuário primeiro.")
        return None

    print("Usuários disponíveis:")
    for i, u in enumerate(usuarios):
        print(f"[{i}] {u['nome']} - CPF: {u['cpf']}")

    try:
        indice = int(input("Escolha o usuário pelo índice: "))
        usuario = usuarios[indice]
    except (ValueError, IndexError):
        print("Usuário inválido!")
        return None

    conta = {
        'agencia': AGENCIA_PADRAO,
        'numero_conta': proximo_numero_conta,
        'usuario': usuario,
        'saldo': 0,
        'extrato': []
    }
    contas.append(conta)
    proximo_numero_conta += 1
    print(f"Conta {conta['numero_conta']} criada para {usuario['nome']}!")
    return conta

def selecionar_conta():
    if not contas:
        print("Não há contas cadastradas!")
        return None
    print("Contas disponíveis:")
    for i, c in enumerate(contas):
        print(f"[{i}] Agência {c['agencia']} Conta {c['numero_conta']} - {c['usuario']['nome']}")
    try:
        indice = int(input("Escolha a conta pelo índice: "))
        return contas[indice]
    except (ValueError, IndexError):
        print("Conta inválida!")
        return None

# -------------------------
# Funções de operação
# -------------------------
def depositar(conta):
    try:
        valor = float(input("Valor do depósito: "))
        if valor <= 0:
            print("Valor inválido para depósito!")
            return
        conta['saldo'] += valor
        conta['extrato'].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Depósito: R$ {valor:.2f}")
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    except ValueError:
        print("Entrada inválida! Informe apenas números.")

def sacar(conta):
    try:
        valor = float(input("Valor do saque: "))
        if valor <= 0:
            print("Valor inválido para saque!")
            return
        if valor > conta['saldo']:
            print("Saldo insuficiente!")
            return
        if valor > LIMITE_SAQUE:
            print(f"Limite de saque diário é R$ {LIMITE_SAQUE:.2f}")
            return
        conta['saldo'] -= valor
        conta['extrato'].append(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Saque: R$ {valor:.2f}")
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    except ValueError:
        print("Entrada inválida! Informe apenas números.")

def mostrar_extrato(conta):
    print(f"\n===== EXTRATO - Agência {conta['agencia']} Conta {conta['numero_conta']} - {conta['usuario']['nome']} =====")
    if not conta['extrato']:
        print("Nenhuma movimentação realizada.")
    else:
        for movimento in conta['extrato']:
            print(movimento)
    print(f"Saldo atual: R$ {conta['saldo']:.2f}")
    print("====================================================\n")

# -------------------------
# Menu principal
# -------------------------
def menu():
    while True:
        print("=== CAIXA ELETRÔNICO ===")
        print("[1] Criar usuário")
        print("[2] Criar conta corrente")
        print("[3] Depositar")
        print("[4] Sacar")
        print("[5] Extrato")
        print("[0] Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            criar_conta_corrente()
        elif opcao == "3":
            conta = selecionar_conta()
            if conta:
                depositar(conta)
        elif opcao == "4":
            conta = selecionar_conta()
            if conta:
                sacar(conta)
        elif opcao == "5":
            conta = selecionar_conta()
            if conta:
                mostrar_extrato(conta)
        elif opcao == "0":
            print("Obrigado por usar o Caixa Eletrônico!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
