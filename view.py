import streamlit as st
from datetime import datetime
from projeto import Restaurante, RestauranteController, Produto, Cliente, Funcionario, Mesa, Cardapio, Pedido, Reserva, Promocao, Avaliacao

# Tenta carregar os dados persistentes, se existentes; caso contrário, cria o restaurante
restaurante_carregado = RestauranteController.carregar_dados()
if restaurante_carregado is None:
    restaurante = Restaurante(1, "Restaurante Exemplo", "Rua Principal, 123")
    controller = RestauranteController(restaurante)
    try:
        controller.cadastrar_cliente(1, "João Silva", "123456789")
    except Exception:
        pass
    try:
        controller.cadastrar_funcionario(1, "Maria Souza", "987654321", "Garçom", 1500.0)
    except Exception:
        pass
    if not restaurante.mesas:
        try:
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
        except Exception:
            pass
    if restaurante.cardapio is None:
        cardapio = controller.definir_cardapio(1, "Cardápio do Restaurante Exemplo")
        produto1 = Produto("Pizza", 35.0, "Alimento")
        produto2 = Produto("Refrigerante", 5.0, "Bebida")
        cardapio.adicionar_produto(produto1)
        cardapio.adicionar_produto(produto2)
    controller.salvar_dados()
else:
    restaurante = restaurante_carregado
    controller = RestauranteController(restaurante)

if "option" not in st.session_state:
    st.session_state["option"] = "Home"

paginas = ["Home", "Clientes", "Funcionários", "Mesas", "Cardápio", "Pedidos", "Reservas", "Promoções", "Avaliações"]
if st.session_state["option"] not in paginas:
    st.session_state["option"] = "Home"

option_index = paginas.index(st.session_state["option"])
option = st.sidebar.selectbox("Selecione uma opção:", paginas, index=option_index)
if option != st.session_state["option"]:
    st.session_state["option"] = option
    st.stop()  # Substitui o st.experimental_rerun()

if st.session_state["option"] == "Home":
    st.title("Sistema de Restaurante")
    st.write("Bem-vindo ao sistema de restaurante!")
    st.write("Escolha abaixo a funcionalidade ou utilize o menu lateral.")

    st.image("https://blog.artdescaves.com.br/hubfs/blog/6-dicas-para-agradar-os-clientes-do-seu-restaurante.jpg")
    if st.button("Clientes"):
        st.session_state["option"] = "Clientes"
        st.experimental_rerun()

    st.image("https://www.menucontrol.com.br/wp-content/uploads/2022/05/group-hotel-staffs-standing-kitchen-scaled-1.jpg")
    if st.button("Funcionários"):
        st.session_state["option"] = "Funcionários"
        st.experimental_rerun()

    st.image("https://www.housecustomize.com/wp-content/uploads/2023/08/02-2-64ed9ce0773f5-1024x758.webp")
    if st.button("Mesas"):
        st.session_state["option"] = "Mesas"
        st.experimental_rerun()

    st.image("https://www.tribunapr.com.br/wp-content/uploads/2020/01/30161957/CARD%C3%81PIO-TECNICOPIAS-970x550.jpg")
    if st.button("Cardápio"):
        st.session_state["option"] = "Cardápio"
        st.experimental_rerun()

    st.image("https://img.elo7.com.br/product/zoom/502C0B7/bloco-de-pedidos-para-restaurantes-empresa.jpg")
    if st.button("Pedidos"):
        st.session_state["option"] = "Pedidos"
        st.experimental_rerun()

    st.image("https://cms-bomgourmet.s3.amazonaws.com/bomgourmet%2F2021%2F06%2F11152136%2Fmesa-reservada-foto-bigstock.jpg")
    if st.button("Reservas"):
        st.session_state["option"] = "Reservas"
        st.experimental_rerun()

    st.image("https://img.cdndsgni.com/preview/10034124.jpg")
    if st.button("Promoções"):
        st.session_state["option"] = "Promoções"
        st.experimental_rerun()

    st.image("https://static.vecteezy.com/ti/vetor-gratis/t1/11802277-modelo-de-avaliacao-de-restaurante-ilustracao-plana-de-desenho-animado-desenhado-a-mao-com-feedback-do-cliente-estrela-de-taxa-opiniao-de-especialistas-e-pesquisa-on-line-vetor.jpg")
    if st.button("Avaliações"):
        st.session_state["option"] = "Avaliações"
        st.experimental_rerun()

