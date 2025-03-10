# Bibliotecas para baixar:
# pip install streamlit

import streamlit as st
from datetime import datetime

# Importação do código principal do restaurante
from projeto import Restaurante, RestauranteController, Produto, Cliente, Funcionario, Mesa, Cardapio, Pedido, Reserva, Promocao, Avaliacao

# Se não existir, cria a variável de estado "option" com valor inicial "Home"
if "option" not in st.session_state:
    st.session_state["option"] = "Home"

######################################
# Inicialização do sistema (Model + Controller)
######################################
restaurante = Restaurante(1, "Restaurante Exemplo", "Rua Principal, 123")
controller = RestauranteController(restaurante)

# Configuração inicial de dados para demonstração
if not restaurante.clientes:
    controller.cadastrar_cliente(1, "João Silva", "123456789")

if not restaurante.funcionarios:
    controller.cadastrar_funcionario(1, "Maria Souza", "987654321", "Garçom", 1500.0)

if not restaurante.mesas:
    controller.adicionar_mesa(1, 10, 4)
    controller.adicionar_mesa(2, 20, 4)
    controller.adicionar_mesa(3, 30, 4)
    controller.adicionar_mesa(4, 40, 4)
    controller.adicionar_mesa(5, 50, 4)
    controller.adicionar_mesa(6, 60, 4)
    controller.adicionar_mesa(7, 70, 4)
    controller.adicionar_mesa(8, 80, 4)
    controller.adicionar_mesa(9, 90, 4)
    controller.adicionar_mesa(10, 110, 8)
    controller.adicionar_mesa(11, 210, 8)
    controller.adicionar_mesa(12, 310, 8)

if restaurante.cardapio is None:
    cardapio = controller.definir_cardapio(1, "Cardápio do Restaurante Exemplo")
    produto1 = Produto("Pizza", 35.0, "Alimento")
    produto2 = Produto("Refrigerante", 5.0, "Bebida")
    cardapio.adicionar_produto(produto1)
    cardapio.adicionar_produto(produto2)

######################################
# Barra Lateral (selectbox)
######################################
# O 'index' é definido com base em st.session_state["option"]
paginas = ["Home", "Clientes", "Funcionários", "Mesas", "Cardápio", "Pedidos", "Reservas", "Promoções", "Avaliações"]
# Para evitar erro de 'ValueError' caso a session_state esteja fora da lista, checamos:
if st.session_state["option"] not in paginas:
    st.session_state["option"] = "Home"

option_index = paginas.index(st.session_state["option"])
option = st.sidebar.selectbox("Selecione uma opção:", paginas, index=option_index)

# Se o usuário mudou o selectbox manualmente, atualizamos o session_state e recarregamos:
if option != st.session_state["option"]:
    st.session_state["option"] = option
    st.rerun()
######################################
# Lógica de navegação
######################################
if st.session_state["option"] == "Home":
    st.title("Sistema de Restaurante")
    st.write("Bem-vindo ao sistema de restaurante!")
    st.write("Escolha abaixo a funcionalidade que deseja ou utilize o menu lateral para navegar entre as funcionalidades.")

    # Exibe uma imagem e um botão para ir a 'Clientes'
    st.image("https://blog.artdescaves.com.br/hubfs/blog/6-dicas-para-agradar-os-clientes-do-seu-restaurante.jpg")
    if st.button("Clientes"):
        st.session_state["option"] = "Clientes"
        st.rerun()

    st.image("https://www.menucontrol.com.br/wp-content/uploads/2022/05/group-hotel-staffs-standing-kitchen-scaled-1.jpg")
    if st.button("Funcionários"):
        st.session_state["option"] = "Funcionários"
        st.rerun()

    st.image("https://www.housecustomize.com/wp-content/uploads/2023/08/02-2-64ed9ce0773f5-1024x758.webp")
    if st.button("Mesas"):
        st.session_state["option"] = "Mesas"
        st.rerun()

    st.image("https://www.tribunapr.com.br/wp-content/uploads/2020/01/30161957/CARD%C3%81PIO-TECNICOPIAS-970x550.jpg")
    if st.button("Cardápio"):
        st.session_state["option"] = "Cardápio"
        st.rerun()

    st.image("https://img.elo7.com.br/product/zoom/502C0B7/bloco-de-pedidos-para-restaurantes-empresa.jpg")
    if st.button("Pedidos"):
        st.session_state["option"] = "Pedidos"
        st.rerun()

    st.image("https://cms-bomgourmet.s3.amazonaws.com/bomgourmet%2F2021%2F06%2F11152136%2Fmesa-reservada-foto-bigstock.jpg")
    if st.button("Reservas"):
        st.session_state["option"] = "Reservas"
        st.rerun()

    st.image("https://img.cdndsgni.com/preview/10034124.jpg")
    if st.button("Promoções"):
        st.session_state["option"] = "Promoções"
        st.rerun()

    st.image("https://static.vecteezy.com/ti/vetor-gratis/t1/11802277-modelo-de-avaliacao-de-restaurante-ilustracao-plana-de-desenho-animado-desenhado-a-mao-com-feedback-do-cliente-estrela-de-taxa-opiniao-de-especialistas-e-pesquisa-on-line-vetor.jpg")
    if st.button("Avaliações"):
        st.session_state["option"] = "Avaliações"
        st.rerun()

