# vehicles.py
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno y establecer conexión a la base de datos
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Función para crear la conexión a MySQL
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

# Función para insertar múltiples vehículos en bulk
def insert_vehicles_bulk(vehicles_data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO vehicles (reference, year, engine_capacity, brand, price)
                   VALUES (%s, %s, %s, %s, %s)"""
        try:
            cursor.executemany(query, vehicles_data)
            connection.commit()
            st.success("¡Vehículos insertados exitosamente!")
        except Error as e:
            st.error(f"Error al insertar los vehículos: {e}")
        finally:
            cursor.close()
            connection.close()

# Función para consultar todos los vehículos
def get_vehicles():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM vehicles"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error al consultar vehículos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

# Función de interfaz específica para la tabla 'vehicles'
def vehicles_interface():
    st.title("Gestión de Vehículos")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar vehículos en bulk", "Consultar vehículos"])

    if option == "Insertar vehículos en bulk":
        st.header("Insertar múltiples vehículos")
        
        num_vehicles = st.number_input("Número de vehículos a insertar", min_value=1, step=1)
        vehicles_data = []
        
        for i in range(num_vehicles):
            st.subheader(f"Vehículo {i+1}")
            reference = st.text_input(f"Referencia del vehículo {i+1}", key=f"reference_{i}")
            year = st.number_input(f"Año del vehículo {i+1}", min_value=1900, max_value=2100, step=1, key=f"year_{i}")
            engine_capacity = st.number_input(f"Cilindraje del vehículo {i+1}", key=f"engine_capacity_{i}")
            brand = st.text_input(f"Marca del vehículo {i+1}", key=f"brand_{i}")
            price = st.number_input(f"Precio del vehículo {i+1}", key=f"price_{i}")
            
            if reference and year and engine_capacity and brand and price:
                vehicles_data.append((reference, year, engine_capacity, brand, price))
        
        if st.button("Insertar vehículos"):
            if vehicles_data:
                insert_vehicles_bulk(vehicles_data)
            else:
                st.warning("Por favor, ingresa todos los datos requeridos para los vehículos.")
    
    elif option == "Consultar vehículos":
        st.header("Consultar vehículos")
        vehicles = get_vehicles()
        if vehicles:
            st.write(vehicles)
        else:
            st.info("No hay vehículos registrados.")
