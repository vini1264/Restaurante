from datetime import datetime

# MODEL
################################################
# Classe Base Comum
class EntidadeRestaurante:
    def __init__(self, id, nome):
        self.id = id  # id único para todos os objetos, para facilitar a busca
        self.nome = nome  # nome para todos os objetos

# Classes derivadas de EntidadeRestaurante

class Cliente(EntidadeRestaurante):
    def __init__(self, id, nome, telefone):
        super().__init__(id, nome)
        self.telefone = telefone
        self.historicoPedidos = []  # Lista de pedidos realizados
        self.reservas = []          # Lista de reservas efetuadas

    def get_info(self):
        return f"Nome: {self.nome} - Telefone: {self.telefone}"

class Funcionario(EntidadeRestaurante):
    def __init__(self, id, nome, telefone, cargo, salario):
        super().__init__(id, nome)
        self.telefone = telefone
        self.cargo = cargo
        self.salario = salario

    def get_info(self):
        return f"{self.nome} - {self.telefone} - {self.cargo} - R$ {self.salario:.2f}"

class Produto:
    def __init__(self, nome, preco, tipo):
        self.nome = nome
        self.preco = preco
        self.tipo = tipo

    def get_preco(self):
        return self.preco

    def get_nome(self):
        return self.nome

    def get_tipo(self):
        return self.tipo

class ItemPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_subtotal(self):
        return self.produto.get_preco() * self.quantidade

class Pedido(EntidadeRestaurante):
    def __init__(self, id, cliente):
        super().__init__(id, f"Pedido_{id}")
        self.cliente = cliente
        self.itens = []  # Lista de ItemPedido

    def adicionar_item(self, produto, quantidade):
        self.itens.append(ItemPedido(produto, quantidade))

    def remover_item(self, nome_produto):
        self.itens = [item for item in self.itens if item.produto.get_nome() != nome_produto]

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def listar_itens(self):
        return [f"{item.produto.get_nome()} - {item.quantidade} unidades - Subtotal: R$ {item.calcular_subtotal():.2f}" for item in self.itens]

# Classe Reserva atualizada para incluir a mesa
class Reserva(EntidadeRestaurante):
    def __init__(self, id, cliente, data_hora, mesa):
        super().__init__(id, f"Reserva_{id}")
        self.cliente = cliente
        self.data_hora = data_hora
        self.mesa = mesa
        self.status = "PENDENTE"

    def confirmar_reserva(self):
        self.status = "CONFIRMADA"

    def cancelar_reserva(self):
        self.status = "CANCELADA"

    def exibir_reserva(self):
        return f"Reserva para {self.cliente.get_info()} na Mesa {self.mesa.numero} em {self.data_hora} | Status: {self.status}"

class Mesa(EntidadeRestaurante):
    def __init__(self, id, numero, capacidade):
        super().__init__(id, f"Mesa_{numero}")
        self.numero = numero
        self.capacidade = capacidade
        self.ocupada = False
        self.reservada = False
        self.pedidoAtual = None  # Pedido atual na mesa, se houver
        self.reservaAtual = None  # Reserva atual na mesa, se houver

    def ocupar(self, pedido):
        if not self.ocupada and not self.reservada:
            self.ocupada = True
            self.pedidoAtual = pedido
        else:
            raise Exception("Mesa já está ocupada ou reservada")

    def reservar(self, reserva):
        if not self.ocupada and not self.reservada:
            self.reservada = True
            self.reservaAtual = reserva
        else:
            raise Exception("Mesa já está ocupada ou reservada")

    def liberar(self):
        if self.pedidoAtual is None and self.reservaAtual is None:
            self.ocupada = False
            self.reservada = False
        else:
            raise Exception("Mesa não pode ser liberada, pois há um pedido ou reserva ativa")

    def verificar_reserva(self):
        if self.reservaAtual:
            tempo_reserva = datetime.now() - self.reservaAtual.data_hora
            if tempo_reserva.total_seconds() > 1800:  # 30 minutos
                self.reservaAtual = None
                self.reservada = False

class Cardapio(EntidadeRestaurante):
    def __init__(self, id, descricao):
        super().__init__(id, "Cardapio")
        self.descricao = descricao
        self.produtos = []  # Lista de produtos

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def remover_produto(self, nome_produto):
        self.produtos = [p for p in self.produtos if p.get_nome() != nome_produto]

    def listar_produtos(self):
        return self.produtos

