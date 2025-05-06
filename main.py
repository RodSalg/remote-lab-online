import streamlit as st
import pymysql
import pandas as pd
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configurações do banco via .env
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "ssl": {"ssl": {}},
    "charset": 'utf8mb4',
    "cursorclass": pymysql.cursors.DictCursor
}

# Título centralizado
st.markdown("<h1 style='text-align: center;'>LABORATÓRIO REMOTO</h1>", unsafe_allow_html=True)

# Consulta e exibição da tabela
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
    conn.close()
except Exception as e:
    st.error(f"Erro ao conectar ou consultar dados: {e}")
