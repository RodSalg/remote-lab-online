import streamlit as st
import pymysql
import pandas as pd
from dotenv import load_dotenv
import os


db_config = {
    "host": st.secrets["DB_HOST"],
    "port": int(st.secrets["DB_PORT"]),
    "user": st.secrets["DB_USER"],
    "password": st.secrets["DB_PASSWORD"],
    "database": st.secrets["DB_NAME"],
    "ssl": {"ssl": {}},
    "charset": 'utf8mb4',
    "cursorclass": pymysql.cursors.DictCursor
}


st.markdown("<h1 style='text-align: center;'>LABORATÓRIO REMOTO</h1>", unsafe_allow_html=True)

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
