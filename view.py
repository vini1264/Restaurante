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
    controller.adicionar_mesa(1, 1, 4)

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

elif st.session_state["option"] == "Clientes":
    # Formulário para cadastrar um novo cliente
    with st.form("cadastro_cliente"):
        st.subheader("Cadastrar Novo Cliente")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        nome_cliente = st.text_input("Nome do Cliente")
        telefone_cliente = st.text_input("Telefone do Cliente")

        submitted = st.form_submit_button("Cadastrar")

        if submitted:
            st.write("Botão de cadastro clicado")
            st.write(f"id_cliente: {id_cliente}, nome_cliente: {nome_cliente}, telefone_cliente: {telefone_cliente}")
            if id_cliente and nome_cliente and telefone_cliente:
                st.write("Todos os campos foram preenchidos")
                if any(c.id == id_cliente for c in restaurante.clientes):
                    st.warning("Já existe um cliente com esse ID.")
                else:
                    try:
                        st.write("Cadastrando cliente...")
                        controller.cadastrar_cliente(id_cliente, nome_cliente, telefone_cliente)
                        st.success(f"Cliente {nome_cliente} cadastrado com sucesso!")
                        st.write(f"Clientes antes do cadastro: {len(restaurante.clientes)}")
                        restaurante.clientes.append(Cliente(id_cliente, nome_cliente, telefone_cliente))
                        st.write(f"Clientes depois do cadastro: {len(restaurante.clientes)}")
                        st.write("Recarregando a página...")
                        st.rerun()  # Atualiza a página automaticamente após o cadastro
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao cadastrar o cliente: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    st.subheader("Clientes Cadastrados")
    for cliente in restaurante.clientes:
        st.write(cliente.get_info())
    st.write("Total de clientes cadastrados: ", len(restaurante.clientes))

elif st.session_state["option"] == "Funcionários":
    st.subheader("Funcionários")
    for f in restaurante.funcionarios:
        st.write(f"{f.nome} - Cargo: {f.cargo}")

elif st.session_state["option"] == "Mesas":
    st.subheader("Mesas")
    for mesa in restaurante.mesas:
        status = "Ocupada" if mesa.ocupada else "Livre"
        st.write(f"Mesa {mesa.numero} - Capacidade: {mesa.capacidade} - {status}")

elif st.session_state["option"] == "Cardápio":
    st.subheader("Cardápio")
    if restaurante.cardapio:
        for prod in restaurante.cardapio.listar_produtos():
            st.write(prod)

elif st.session_state["option"] == "Pedidos":
    st.subheader("Pedidos")
    for pedido in restaurante.pedidos:
        st.write(f"{pedido.nome} - Total: R$ {pedido.calcular_total():.2f}")
        for item in pedido.listar_itens():
            st.write(f"  - {item}")

elif st.session_state["option"] == "Reservas":
    st.subheader("Reservas")
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
