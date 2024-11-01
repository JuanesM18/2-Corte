import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

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

def insert_customer(name, identification_number, email, phone):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO customers (name, identification_number, email, phone)
                   VALUES (%s, %s, %s, %s)"""
        try:
            cursor.execute(query, (name, identification_number, email, phone))
            connection.commit()
            st.success("¡Cliente insertado exitosamente!")
        except Error as e:
            st.error(f"Error al insertar el cliente: {e}")
        finally:
            cursor.close()
            connection.close()

def get_customers():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM customers"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error al consultar clientes: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

def customers_interface():
    st.title("Gestión de Clientes")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar cliente", "Consultar clientes"])

    if option == "Insertar cliente":
        st.header("Insertar un cliente")
        name = st.text_input("Nombre")
        identification_number = st.text_input("Número de Identificación")
        email = st.text_input("Correo Electrónico")
        phone = st.text_input("Teléfono")
        
        if st.button("Insertar cliente"):
            if name and identification_number:
                insert_customer(name, identification_number, email, phone)
            else:
                st.warning("Por favor, completa los campos requeridos.")
    
    elif option == "Consultar clientes":
        st.header("Consultar clientes")
        customers = get_customers()
        if customers:
            st.write(customers)
        else:
            st.info("No hay clientes registrados.")
