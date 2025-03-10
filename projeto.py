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
    def __init__(self, id, nome, telefone):
        super().__init__(id,nome)
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
    def __init__(self,nome,preco,tipo):
        self.nome = nome
        self.prec o= preco
        self.tipo = tipo

    def get_preco(self):
        return self.preco #retorna o preço do produto

    def get_nome(self):
        return self.nome #retorna o nome do produto

    def get_tipo(self):
        return self.tipo #retorna o tipo do produto

class ItemPedido:
    def __init__(self,produto,quantidade):
        self.produto = produto
        self.quantidade = quantidade
        
    def calcular_subtotal(self):
        return self.produto.get_preco()*self.quantidade

class Pedido(EntidadeRestaurante):
    def __init__(self,id,cliente):
        super().__init__(id, f"Pedido_{id}")
        self.cliente = cliente
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
        self.cliente = cliente
        self.data_hora = data_hora
        self.status = "PENDENTE"
        
    def confirmar_reserva(self):
        self.status = "CONFIRMADA"
    
    def cancelar_reserva(self):
        self.status = "CANCELADA"
    
    def exibir_reserva(self):
        return f"Reserva para {self.cliente.get_info()} em {self.data_hora} | Status: {self.status}"

# Implementação das classes Mesa e Cardapio
class Mesa(EntidadeRestaurante):
    def __init__(self,id,numero,capacidade):
        super().__init__(id,f"Mesa_{numero}")
        self.numero = numero
        self.capacidade = capacidade
        self.ocupada = False
        self.reservada = False
        self.pedidoAtual = None  #Pedido atual na mesa, se houver
        self.reservaAtual = None  # Reserva atual na mesa, se houver

    def ocupar(self,pedido):
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
            tempo_reserva = datetime.now()-self.reservaAtual.data_hora
            if tempo_reserva.total_seconds()>1800:  # 30 minutos
                self.reservaAtual = None
                self.reservada = False

class Cardapio(EntidadeRestaurante):
    def __init__(self,id,descricao):
        super().__init__(id,"Cardapio")
        self.descricao = descricao
        self.produtos = [] # Lista de produtos
    
    def adicionar_produto(self,produto):
        self.produtos.append(produto)
    
    def remover_produto(self, nome_produto):
        self.produtos = [p for p in self.produtos if p.get_nome()!=nome_produto]
    
    def listar_produtos(self):
        return [f"{p.get_nome()} - R$ {p.get_preco():.2f}" for p in self.produtos]


# Classe Promocao 
class Promocao(EntidadeRestaurante):
    def __init__(self, id, descricao, desconto, dataValidade):
        super().__init__(id, "Promocao")
        self.descricao = descricao
        self.desconto = desconto  # Percentual ou valor de desconto
        self.produtos = []        # Lista de produtos aos quais a promoção se aplica
        self.dataValidade = dataValidade
    
    def adicionar_produto(self, produto):
        self.produtos.append(produto)
    
    def remover_produto(self, nome_produto):
        self.produtos=[p for p in self.produtos if p.get_nome()!=nome_produto]
    
    def listar_produtos(self):
        return [f"{p.get_nome()} - R$ {p.get_preco()::.2f}" for p in self.produtos]

# Classe Avaliacao
class Avaliacao(EntidadeRestaurante):
    def __init__(self, id, cliente, nota, comentario):
        super().__init__(id, f"Avaliacao_{id}")
        self.cliente = cliente
        self.nota = nota
        self.comentario = comentario

#Classe Restaurante Central
class Restaurante(EntidadeRestaurante):
    def __init__(self,id,nome,endereco):
        super().__init__(id,nome)
        self.endereco=endereco
        self.funcionarios = []  # Lista de Funcionarios
        self.mesas = []         # Lista de Mesas
        self.pedidos = []       # Lista de Pedidos
        self.clientes = []      # Lista de Clientes
        self.cardapio = None    # Cardapio do restaurante
        self.reservas = []      # Lista de Reservas
        self.promocoes = []     # Lista de Promocoes
        self.avaliacoes = []    # Lista de Avaliacoes
    
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
    
    def criar_reserva(self, reserva):
        self.reservas.append(reserva)
    
    def criar_promocao(self, promocao):
        self.promocoes.append(promocao)
    
    def adicionar_avaliacao(self, avaliacao):
        self.avaliacoes.append(avaliacao)

#Controller simples, organizar melhor depois
#######################################################

class RestauranteController:
    def __init__(self, restaurante):
        self.restaurante = restaurante

    def cadastrar_cliente(self, id_cliente, nome_cliente, telefone_cliente):
        try:
            cliente = Cliente(id_cliente, nome_cliente, telefone_cliente)
            self.restaurante.cadastrar_cliente(cliente)
        except Exception as e:
            raise e

    def cadastrar_funcionario(self, id, nome, telefone, cargo, salario):
        try:
            funcionario = Funcionario(id, nome, telefone, cargo, salario)
            self.restaurante.cadastrar_funcionario(funcionario)
        except Exception as e:
            raise e

    def adicionar_mesa(self, id, numero, capacidade):
        try:
            mesa = Mesa(id, numero, capacidade)
            self.restaurante.adicionar_mesa(mesa)
        except Exception as e:
            raise e

    def definir_cardapio(self, id, descricao):
        try:
            cardapio = Cardapio(id, descricao)
            self.restaurante.definir_cardapio(cardapio)
            return cardapio
        except Exception as e:
            raise e

    def criar_pedido(self, id, cliente, numero_mesa):
        try:
            pedido = Pedido(id, cliente)
            mesa = self.restaurante.mesas[numero_mesa - 1]
            mesa.ocupar(pedido)
            self.restaurante.criar_pedido(pedido)
        except Exception as e:
            raise e

    def criar_reserva(self, id, cliente, data_hora, numero_mesa):
        try:
            reserva = Reserva(id, cliente, data_hora)
            mesa=self.restaurante.mesas[numero_mesa - 1]
            mesa.reservar(reserva)
            self.restaurante.criar_reserva(reserva)
        except Exception as e:
            raise e

    def liberar_mesa(self, numero_mesa):
        try:
            mesa = next((m for m in self.restaurante.mesas if m.numero == numero_mesa), None)
            if mesa:
                mesa.liberar()
            else:
                raise Exception(f"Mesa {numero_mesa} não encontrada.")
                
        except Exception as e:
            raise e

    def adicionar_produto_ao_cardapio(self, nome, preco, tipo):
        try:
            produto = Produto(nome, preco, tipo)
            self.restaurante.cardapio.adicionar_produto(produto)
        except Exception as e:
            raise e
