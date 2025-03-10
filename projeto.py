from datetime import datetime
#MODEL
################################################
# Classe Base Comum
class EntidadeRestaurante:
    def __init__(self,id,nome):
        self.id=id #id único para todos os objetos, para facilitar a busca(perdão professor não ter falado isso na hora)
        self.nome=nome #nome para todos os objetos

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
        self.telefone=telefone
        self.cargo=cargo
        self.salario=salario

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
        self.cliente=cliente
        self.itens=[]  # Lista de ItemPedido
    def adicionar_item(self,produto,quantidade):
        self.itens.append(ItemPedido(produto,quantidade))
    def remover_item(self,nome_produto):
        self.itens=[item for item in self.itens if item.produto.get_nome()!=nome_produto]
    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)
    def listar_itens(self):
        return [f"{item.produto.get_nome()} - {item.quantidade} unidades - Subtotal: R$ {item.calcular_subtotal():.2f}" for item in self.itens]

class Reserva(EntidadeRestaurante):
    def __init__(self, id, cliente, data_hora):
        super().__init__(id, f"Reserva_{id}")
        self.cliente=cliente
        self.data_hora=data_hora
        self.status="PENDENTE"
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


# Classe Promocao 
class Promocao(EntidadeRestaurante):
    def __init__(self, id, descricao, desconto, dataValidade):
        super().__init__(id, "Promocao")
        self.descricao=descricao
        self.desconto=desconto  # Percentual ou valor de desconto
        self.produtos=[]        # Lista de produtos aos quais a promoção se aplica
        self.dataValidade=dataValidade
    def adicionar_produto(self, produto):
        self.produtos.append(produto)
    def remover_produto(self, nome_produto):
        self.produtos=[p for p in self.produtos if p.get_nome()!=nome_produto]
    def listar_produtos(self):
        return [f"{p.get_nome()} - R$ {p.get_preco():.2f}" for p in self.produtos]

# Classe Avaliacao
class Avaliacao(EntidadeRestaurante):
    def __init__(self, id, cliente, nota, comentario):
        super().__init__(id, f"Avaliacao_{id}")
        self.cliente=cliente
        self.nota=nota
        self.comentario=comentario

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

#Controller simples, organizar melhor depois
#######################################################

class RestauranteController:
    def __init__(self, restaurante):
        self.restaurante=restaurante

    def cadastrar_cliente(self, id_cliente, nome_cliente, telefone_cliente):
        try:
            cliente=Cliente(id_cliente, nome_cliente, telefone_cliente)
            self.restaurante.clientes.append(cliente)
        except Exception as e:
            raise e

    def cadastrar_funcionario(self, id, nome, telefone, cargo, salario):
        funcionario=Funcionario(id, nome, telefone, cargo, salario)
        self.restaurante.cadastrar_funcionario(funcionario)
        return funcionario

    def adicionar_mesa(self, id, numero, capacidade):
        mesa=Mesa(id, numero, capacidade)
        self.restaurante.adicionar_mesa(mesa)
        return mesa

    def definir_cardapio(self, id, descricao):
        cardapio=Cardapio(id, descricao)
        self.restaurante.definir_cardapio(cardapio)
        return cardapio

    def criar_pedido(self, id, cliente):
        pedido=Pedido(id, cliente)
        self.restaurante.criar_pedido(pedido)
        return pedido

    def criar_reserva(self, id, cliente, data_hora):
        reserva=Reserva(id, cliente, data_hora)
        self.restaurante.criar_reserva(reserva)
        return reserva

    def criar_promocao(self, id, descricao, desconto, dataValidade):
        promocao=Promocao(id, descricao, desconto, dataValidade)
        self.restaurante.criar_promocao(promocao)
        return promocao

    def adicionar_avaliacao(self, id, cliente, nota, comentario):
        avaliacao=Avaliacao(id, cliente, nota, comentario)
        self.restaurante.adicionar_avaliacao(avaliacao)
        return avaliacao

#VIEW
################################################
# Criação do objeto Restaurante central
restaurante=Restaurante(1, "Restaurante Exemplo", "Rua Principal, 123")
controller=RestauranteController(restaurante)

# Configuração inicial de dados para demonstração (caso ainda não existam)
if not restaurante.clientes:
    controller.cadastrar_cliente(1, "João Silva", "123456789")

if not restaurante.funcionarios:
    controller.cadastrar_funcionario(1, "Maria Souza", "987654321", "Garçom", 1500.0)

if not restaurante.mesas:
    controller.adicionar_mesa(1, 1, 4)

if restaurante.cardapio is None:
    cardapio=controller.definir_cardapio(1, "Cardápio do Restaurante Exemplo")
    # Adiciona alguns produtos ao cardápio
    produto1=Produto("Pizza", 35.0)
    produto2=Produto("Refrigerante", 5.0)
    cardapio.adicionar_produto(produto1)
    cardapio.adicionar_produto(produto2)
