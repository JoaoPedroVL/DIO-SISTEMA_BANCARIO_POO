from abc import ABC
from datetime import datetime



class Cliente:
    def __init__(self, endereco = str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
    

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = float(0)
        self._numero = int(numero)
        self._agencia = str("0001")
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self.saldo
    
    @property
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_valor = valor > saldo

        if excedeu_valor:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True
    
        else:
            print("Valor inválido para saque.")
            return False
        
    def depositar(self, valor):
        if valor <= 0:
            print("Oops... Valor de depósito deve ser maior que zero.")
            return False
        else:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")


class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):    
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._trnasacoes = []

    @property
    def transacoes(self):
        self.transacoes
    
    def adicionar_transacao(self, transacao):
        self._trnasacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })

class Transacao(ABC):
    @property
    def valor(self):
        pass

    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    class Deposito(Transacao):
        def __init__(self, valor):
            self._valor = valor

        @property
        def valor(self):
            return self._valor  
        
        def registrar(self, conta):
            sucesso_transacao = conta.depositar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)              
        