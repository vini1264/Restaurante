from datetime import datetime
################################################
# Classe Base Comum
class EntidadeRestaurante:
    def __init__(self,id,nome):
        self.id=id
        self.nome=nome

# Classes derivadas de EntidadeRestaurante

class Cliente(EntidadeRestaurante):
    def __init__(self,id,nome,telefone):
        super().__init__(id,nome)
        self.telefone=telefone
        self.historicoPedidos=[]  # Lista de pedidos realizados
        self.reservas=[]          # Lista de reservas efetuadas
    def get_info(self):
        return f"{self.nome}-{self.telefone}"
    
class Funcionario(EntidadeRestaurante):
    def __init__(self, id, nome, telefone, cargo, salario):
        super().__init__(id, nome)
        self.telefone = telefone
        self.cargo = cargo
        self.salario = salario

class Produto:
    def __init__(self,nome,preco):
        self.nome=nome
        self.preco=preco
    def get_preco(self):
        return self.preco # Retorna o preço do produto
    def get_nome(self):
        return self.nome # Retorna o nome do produto

class ItemPedido:
    def __init__(self,produto,quantidade):
        self.produto=produto
        self.quantidade=quantidade
    def calcular_subtotal(self):
        return self.produto.get_preco()*self.quantidade

class Pedido(EntidadeRestaurante):
    def __init__(self,id,cliente):
        super().__init__(id, f"Pedido_{id}")
        self.cliente = cliente
        self.itens = []  # Lista de ItemPedido
    def adicionar_item(self,produto,quantidade):
        self.itens.append(ItemPedido(produto,quantidade))
    def remover_item(self,nome_produto):
        self.itens = [item for item in self.itens if item.produto.get_nome()!=nome_produto]
    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)
    def listar_itens(self):
        return [f"{item.produto.get_nome()} - {item.quantidade} unidades - Subtotal: R$ {item.calcular_subtotal():.2f}" for item in self.itens]

class Reserva(EntidadeRestaurante):
    def __init__(self, id, cliente, data_hora):
        super().__init__(id, f"Reserva_{id}")
        self.cliente = cliente
        self.data_hora = data_hora
        self.status = "PENDENTE"
    def confirmar_reserva(self):
        self.status="CONFIRMADA"
    def cancelar_reserva(self):
        self.status="CANCELADA"
    def exibir_reserva(self):
        return f"Reserva para {self.cliente.get_info()} em {self.data_hora} | Status: {self.status}"

# Implementação das classes Mesa e Cardapio
class Mesa(EntidadeRestaurante):
    def __init__(self,id,numero,capacidade):
        super().__init__(id,f"Mesa_{numero}")
        self.numero=numero
        self.capacidade=capacidade
        self.ocupada=False
        self.pedidoAtual=None  # Pedido atual na mesa, se houver
    def ocupar(self,pedido):
        self.ocupada=True
        self.pedidoAtual=pedido
    def liberar(self):
        self.ocupada=False
        self.pedidoAtual=None

class Cardapio(EntidadeRestaurante):
    def __init__(self,id,descricao):
        super().__init__(id,"Cardapio")
        self.descricao=descricao
        self.produtos=[] # Lista de produtos
    def adicionar_produto(self,produto):
        self.produtos.append(produto)
    def remover_produto(self, nome_produto):
        self.produtos=[p for p in self.produtos if p.get_nome()!=nome_produto]
    def listar_produtos(self):
        return [f"{p.get_nome()} - R$ {p.get_preco():.2f}" for p in self.produtos]

#Classe Restaurante Central
class Restaurante(EntidadeRestaurante):
    def __init__(self,id,nome,endereco):
        super().__init__(id,nome)
        self.endereco=endereco
        self.funcionarios=[]  # Lista de Funcionarios
        self.mesas=[]         # Lista de Mesas
        self.pedidos=[]       # Lista de Pedidos
        self.clientes=[]      # Lista de Clientes
        self.cardapio=None    # Cardapio do restaurante
        self.reservas=[]      # Lista de Reservas
    def cadastrar_cliente(self,cliente):
        self.clientes.append(cliente)
    def cadastrar_funcionario(self,funcionario):
        self.funcionarios.append(funcionario)
    def adicionar_mesa(self,mesa):
        self.mesas.append(mesa)
    def definir_cardapio(self,cardapio):
        self.cardapio=cardapio
    def criar_pedido(self, pedido):
        self.pedidos.append(pedido)

  
