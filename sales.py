# sales.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
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

# Función para consultar datos de la tabla de ventas
def get_sales():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT sale_id FROM sales"  # Solo obtenemos los IDs de ventas
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error al consultar ventas: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

# Interfaz de Streamlit para ventas
def sales_interface():
    st.title("Gestión de Ventas")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar ventas", "Consultar ventas"])

    if option == "Insertar ventas":
        st.header("Insertar Ventas")
        st.write("Ingresa los datos de la venta.")

        # Campos para ingresar datos de la venta
        customer_id = st.number_input("ID del Cliente", min_value=1)
        vehicle_id = st.number_input("ID del Vehículo", min_value=1)
        sale_date = st.date_input("Fecha de venta")
        total_price = st.number_input("Precio total", min_value=0.0, format="%.2f")

        if st.button("Insertar Venta"):
            insert_sales_bulk([(customer_id, vehicle_id, sale_date, total_price)])

    elif option == "Consultar ventas":
        st.header("Consultar Ventas")
        sales = get_sales()
        if sales:
            st.write(sales)
        else:
            st.info("No hay ventas registradas.")

# Función para insertar ventas en bulk
def insert_sales_bulk(data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "INSERT INTO sales (customer_id, vehicle_id, sale_date, total_price) VALUES (%s, %s, %s, %s)"
        try:
            cursor.executemany(query, data)
            connection.commit()
            st.success("Ventas insertadas exitosamente.")
        except Error as e:
            st.error(f"Error al insertar ventas: {e}")
        finally:
            cursor.close()
            connection.close()