# Classe Promoção atualizada para incluir título e data de validade opcional
class Promocao(EntidadeRestaurante):
    def __init__(self, id, titulo, descricao, desconto, dataValidade=None):
        super().__init__(id, "Promocao")
        self.titulo = titulo
        self.descricao = descricao
        self.desconto = desconto  # Percentual ou valor de desconto
        self.produtos = []        # Lista de produtos aos quais a promoção se aplica
        self.dataValidade = dataValidade

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

    def remover_produto(self, nome_produto):
        self.produtos = [p for p in self.produtos if p.get_nome() != nome_produto]

    def listar_produtos(self):
        return [f"{p.get_nome()} - R$ {p.get_preco():.2f}" for p in self.produtos]

class Avaliacao(EntidadeRestaurante):
    def __init__(self, id, cliente, nota, comentario):
        super().__init__(id, f"Avaliacao_{id}")
        self.cliente = cliente
        self.nota = nota
        self.comentario = comentario

# Classe Restaurante Central
class Restaurante(EntidadeRestaurante):
    def __init__(self, id, nome, endereco):
        super().__init__(id, nome)
        self.endereco = endereco
        self.funcionarios = []  # Lista de Funcionarios
        self.mesas = []         # Lista de Mesas
        self.pedidos = []       # Lista de Pedidos
        self.clientes = []      # Lista de Clientes
        self.cardapio = None    # Cardapio do restaurante
        self.reservas = []      # Lista de Reservas
        self.promocoes = []     # Lista de Promocoes
        self.avaliacoes = []    # Lista de Avaliacoes

    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)

    def cadastrar_funcionario(self, funcionario):
        self.funcionarios.append(funcionario)

    def adicionar_mesa(self, mesa):
        self.mesas.append(mesa)

    def definir_cardapio(self, cardapio):
        self.cardapio = cardapio

    def criar_pedido(self, pedido):
        self.pedidos.append(pedido)

    def criar_reserva(self, reserva):
        self.reservas.append(reserva)

    def criar_promocao(self, promocao):
        self.promocoes.append(promocao)

    def adicionar_avaliacao(self, avaliacao):
        self.avaliacoes.append(avaliacao)

# Controller simples e com persistência
#######################################################
import pickle
import os

class RestauranteController:
    def __init__(self, restaurante):
        self.restaurante = restaurante

    def cadastrar_cliente(self, id_cliente, nome_cliente, telefone_cliente):
        if any(c.id == id_cliente for c in self.restaurante.clientes):
            raise Exception("Cliente com este ID já existe.")
        cliente = Cliente(id_cliente, nome_cliente, telefone_cliente)
        self.restaurante.cadastrar_cliente(cliente)

    def cadastrar_funcionario(self, id, nome, telefone, cargo, salario):
        if any(f.id == id for f in self.restaurante.funcionarios):
            raise Exception("Funcionário com este ID já existe.")
        funcionario = Funcionario(id, nome, telefone, cargo, salario)
        self.restaurante.cadastrar_funcionario(funcionario)

    def adicionar_mesa(self, id, numero, capacidade):
        if any(m.numero == numero for m in self.restaurante.mesas):
            raise Exception("Mesa com este número já existe.")
        mesa = Mesa(id, numero, capacidade)
        self.restaurante.adicionar_mesa(mesa)

    def definir_cardapio(self, id, descricao):
        cardapio = Cardapio(id, descricao)
        self.restaurante.definir_cardapio(cardapio)
        return cardapio

    def criar_pedido(self, id, cliente, numero_mesa):
        pedido = Pedido(id, cliente)
        mesa = next((m for m in self.restaurante.mesas if m.numero == numero_mesa), None)
        if mesa is None:
            raise Exception("Mesa não encontrada.")
        mesa.ocupar(pedido)
        self.restaurante.criar_pedido(pedido)

    def criar_reserva(self, id, cliente, data_hora, numero_mesa):
        mesa = next((m for m in self.restaurante.mesas if m.numero == numero_mesa), None)
        if mesa is None:
            raise Exception("Mesa não encontrada.")
        reserva = Reserva(id, cliente, data_hora, mesa)
        mesa.reservar(reserva)
        self.restaurante.criar_reserva(reserva)

    def liberar_mesa(self, numero_mesa):
        mesa = next((m for m in self.restaurante.mesas if m.numero == numero_mesa), None)
        if mesa:
            mesa.liberar()
        else:
            raise Exception(f"Mesa {numero_mesa} não encontrada.")

    def adicionar_produto_ao_cardapio(self, nome, preco, tipo):
        if self.restaurante.cardapio is None:
            raise Exception("Cardápio não definido.")
        produto = Produto(nome, preco, tipo)
        self.restaurante.cardapio.adicionar_produto(produto)

    def salvar_dados(self, filename="restaurante_data.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.restaurante, f)

    @staticmethod
    def carregar_dados(filename="restaurante_data.pkl"):
        if os.path.exists(filename):
            with open(filename, "rb") as f:
                restaurante = pickle.load(f)
            return restaurante
        else:
            return None
