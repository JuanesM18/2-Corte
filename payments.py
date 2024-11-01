# payments.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from sales import get_sales
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener los parámetros de conexión desde las variables de entorno
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Conectar a la base de datos MySQL
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

# Función para insertar múltiples pagos en la tabla payments
def insert_payments_bulk(payments):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO payments (sale_id, payment_date, amount, payment_method)
                   VALUES (%s, %s, %s, %s)"""
        try:
            cursor.executemany(query, payments)  # Insertar en bulk
            connection.commit()
            st.success("¡Pagos insertados exitosamente!")
        except Error as e:
            st.error(f"Error al insertar los pagos: {e}")
        finally:
            cursor.close()
            connection.close()

# Función para consultar datos de la tabla de pagos
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

# Interfaz de Streamlit
def payments_interface():
    st.title("Gestión de Pagos")

    # Selección de operación
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar pagos", "Consultar pagos"])

    if option == "Insertar pagos":
        st.header("Insertar Pagos")
        st.write("Ingresa los datos del pago.")

        # Obtener ventas para el menú desplegable
        sales = get_sales()  # Suponiendo que tienes esta función en sales.py
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

    elif option == "Consultar pagos":
        st.header("Consultar Pagos")
        payments = get_payments()
        if payments:
            st.write(payments)
        else:
            st.info("No hay pagos registrados.")
