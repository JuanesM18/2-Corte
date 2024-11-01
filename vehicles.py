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
        return connection
    except Error as e:
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

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

def insert_vehicles_from_dataframe(df):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO vehicles (reference, year, engine_capacity, brand, price)
                   VALUES (%s, %s, %s, %s, %s)"""
        try:
            for _, row in df.iterrows():
                cursor.execute(query, (row['reference'], row['year'], row['engine_capacity'], row['brand'], row['price']))
            connection.commit()
            st.success("¡Vehículos insertados exitosamente desde el archivo!")
        except Error as e:
            st.error(f"Error al insertar vehículos desde el archivo: {e}")
        finally:
            cursor.close()
            connection.close()

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

def vehicles_interface():
    st.title("Gestión de Vehículos")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar vehículos", "Cargar vehículos desde Excel", "Consultar vehículos"])

    if option == "Insertar vehículos":
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
    
    elif option == "Cargar vehículos desde Excel":
        st.header("Cargar vehículos desde un archivo Excel")
        uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            required_columns = ['reference', 'year', 'engine_capacity', 'brand', 'price']
            if all(column in df.columns for column in required_columns):
                insert_vehicles_from_dataframe(df)
            else:
                st.error("El archivo debe contener las columnas: 'reference', 'year', 'engine_capacity', 'brand', 'price'.")
    
    elif option == "Consultar vehículos":
        st.header("Consultar vehículos")
        vehicles = get_vehicles()
        if vehicles:
            st.write(vehicles)
        else:
            st.info("No hay vehículos registrados.")
