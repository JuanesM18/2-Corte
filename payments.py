import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from sales import get_sales
import os
import pandas as pd

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

def insert_payments_bulk(payments):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO payments (sale_id, payment_date, amount, payment_method)
                   VALUES (%s, %s, %s, %s)"""
        try:
            cursor.executemany(query, payments)
            connection.commit()
            st.success("¡Pagos insertados exitosamente!")
        except Error as e:
            st.error(f"Error al insertar los pagos: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_payments_from_dataframe(df):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO payments (sale_id, payment_date, amount, payment_method)
                   VALUES (%s, %s, %s, %s)"""
        try:
            for _, row in df.iterrows():
                cursor.execute(query, (row['sale_id'], row['payment_date'], row['amount'], row['payment_method']))
            connection.commit()
            st.success("¡Pagos insertados exitosamente desde el archivo!")
        except Error as e:
            st.error(f"Error al insertar pagos desde el archivo: {e}")
        finally:
            cursor.close()
            connection.close()

def get_payments():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM payments"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error al consultar pagos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

def payments_interface():
    st.title("Gestión de Pagos")

    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar pagos", "Cargar pagos desde Excel", "Consultar pagos"])

    if option == "Insertar pagos":
        st.header("Insertar Pagos")
        st.write("Ingresa los datos del pago.")

        sales = get_sales()
        sale_ids = [sale['sale_id'] for sale in sales]
        sale_id = st.selectbox("Selecciona una venta", sale_ids)

        payment_date = st.date_input("Fecha de pago")
        amount = st.number_input("Monto", min_value=0.0, format="%.2f")
        payment_method = st.text_input("Método de pago")

        if st.button("Insertar Pago"):
            if payment_method:
                insert_payments_bulk([(sale_id, payment_date, amount, payment_method)])
            else:
                st.warning("Por favor, completa todos los campos requeridos.")

    elif option == "Cargar pagos desde Excel":
        st.header("Cargar Pagos desde un archivo Excel")
        uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            required_columns = ['sale_id', 'payment_date', 'amount', 'payment_method']
            if all(column in df.columns for column in required_columns):
                insert_payments_from_dataframe(df)
            else:
                st.error("El archivo debe contener las columnas: 'sale_id', 'payment_date', 'amount', 'payment_method'.")

    elif option == "Consultar pagos":
        st.header("Consultar Pagos")
        payments = get_payments()
        if payments:
            st.write(payments)
        else:
            st.info("No hay pagos registrados.")
