
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lucrometro - Simulador", layout="centered")
st.title("🧮 Simulador de Precificação Lucrometro v11.5")

st.markdown("Preencha os campos abaixo para simular a estrutura financeira do seu negócio com clareza.")

def format_brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Bloco 1 - Produto e Faturamento
with st.container():
    st.header("📦 Passo 1: Produto e Faturamento")

    col1, col2 = st.columns(2)
    with col1:
        preco_produto = st.number_input("Preço do produto (R$)", value=500.00, step=10.0)
    with col2:
        qtd_produtos = st.number_input("Quantidade de produtos vendidos", value=1000, step=10)

    faturamento = preco_produto * qtd_produtos
    st.success(f"Faturamento estimado: {format_brl(faturamento)}")

# Bloco 2 - Custos Variáveis
with st.container():
    st.header("💸 Passo 2: Custos Variáveis")

    col3, col4 = st.columns(2)
    with col3:
        envio_pct = st.slider("% de envio sobre faturamento", 0, 100, 20)
        taxas_pct = st.slider("% de taxas e tarifas sobre faturamento", 0, 100, 10)
    with col4:
        impostos_pct = st.slider("% de impostos sobre faturamento", 0, 100, 20)
        insumos_pct = st.slider("% de insumos sobre faturamento", 0, 100, 6)

    envio = faturamento * envio_pct / 100
    taxas = faturamento * taxas_pct / 100
    impostos = faturamento * impostos_pct / 100
    insumos = faturamento * insumos_pct / 100
    total_custos_variaveis = envio + taxas + impostos + insumos

    st.info(f"Custo variável total: {format_brl(total_custos_variaveis)}")

# Bloco 3 - Custos Fixos
with st.container():
    st.header("🏠 Passo 3: Custos Fixos")
    custos_fixos = st.number_input("Total de custos fixos (R$)", value=100000.0, step=100.0)

# Resultados
st.markdown("---")
st.header("📈 Resultado")

col5, col6 = st.columns(2)
with col5:
    st.metric("Faturamento", format_brl(faturamento))
    st.metric("Custos Variáveis", format_brl(total_custos_variaveis))
    st.metric("Custos Fixos", format_brl(custos_fixos))
with col6:
    margem = faturamento - total_custos_variaveis
    lucro = margem - custos_fixos
    lucro_status = "🟢 Lucro" if lucro >= 0 else "🔴 Prejuízo"

    st.metric("Margem de Contribuição", format_brl(margem))

    html_block = f'''
        <div style="background-color:#f1f1f1; padding:15px; border-radius:10px; margin-top:10px;">
            <h3 style="margin-bottom:10px;">Lucro Final</h3>
            <p style="font-size:28px; color:{'#2e7d32' if lucro >= 0 else '#c62828'}; margin:0;">
                <strong>{format_brl(lucro)}</strong>
            </p>
            <p style="font-size:18px; margin-top:8px;">
                <strong>Status:</strong> {lucro_status}
            </p>
        </div>
    '''
    st.markdown(html_block, unsafe_allow_html=True)

# Nova Tabela Estilo v9 - Resumo Completo com valores formatados
st.markdown("---")
st.subheader("📊 Resumo Financeiro da Simulação")

dados = {
    "Categoria": ["Faturamento", "Insumos", "Envio", "Taxas", "Impostos", "Custo Fixo", "Lucro"],
    "Tipo": ["Receita", "Despesa", "Despesa", "Despesa", "Despesa", "Despesa", "Lucro"],
    "Valor (R$)": list(map(format_brl, [faturamento, insumos, envio, taxas, impostos, custos_fixos, lucro]))
}
df = pd.DataFrame(dados)

def highlight_tipo(val):
    if val == "Despesa":
        return "color: red;"
    elif val == "Lucro":
        return "color: green;"
    elif val == "Receita":
        return "color: blue;"
    return ""

st.dataframe(df.style.applymap(highlight_tipo, subset=["Tipo"]), use_container_width=True)

# Histórico de simulações
st.markdown("---")
st.subheader("📁 Histórico de Simulações (sessão atual)")
if "historico" not in st.session_state:
    st.session_state.historico = []

if st.button("Salvar Simulação Atual"):
    st.session_state.historico.append({
        "Preço Produto": preco_produto,
        "Qtd": qtd_produtos,
        "Faturamento": faturamento,
        "Envio": envio,
        "Taxas": taxas,
        "Impostos": impostos,
        "Insumos": insumos,
        "Custos Fixos": custos_fixos,
        "Lucro": lucro
    })

if st.session_state.historico:
    df_hist = pd.DataFrame(st.session_state.historico)
    st.dataframe(df_hist, use_container_width=True)

    st.download_button("📥 Baixar simulações em Excel", data=df_hist.to_csv(index=False).encode('utf-8'),
                       file_name="simulacoes_lucrometro.csv", mime="text/csv")

st.markdown("---")
st.markdown("💡 **Dica:** A Margem de Contribuição mostra o quanto sobra para cobrir os custos fixos. O lucro aparece apenas se a margem for maior que os custos fixos. Use o Lucrometro para testar variações de preço, volume e estrutura de custos.")
