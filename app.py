import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import linprog

st.set_page_config(page_title="Otimizador de Liga Metálica", layout="centered")
st.title("🔩 Otimizador de Carga de Liga Metálica")

st.markdown("""
Este aplicativo calcula a composição ideal de uma liga metálica de aproximadamente 100 kg,
minimizando o custo e respeitando as faixas de composição química desejadas.
""")

massa_total = st.number_input("Massa total da liga (kg):", min_value=1.0, value=100.0, step=1.0)

st.subheader("📦 Cadastro de Materiais")
num_materiais = st.number_input("Quantos materiais deseja cadastrar?", min_value=1, max_value=20, value=4)

materiais = []
elementos = ["C", "Si", "Mn", "Cr", "Ni", "Mo", "Cu"]

for i in range(num_materiais):
    with st.expander(f"Material #{i+1}"):
        nome = st.text_input(f"Nome do material {i+1}", key=f"nome_{i}")
        tipo = st.selectbox(f"Tipo do material {i+1}", ["sucata", "metal_puro"], key=f"tipo_{i}")
        custo = st.number_input(f"Custo por kg (R$) {i+1}", min_value=0.0, value=10.0, key=f"custo_{i}")
        composicao = {}
        for el in elementos:
            composicao[el] = st.number_input(f"{el} (%) - Material {i+1}", min_value=0.0, max_value=100.0, value=0.0, key=f"{el}_{i}")
        fe = 100 - sum(composicao.values())
        composicao["Fe"] = max(fe, 0.0)
        materiais.append({"nome": nome, "tipo": tipo, "custo": custo, **composicao})

st.subheader("⚗️ Limites da Composição da Liga-Alvo (%)")
limites = {}
for el in elementos:
    col1, col2 = st.columns(2)
    with col1:
        minimo = st.number_input(f"{el} mínimo (%)", min_value=0.0, value=0.0, key=f"min_{el}")
    with col2:
        maximo = st.number_input(f"{el} máximo (%)", min_value=0.0, value=5.0, key=f"max_{el}")
    limites[el] = (minimo, maximo)

if st.button("Calcular Otimização"):
    nomes = [m["nome"] for m in materiais]
    custos = [m["custo"] for m
