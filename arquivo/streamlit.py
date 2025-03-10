import streamlit as st
from datetime import datetime

# Importação do código principal do restaurante
from projeto import Restaurante, RestauranteController, Produto, Cliente, Funcionario, Mesa, Cardapio, Pedido, Reserva, Promocao, Avaliacao

# Criação do objeto Restaurante central
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

# Interface com Streamlit
st.title("Sistema de Restaurante")

# Menu lateral
option = st.sidebar.selectbox("Selecione uma opção:",
                              ["Home", "Clientes", "Funcionários", "Mesas", "Cardápio",
                               "Pedidos", "Reservas", "Promoções", "Avaliações"])

if option == "Home":
    st.write("Bem-vindo ao sistema de restaurante!")
    st.write("Utilize o menu lateral para navegar entre as funcionalidades.")

elif option == "Clientes":
    st.subheader("Clientes Cadastrados")
    for cliente in restaurante.clientes:
        st.write(cliente.get_info())

elif option == "Funcionários":
    st.subheader("Funcionários")
    for f in restaurante.funcionarios:
        st.write(f"{f.nome} - Cargo: {f.cargo}")

elif option == "Mesas":
    st.subheader("Mesas")
    for mesa in restaurante.mesas:
        status = "Ocupada" if mesa.ocupada else "Livre"
        st.write(f"Mesa {mesa.numero} - Capacidade: {mesa.capacidade} - {status}")

elif option == "Cardápio":
    st.subheader("Cardápio")
    if restaurante.cardapio:
        for prod in restaurante.cardapio.listar_produtos():
            st.write(prod)

elif option == "Pedidos":
    st.subheader("Pedidos")
    for pedido in restaurante.pedidos:
        st.write(f"{pedido.nome} - Total: R$ {pedido.calcular_total():.2f}")
        for item in pedido.listar_itens():
            st.write(f"  - {item}")

elif option == "Reservas":
    st.subheader("Reservas")
    for reserva in restaurante.reservas:
        st.write(reserva.exibir_reserva())

elif option == "Promoções":
    st.subheader("Promoções")
    if hasattr(restaurante, 'promocoes'):
        for promo in restaurante.promocoes:
            st.write(f"{promo.descricao} - Desconto: {promo.desconto}% - Validade: {promo.dataValidade}")
            for prod in promo.listar_produtos():
                st.write(f"  - {prod}")

elif option == "Avaliações":
    st.subheader("Avaliações")
    if hasattr(restaurante, 'avaliacoes'):
        for avaliacao in restaurante.avaliacoes:
            st.write(f"{avaliacao.cliente.nome} avaliou com nota {avaliacao.nota}: {avaliacao.comentario}")
