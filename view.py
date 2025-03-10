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
    produto1 = Produto("Pizza", 35.0)
    produto2 = Produto("Refrigerante", 5.0)
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
    if restaurante.cardapio:
        for prod in restaurante.cardapio.listar_produtos():
            st.write(prod)

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

elif st.session_state["option"] == "Reservas":
    st.subheader("Reservas")

    # Formulário para criar uma reserva em uma mesa
    with st.form("criar_reserva"):
        st.subheader("Criar Reserva")
        id_reserva = st.number_input("ID da Reserva", min_value=1, step=1)
        id_cliente_reserva = st.number_input("ID do Cliente", min_value=1, step=1)
        numero_mesa_reserva = st.number_input("Número da Mesa para a Reserva", min_value=1, step=1)
        data_hora_reserva = st.date_input("Data e Hora da Reserva")
        submitted = st.form_submit_button("Criar Reserva")
        if submitted:
            try:
                cliente = next(c for c in restaurante.clientes if c.id == id_cliente_reserva)
                controller.criar_reserva(id_reserva, cliente, datetime.combine(data_hora_reserva, datetime.min.time()), numero_mesa_reserva)
                st.success(f"Reserva {id_reserva} criada com sucesso na mesa {numero_mesa_reserva}!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao criar a reserva: {e}")

    # Lista as reservas cadastradas
    for reserva in restaurante.reservas:
        st.write(reserva.exibir_reserva())

elif st.session_state["option"] == "Promoções":
    st.subheader("Promoções")
    if hasattr(restaurante, 'promocoes'):
        for promo in restaurante.promocoes:
            st.write(f"{promo.descricao} - Desconto: {promo.desconto}% - Validade: {promo.dataValidade}")
            for prod in promo.listar_produtos():
                st.write(f"  - {prod}")

elif st.session_state["option"] == "Avaliações":
    st.subheader("Avaliações")
    if hasattr(restaurante, 'avaliacoes'):
        for avaliacao in restaurante.avaliacoes:
            st.write(f"{avaliacao.cliente.nome} avaliou com nota {avaliacao.nota}: {avaliacao.comentario}")
