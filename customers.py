import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
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
        if connection.is_connected():
            st.write("Conexión establecida con la base de datos.")
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

def insert_customers_from_dataframe(df):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO customers (name, identification_number, email, phone)
                   VALUES (%s, %s, %s, %s)"""
        try:
            for _, row in df.iterrows():
                cursor.execute(query, (row['name'], row['identification_number'], row['email'], row['phone']))
            connection.commit()
            st.success("¡Clientes insertados exitosamente desde el archivo!")
        except Error as e:
            st.error(f"Error al insertar clientes desde el archivo: {e}")
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
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar cliente", "Cargar clientes desde Excel", "Consultar clientes"])

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
    
    elif option == "Cargar clientes desde Excel":
        st.header("Cargar clientes desde un archivo Excel")
        uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            required_columns = ['name', 'identification_number', 'email', 'phone']
            if all(column in df.columns for column in required_columns):
                insert_customers_from_dataframe(df)
            else:
                st.error("El archivo debe contener las columnas: 'name', 'identification_number', 'email', 'phone'.")
    
    elif option == "Consultar clientes":
        st.header("Consultar clientes")
        customers = get_customers()
        if customers:
            st.write(customers)
        else:
            st.info("No hay clientes registrados.")
