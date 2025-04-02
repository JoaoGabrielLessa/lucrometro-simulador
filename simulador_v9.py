
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Simulador Lucrometro", layout="centered")
st.title("🧮 Simulador Express - Lucrometro")

if "historico" not in st.session_state:
    st.session_state.historico = []

st.markdown("Bem-vindo ao Simulador Lucrometro! Aqui você entende para onde está indo o dinheiro da sua operação de e-commerce.")

# Bloco 1: Produto
st.markdown("### 🧱 Passo 1: Sobre o seu produto")
with st.expander("📦 Informe os dados do seu produto e sua meta de vendas"):
    col1 = st.columns(1)[0]
    with col1:
        preco_produto = st.number_input("💵 Preço médio do produto (R$)", min_value=0.0, value=500.0, step=10.0)
        quantidade_produtos = st.number_input("📦 Quantidade de produtos vendidos", min_value=0, value=1000, step=10)
    

faturamento = preco_produto * quantidade_produtos

# Bloco 2: Custos fixos
st.markdown("### 🏠 Passo 2: Custos Fixos")
with st.expander("💼 Informe seus custos fixos mensais"):
    custo_fixo_total = st.number_input("Custos Fixos mensais (R$)", min_value=0.0, value=100000.0, step=1000.0)

# Bloco 3: Custos variáveis
st.markdown("### 💸 Passo 2: Custos variáveis da sua operação")
with st.expander("🧾 Configure os percentuais dos seus principais custos variáveis"):
    col3, col4, col5 = st.columns(3)
    with col3:
        pct_envio = st.slider("📦 Envio (%)", 0, 100, 20)
    with col4:
        pct_taxas = st.slider("💳 Taxas & Tarifas (%)", 0, 100, 10)
    with col5:
        pct_impostos = st.slider("📄 Impostos (%)", 0, 100, 20)

    st.markdown("#### 🧪 Insumos")
    tipo_insumo = st.radio("Como você quer inserir o custo de insumos?", ["Valor absoluto (R$)", "Percentual sobre faturamento (%)"])
    if tipo_insumo == "Valor absoluto (R$)":
        insumos = st.number_input("Insumos (R$)", min_value=0.0, value=50000.0, step=1000.0)
    else:
        pct_insumos = st.slider("Insumos (%)", 0, 100, 10)
        insumos = faturamento * pct_insumos / 100

# Calcular e salvar histórico
if st.button("🔍 Calcular"):
    envio = faturamento * pct_envio / 100
    taxas = faturamento * pct_taxas / 100
    impostos = faturamento * pct_impostos / 100
    total_variaveis = insumos + envio + taxas + impostos
    margem_contribuicao = faturamento - total_variaveis
    lucro_liquido = margem_contribuicao - custo_fixo_total
    percentual_lucro = (lucro_liquido / faturamento) * 100 if faturamento > 0 else 0

    st.markdown("### 📊 Resultados da Simulação")

    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento", f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("Custos Variáveis", f"R$ {total_variaveis:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col3.metric("Custos Fixos", f"R$ {custo_fixo_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    col4, col5 = st.columns(2)
    col4.metric("Lucro Final", f"R$ {lucro_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), f"{percentual_lucro:.1f}%")
    col5.metric("Situação", "✅ Lucro" if lucro_liquido >= 0 else "❌ Prejuízo")

    # Tabela de composição
    st.markdown("### 📋 Composição da operação:")
    composicao = {
        "Item": [
            "Faturamento",
            "Insumos",
            "Envio",
            "Taxas",
            "Impostos",
            "Custos Fixos",
            "Lucro Final"
        ],
        "Valor (R$)": [
            faturamento,
            insumos,
            envio,
            taxas,
            impostos,
            custo_fixo_total,
            lucro_liquido
        ],
        "% sobre faturamento": [
            100.0,
            (insumos / faturamento) * 100 if faturamento > 0 else 0,
            (envio / faturamento) * 100 if faturamento > 0 else 0,
            (taxas / faturamento) * 100 if faturamento > 0 else 0,
            (impostos / faturamento) * 100 if faturamento > 0 else 0,
            (custo_fixo_total / faturamento) * 100 if faturamento > 0 else 0,
            (lucro_liquido / faturamento) * 100 if faturamento > 0 else 0,
        ]
    }

    df_comp = pd.DataFrame(composicao)
    df_comp["% sobre faturamento"] = df_comp["% sobre faturamento"].map(lambda x: f"{x:.1f}%")

    def format_color(val):
        try:
            if "R$" in str(val):
                num = float(val.replace("R$", "").replace(".", "").replace(",", "."))
                if num < 0:
                    return "color: red"
        except:
            pass
        return ""

    df_comp["Valor (R$)"] = df_comp["Valor (R$)"].map(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    st.dataframe(df_comp.style.applymap(format_color, subset=["Valor (R$)"]), use_container_width=True)

    # Salvar histórico
    st.session_state.historico.append({
        "Faturamento": faturamento,
        "Insumos": insumos,
        "Envio": envio,
        "Taxas": taxas,
        "Impostos": impostos,
        "Custos Variáveis": total_variaveis,
        "Custos Fixos": custo_fixo_total,
        "Lucro Final": lucro_liquido,
        "% Lucro": percentual_lucro
    })

# Bloco de histórico e compartilhamento
if st.session_state.historico:
    st.markdown("### 🧾 Histórico de Simulações")

    df_hist = pd.DataFrame(st.session_state.historico)
    df_hist_display = df_hist.copy()
    for col in df_hist.columns:
        if col != "% Lucro":
            df_hist_display[col] = df_hist[col].map(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        else:
            df_hist_display[col] = df_hist[col].map(lambda x: f"{x:.1f}%")

    st.dataframe(df_hist_display, use_container_width=True)

    # Exportar para Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_hist.to_excel(writer, index=False, sheet_name='Simulações')
    st.download_button(
        label="📥 Exportar simulações para Excel",
        data=buffer.getvalue(),
        file_name="simulacoes_lucrometro.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")
    st.markdown("🎉 Curtiu o simulador? Compartilhe com seus colegas:")
    wa_url = "https://wa.me/?text=Testei%20o%20Simulador%20Lucrometro%20e%20recomendo!%20Acesse%20aqui:%20https://lucrometro.streamlit.app"
    st.markdown(f"[📲 Compartilhar no WhatsApp]({wa_url})", unsafe_allow_html=True)