# Dentro da lógica de navegação, na seção "Clientes":
if st.session_state["option"] == "Clientes":
    st.subheader("Clientes Cadastrados")
    # Formulário para cadastrar um novo cliente
    with st.form("cadastro_cliente"):
        st.subheader("Cadastrar Novo Cliente")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        nome_cliente = st.text_input("Nome do Cliente")
        telefone_cliente = st.text_input("Telefone do Cliente")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if id_cliente and nome_cliente and telefone_cliente:
                # Verifica se já existe um cliente com esse ID
                if any(c.id == id_cliente for c in restaurante.clientes):
                    st.warning("Já existe um cliente com esse ID.")
                else:
                    try:
                        controller.cadastrar_cliente(id_cliente, nome_cliente, telefone_cliente)
                        st.success(f"Cliente {nome_cliente} cadastrado com sucesso!")
                    except Exception as e:  
                        st.error(f"Ocorreu um erro ao cadastrar o cliente: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    
    # Lista os clientes cadastrados
    for cliente in restaurante.clientes:
        st.write(cliente.get_info())
    st.write("Total de clientes cadastrados: ", len(restaurante.clientes))

# Dentro da lógica de navegação, na seção Funcionários:
elif st.session_state["option"] == "Funcionários":
    st.subheader("Funcionários")

    # Formulário para cadastrar um novo funcionário
    with st.form("cadastro_de_funcionario"):
        st.subheader("Cadastrar Novo Funcionário")
        id_funcionario = st.number_input("ID do Funcionário", min_value=1, step=1)
        nome_funcionario = st.text_input("Nome do Funcionário:")
        telefone_funcionario = st.text_input("Telefone do Funcionário:")
        cargo_funcionario = st.text_input("Cargo do Funcionário:")
        salario_funcionario = st.number_input("Salário do Funcionário", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if id_funcionario and nome_funcionario and telefone_funcionario: # Verifica se já existe um funcionário com esse ID
                if any(c.id == id_funcionario for c in restaurante.funcionarios):
                    st.warning("Já existe um Funcionário com esse ID.")
                else:
                    try:
                        controller.cadastrar_funcionario(id_funcionario, nome_funcionario, telefone_funcionario, cargo_funcionario, salario_funcionario)
                        st.success(f"Funcionário {nome_funcionario} cadastrado com sucesso!")
                    except Exception as e:  
                        st.error(f"Ocorreu um erro ao cadastrar o funcionário: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    
    # Lista dos funcionários cadastrados
    st.subheader("Funcionários Cadastrados")
    st.write("ID - Nome - Telefone - Cargo - Salário")
    for funcionario in restaurante.funcionarios:
        st.write(funcionario.get_info())
    st.write("Total de funcionários cadastrados: ", len(restaurante.funcionarios))

#Imagina que o local seria um restaurante fixo, então não seria necessário cadastrar mesas
elif st.session_state["option"] == "Mesas":
    st.subheader("Mesas")

    # Formulário para liberar uma mesa
    with st.form("liberar_mesa"):
        st.subheader("Liberar Mesa")
        numero_mesa_liberar = st.number_input("Número da Mesa para Liberar", min_value=10, step=10)
        submitted = st.form_submit_button("Liberar Mesa")
        if submitted:
            try:
                mesa = next((m for m in restaurante.mesas if m.numero == numero_mesa_liberar), None)
                if mesa:
                    controller.liberar_mesa(numero_mesa_liberar)
                    st.success(f"Mesa {numero_mesa_liberar} liberada com sucesso!")
                else:
                    st.error(f"Mesa {numero_mesa_liberar} não existe.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao liberar a mesa: {e}")

    # Lista as mesas cadastradas
    st.subheader("Mesas Cadastradas")
    for mesa in restaurante.mesas:
        status = "Ocupada" if mesa.ocupada else "Reservada" if mesa.reservada else "Livre"
        st.write(f"Mesa {mesa.numero} - Capacidade: {mesa.capacidade} - Status: {status}")

elif st.session_state["option"] == "Cardápio":
    st.subheader("Cardápio")

    # Formulário para adicionar um novo produto ao cardápio
    with st.form("adicionar_produto"):
        st.subheader("Adicionar Novo Produto")
        nome_produto = st.text_input("Nome do Produto")
        preco_produto = st.number_input("Preço do Produto", min_value=0.0, step=0.01)
        tipo_produto = st.selectbox("Tipo do Produto", ["Alimento", "Bebida"])
        submitted = st.form_submit_button("Adicionar")
        if submitted:
            if nome_produto and preco_produto:
                try:
                    controller.adicionar_produto_ao_cardapio(nome_produto, preco_produto, tipo_produto)
                    st.success(f"Produto {nome_produto} adicionado com sucesso!")
                except Exception as e:
                    st.error(f"Ocorreu um erro ao adicionar o produto: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")

    # Lista os produtos cadastrados no cardápio
    st.subheader("Produtos no Cardápio")
    if restaurante.cardapio:
        alimentos = [prod for prod in restaurante.cardapio.listar_produtos() if prod.get_tipo() == "Alimento"]
        bebidas = [prod for prod in restaurante.cardapio.listar_produtos() if prod.get_tipo() == "Bebida"]

        st.write("**Alimentos**")
        for comida in alimentos:
            st.write(f"{comida.get_nome()} - R$ {comida.get_preco():.2f}")

        st.write("**Bebidas**")
        for bebida in bebidas:
            st.write(f"{bebida.get_nome()} - R$ {bebida.get_preco():.2f}")

elif st.session_state["option"] == "Pedidos":
    st.subheader("Pedidos")

    # Formulário para criar um pedido em uma mesa
    with st.form("criar_pedido"):
        st.subheader("Criar Pedido")
        id_pedido = st.number_input("ID do Pedido", min_value=1, step=1)
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        numero_mesa_pedido = st.number_input("Número da Mesa para o Pedido", min_value=1, step=1)
        submitted = st.form_submit_button("Criar Pedido")
        if submitted:
            try:
                cliente = next(c for c in restaurante.clientes if c.id == id_cliente)
                controller.criar_pedido(id_pedido, cliente, numero_mesa_pedido)
                st.success(f"Pedido {id_pedido} criado com sucesso na mesa {numero_mesa_pedido}!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao criar o pedido: {e}")

    # Lista os pedidos cadastrados
    for pedido in restaurante.pedidos:
        st.write(f"{pedido.nome} - Total: R$ {pedido.calcular_total():.2f}")
        for item in pedido.listar_itens():
            st.write(f"  - {item}")

class Cliente:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

class Mesa:
    def __init__(self, numero):
        self.numero = numero

class Avaliacao:
    def __init__(self, cliente, nota, comentario):
        self.cliente = cliente
        self.nota = nota
        self.comentario = comentario

class Reserva:
    def __init__(self, cliente, mesa, data):
        self.cliente = cliente
        self.mesa = mesa
        self.data = data

# Inicializando o estado da aplicação
if "avaliacoes" not in st.session_state:
    st.session_state["avaliacoes"] = []

if "reservas" not in st.session_state:
    st.session_state["reservas"] = []

if "clientes" not in st.session_state:
    st.session_state["clientes"] = [Cliente(1, "Carlos"), Cliente(2, "Ana")]  # Exemplo de clientes

if "mesas" not in st.session_state:
    st.session_state["mesas"] = [Mesa(1), Mesa(2)]  # Exemplo de mesas

######################################
# Lógica de navegação - Avaliações
######################################
if st.session_state["option"] == "Avaliações":
    st.subheader("Avaliações")

    # Formulário para cadastrar uma avaliação
    with st.form("cadastro_avaliacao"):
        st.subheader("Cadastrar Nova Avaliação")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        nota = st.slider("Nota (1-5)", min_value=1, max_value=5, step=1)
        comentario = st.text_area("Comentário")
        submitted = st.form_submit_button("Enviar Avaliação")
        if submitted:
            cliente = next((c for c in st.session_state["clientes"] if c.id == id_cliente), None)
            if cliente:
                try:
                    avaliacao = Avaliacao(cliente, nota, comentario)
                    st.session_state["avaliacoes"].append(avaliacao)
                    st.success("Avaliação registrada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar avaliação: {e}")
            else:
                st.error("Cliente não encontrado. Verifique o ID.")

    # Lista avaliações cadastradas
    st.subheader("Avaliações dos Clientes")
    for i, avaliacao in enumerate(st.session_state["avaliacoes"]):
        st.write(f"{avaliacao.cliente.nome} avaliou com nota {avaliacao.nota}: {avaliacao.comentario}")

        # Editar e excluir avaliação
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Editar {i}"):
                # Formulário de edição
                new_nota = st.slider(f"Nova nota para {avaliacao.cliente.nome}", min_value=1, max_value=5, step=1, value=avaliacao.nota)
                new_comentario = st.text_area(f"Novo comentário para {avaliacao.cliente.nome}", value=avaliacao.comentario)
                if st.button("Confirmar edição"):
                    avaliacao.nota = new_nota
                    avaliacao.comentario = new_comentario
                    st.success("Avaliação editada com sucesso!")

        with col2:
            if st.button(f"Excluir {i}"):
                st.session_state["avaliacoes"].pop(i)
                st.success(f"Avaliação de {avaliacao.cliente.nome} excluída com sucesso!")

######################################
# Lógica de navegação - Reservas
######################################
if st.session_state["option"] == "Reservas":
    st.subheader("Reservas")

    # Formulário para cadastrar uma reserva
    with st.form("cadastro_reserva"):
        st.subheader("Fazer Nova Reserva")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        id_mesa = st.number_input("Número da Mesa", min_value=1, step=1)
        data_reserva = st.date_input("Data da Reserva")
        hora_reserva = st.time_input("Hora da Reserva")
        submitted = st.form_submit_button("Reservar")
        if submitted:
            cliente = next((c for c in st.session_state["clientes"] if c.id == id_cliente), None)
            mesa = next((m for m in st.session_state["mesas"] if m.numero == id_mesa), None)
            if cliente and mesa:
                try:
                    reserva = Reserva(cliente, mesa, datetime.combine(data_reserva, hora_reserva))
                    st.session_state["reservas"].append(reserva)
                    st.success("Reserva realizada com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao fazer reserva: {e}")
            else:
                st.error("Cliente ou mesa não encontrados. Verifique os IDs.")
    
    # Exibir reservas realizadas
    st.subheader("Reservas Confirmadas")
    for i, reserva in enumerate(st.session_state["reservas"]):
        st.write(f"Cliente: {reserva.cliente.nome}, Mesa: {reserva.mesa.numero}, Data e Hora: {reserva.data}")
        
        # Editar e excluir reserva
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"Editar {i}"):
                # Formulário de edição
                new_data = st.date_input("Nova data da reserva", value=reserva.data.date())
                new_hora = st.time_input("Nova hora da reserva", value=reserva.data.time())
                if st.button("Confirmar edição"):
                    reserva.data = datetime.combine(new_data, new_hora)
                    st.success("Reserva editada com sucesso!")

        with col2:
            if st.button(f"Excluir {i}"):
                st.session_state["reservas"].pop(i)
                st.success(f"Reserva de {reserva.cliente.nome} excluída com sucesso!")

######################################
# Rodapé
######################################
st.sidebar.markdown("---")
st.sidebar.write("Sistema de gerenciamento de restaurante desenvolvido com Streamlit.")
st.sidebar.write("Criado para facilitar a administração de clientes, funcionários, mesas, pedidos e mais.")

st.write("---")
st.write("© 2025 Restaurante Cachorro Belga. Todos os direitos reservados.")