elif st.session_state["option"] == "Clientes":
    st.subheader("Clientes Cadastrados")
    with st.form("cadastro_cliente"):
        st.subheader("Cadastrar Novo Cliente")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        nome_cliente = st.text_input("Nome do Cliente")
        telefone_cliente = st.text_input("Telefone do Cliente")
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if id_cliente and nome_cliente and telefone_cliente:
                try:
                    controller.cadastrar_cliente(id_cliente, nome_cliente, telefone_cliente)
                    st.success(f"Cliente {nome_cliente} cadastrado com sucesso!")
                    controller.salvar_dados()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao cadastrar o cliente: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    
    for cliente in restaurante.clientes:
        st.write(cliente.get_info())
    st.write("Total de clientes cadastrados: ", len(restaurante.clientes))

elif st.session_state["option"] == "Funcionários":
    st.subheader("Funcionários")
    with st.form("cadastro_de_funcionario"):
        st.subheader("Cadastrar Novo Funcionário")
        id_funcionario = st.number_input("ID do Funcionário", min_value=1, step=1)
        nome_funcionario = st.text_input("Nome do Funcionário:")
        telefone_funcionario = st.text_input("Telefone do Funcionário:")
        cargo_funcionario = st.text_input("Cargo do Funcionário:")
        salario_funcionario = st.number_input("Salário do Funcionário", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Cadastrar")
        if submitted:
            if id_funcionario and nome_funcionario and telefone_funcionario:
                try:
                    controller.cadastrar_funcionario(id_funcionario, nome_funcionario, telefone_funcionario, cargo_funcionario, salario_funcionario)
                    st.success(f"Funcionário {nome_funcionario} cadastrado com sucesso!")
                    controller.salvar_dados()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao cadastrar o funcionário: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    
    st.subheader("Funcionários Cadastrados")
    st.write("ID - Nome - Telefone - Cargo - Salário")
    for funcionario in restaurante.funcionarios:
        st.write(funcionario.get_info())
    st.write("Total de funcionários cadastrados: ", len(restaurante.funcionarios))

elif st.session_state["option"] == "Mesas":
    st.subheader("Mesas")
    with st.form("liberar_mesa"):
        st.subheader("Liberar Mesa")
        numero_mesa_liberar = st.number_input("Número da Mesa para Liberar", min_value=1, step=1)
        submitted = st.form_submit_button("Liberar Mesa")
        if submitted:
            try:
                controller.liberar_mesa(numero_mesa_liberar)
                st.success(f"Mesa {numero_mesa_liberar} liberada com sucesso!")
                controller.salvar_dados()
            except Exception as e:
                st.error(f"Ocorreu um erro ao liberar a mesa: {e}")
    
    st.subheader("Mesas Cadastradas")
    for mesa in restaurante.mesas:
        status = "Ocupada" if mesa.ocupada else "Reservada" if mesa.reservada else "Livre"
        st.write(f"Mesa {mesa.numero} - Capacidade: {mesa.capacidade} - Status: {status}")

elif st.session_state["option"] == "Cardápio":
    st.subheader("Cardápio")
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
                    controller.salvar_dados()
                except Exception as e:
                    st.error(f"Ocorreu um erro ao adicionar o produto: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    
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
                controller.salvar_dados()
            except Exception as e:
                st.error(f"Ocorreu um erro ao criar o pedido: {e}")
    
    for pedido in restaurante.pedidos:
        st.write(f"{pedido.nome} - Total: R$ {pedido.calcular_total():.2f}")
        for item in pedido.listar_itens():
            st.write(f"  - {item}")

elif st.session_state["option"] == "Reservas":
    st.subheader("Reservas")
    with st.form("cadastro_reserva"):
        st.subheader("Fazer Nova Reserva")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        id_mesa = st.number_input("Número da Mesa", min_value=1, step=1)
        data_reserva = st.date_input("Data da Reserva")
        hora_reserva = st.time_input("Hora da Reserva")
        submitted = st.form_submit_button("Reservar")
        if submitted:
            try:
                cliente = next((c for c in restaurante.clientes if c.id == id_cliente), None)
                mesa = next((m for m in restaurante.mesas if m.numero == id_mesa), None)
                if cliente and mesa:
                    reserva_id = len(restaurante.reservas) + 1
                    data_hora = datetime.combine(data_reserva, hora_reserva)
                    controller.criar_reserva(reserva_id, cliente, data_hora, id_mesa)
                    st.success("Reserva realizada com sucesso!")
                    controller.salvar_dados()
                else:
                    st.error("Cliente ou mesa não encontrados. Verifique os IDs.")
            except Exception as e:
                st.error(f"Erro ao fazer reserva: {e}")
    
    st.subheader("Reservas Confirmadas")
    for reserva in restaurante.reservas:
        st.write(reserva.exibir_reserva())

elif st.session_state["option"] == "Promoções":
    st.subheader("Promoções")
    with st.form("cadastro_promocao"):
        st.subheader("Cadastrar Nova Promoção")
        titulo = st.text_input("Título da Promoção")
        descricao = st.text_area("Descrição da Promoção")
        desconto = st.number_input("Desconto (%)", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Cadastrar Promoção")
        if submitted:
            if titulo and descricao:
                try:
                    promocao_id = len(restaurante.promocoes) + 1
                    promocao = Promocao(promocao_id, titulo, descricao, desconto)
                    restaurante.promocoes.append(promocao)
                    st.success("Promoção cadastrada com sucesso!")
                    controller.salvar_dados()
                except Exception as e:
                    st.error(f"Erro ao cadastrar promoção: {e}")
            else:
                st.error("Preencha todos os campos corretamente.")
    
    st.subheader("Promoções Cadastradas")
    for promocao in restaurante.promocoes:
        st.write(f"**{promocao.titulo}**: {promocao.descricao} - Desconto: {promocao.desconto}%")

elif st.session_state["option"] == "Avaliações":
    st.subheader("Avaliações")
    with st.form("cadastro_avaliacao"):
        st.subheader("Cadastrar Nova Avaliação")
        id_cliente = st.number_input("ID do Cliente", min_value=1, step=1)
        nota = st.slider("Nota (1-5)", min_value=1, max_value=5, step=1)
        comentario = st.text_area("Comentário")
        submitted = st.form_submit_button("Enviar Avaliação")
        if submitted:
            try:
                cliente = next((c for c in restaurante.clientes if c.id == id_cliente), None)
                if cliente:
                    avaliacao_id = len(restaurante.avaliacoes) + 1
                    avaliacao = Avaliacao(avaliacao_id, cliente, nota, comentario)
                    restaurante.avaliacoes.append(avaliacao)
                    st.success("Avaliação registrada com sucesso!")
                    controller.salvar_dados()
                else:
                    st.error("Cliente não encontrado. Verifique o ID.")
            except Exception as e:
                st.error(f"Erro ao cadastrar avaliação: {e}")
    
    st.subheader("Avaliações dos Clientes")
    for avaliacao in restaurante.avaliacoes:
        st.write(f"{avaliacao.cliente.nome} avaliou com nota {avaliacao.nota}: {avaliacao.comentario}")

st.sidebar.markdown("---")
st.sidebar.write("Sistema de gerenciamento de restaurante desenvolvido com Streamlit.")
st.sidebar.write("Criado para facilitar a administração de clientes, funcionários, mesas, pedidos e mais.")

st.write("---")
st.write("© 2025 Restaurante Cachorro Belga. Todos os direitos reservados.")
