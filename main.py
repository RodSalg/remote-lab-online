import streamlit as st
import pymysql
import pandas as pd
from dotenv import load_dotenv
import base64

load_dotenv()

def get_env_var(key):
    if key in st.secrets:
        return st.secrets[key]

db_config = {
    "host": get_env_var("DB_HOST"),
    "port": int(get_env_var("DB_PORT")),
    "user": get_env_var("DB_USER"),
    "password": get_env_var("DB_PASSWORD"),
    "database": get_env_var("DB_NAME"),
    "ssl": {"ssl": {}},
    "charset": 'utf8mb4',
    "cursorclass": pymysql.cursors.DictCursor
}


# Cabeçalho
st.markdown("<h1 style='text-align: center;'>LABORATÓRIO REMOTO</h1>", unsafe_allow_html=True)

# 🔹 Primeiro bloco: dadoscoletados2
try:
    conn = pymysql.connect(**db_config)
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT experimentName, experiment_id, step, pulse_train, pulse_value, timeToChange, time_stamp
            FROM dadoscoletados2;
        """)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Erro ao consultar dadoscoletados2: {e}")

# 🔹 Segundo bloco: imagem
st.markdown("<h1 style='text-align: center;'>IMAGEM CAPTURADA</h1>", unsafe_allow_html=True)

try:
    conn = pymysql.connect(**db_config)
    with conn.cursor() as cursor:
        cursor.execute("SELECT imagem_base64 FROM image WHERE id = 1")
        result = cursor.fetchone()

        if result and result["imagem_base64"]:
            image_bytes = base64.b64decode(result["imagem_base64"])
            st.image(image_bytes, caption="Imagem da planta (ID 1)", use_column_width=True)
        else:
            st.warning("Nenhuma imagem encontrada com ID 1.")
except Exception as e:
    st.error(f"Erro ao carregar imagem: {e}")