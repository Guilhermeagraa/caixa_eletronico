from datetime import datetime

# ========================
# Classe Transação (Interface)
# ========================
class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("Método abstrato")


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta._saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso!")
            return True
        print("Valor inválido!")
        return False


class Saque(Transacao):
    def __init__(self, valor, limite=500):
        self.valor = valor
        self.limite = limite

    def registrar(self, conta):
        if self.valor <= 0:
            print("Valor inválido!")
            return False
        if self.valor > conta._saldo:
            print("Saldo insuficiente!")
            return False
        if self.valor > self.limite:
            print(f"Limite de saque é R$ {self.limite:.2f}")
            return False

        conta._saldo -= self.valor
        conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
        print(f"Saque de R$ {self.valor:.2f} realizado com sucesso!")
        return True


# ========================
# Histórico de Transações
# ========================
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.transacoes.append(f"{data} - {descricao}")

    def mostrar(self):
        if not self.transacoes:
            print("Nenhuma movimentação registrada.")
        else:
            for t in self.transacoes:
                print(t)


# ========================
# Conta
# ========================
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        transacao = Saque(valor)
        return transacao.registrar(self)

    def depositar(self, valor):
        transacao = Deposito(valor)
        return transacao.registrar(self)

    def extrato(self):
        print(f"\n=== EXTRATO Agência {self.agencia} Conta {self.numero} ===")
        self.historico.mostrar()
        print(f"Saldo atual: R$ {self._saldo:.2f}")
        print("====================================\n")


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if self.saques_realizados >= self.limite_saques:
            print("Limite de saques diários atingido!")
            return False
        saque = Saque(valor, self.limite)
        sucesso = saque.registrar(self)
        if sucesso:
            self.saques_realizados += 1
        return sucesso


# ========================
# Cliente
# ========================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao: Transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento


# ========================
# Sistema Bancário (Menu)
# ========================
class SistemaBancario:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.proximo_numero_conta = 1

    def criar_usuario(self):
        nome = input("Nome: ")
        data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
        cpf = ''.join(filter(str.isdigit, input("CPF: ")))
        endereco = input("Endereço (logradouro - nº - bairro - cidade/UF): ")

        # Verifica CPF duplicado
        for u in self.usuarios:
            if u.cpf == cpf:
                print("Erro: CPF já cadastrado!")
                return None

        usuario = PessoaFisica(nome, cpf, data_nasc, endereco)
        self.usuarios.append(usuario)
        print(f"Usuário {nome} criado com sucesso!")
        return usuario

    def criar_conta_corrente(self):
        if not self.usuarios:
            print("Não há usuários cadastrados! Crie um usuário primeiro.")
            return None

        print("Usuários disponíveis:")
        for i, u in enumerate(self.usuarios):
            print(f"[{i}] {u.nome} - CPF: {u.cpf}")

        try:
            indice = int(input("Escolha o usuário pelo índice: "))
            usuario = self.usuarios[indice]
        except (ValueError, IndexError):
            print("Usuário inválido!")
            return None

        conta = ContaCorrente(usuario, self.proximo_numero_conta)
        usuario.adicionar_conta(conta)
        self.contas.append(conta)
        print(f"Conta {conta.numero} criada para {usuario.nome}!")
        self.proximo_numero_conta += 1
        return conta

    def selecionar_conta(self):
        if not self.contas:
            print("Não há contas cadastradas!")
            return None

        print("Contas disponíveis:")
        for i, c in enumerate(self.contas):
            print(f"[{i}] Agência {c.agencia} Conta {c.numero} - {c.cliente.nome}")

        try:
            indice = int(input("Escolha a conta pelo índice: "))
            return self.contas[indice]
        except (ValueError, IndexError):
            print("Conta inválida!")
            return None

    def menu(self):
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
                self.criar_usuario()
            elif opcao == "2":
                self.criar_conta_corrente()
            elif opcao == "3":
                conta = self.selecionar_conta()
                if conta:
                    try:
                        valor = float(input("Valor do depósito: "))
                        conta.depositar(valor)
                    except ValueError:
                        print("Entrada inválida!")
            elif opcao == "4":
                conta = self.selecionar_conta()
                if conta:
                    try:
                        valor = float(input("Valor do saque: "))
                        conta.sacar(valor)
                    except ValueError:
                        print("Entrada inválida!")
            elif opcao == "5":
                conta = self.selecionar_conta()
                if conta:
                    conta.extrato()
            elif opcao == "0":
                print("Obrigado por usar o Caixa Eletrônico!")
                break
            else:
                print("Opção inválida! Tente novamente.")


# ========================
# Execução
# ========================
if __name__ == "__main__":
    sistema = SistemaBancario()
    sistema.menu()
