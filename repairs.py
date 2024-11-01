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

def insert_repairs_bulk(repairs_data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO repairs (vehicle_id, repair_date, description, cost, employee_id)
                   VALUES (%s, %s, %s, %s, %s)"""
        try:
            cursor.executemany(query, repairs_data)
            connection.commit()
            st.success("¡Reparaciones insertadas exitosamente!")
        except Error as e:
            st.error(f"Error al insertar las reparaciones: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_repairs_from_dataframe(df):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO repairs (vehicle_id, repair_date, description, cost, employee_id)
                   VALUES (%s, %s, %s, %s, %s)"""
        try:
            for _, row in df.iterrows():
                cursor.execute(query, (row['vehicle_id'], row['repair_date'], row['description'], row['cost'], row['employee_id']))
            connection.commit()
            st.success("¡Reparaciones insertadas exitosamente desde el archivo!")
        except Error as e:
            st.error(f"Error al insertar reparaciones desde el archivo: {e}")
        finally:
            cursor.close()
            connection.close()

def get_repairs():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM repairs"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error al consultar reparaciones: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

def repairs_interface():
    st.title("Gestión de Reparaciones")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar reparaciones", "Cargar reparaciones desde Excel", "Consultar reparaciones"])

    if option == "Insertar reparaciones":
        st.header("Insertar múltiples reparaciones")
        
        num_repairs = st.number_input("Número de reparaciones a insertar", min_value=1, step=1)
        repairs_data = []
        
        for i in range(num_repairs):
            st.subheader(f"Reparación {i+1}")
            vehicle_id = st.number_input(f"ID del vehículo para la reparación {i+1}", min_value=1, key=f"vehicle_id_{i}")
            repair_date = st.date_input(f"Fecha de reparación {i+1}", key=f"repair_date_{i}")
            description = st.text_area(f"Descripción de la reparación {i+1}", key=f"description_{i}")
            cost = st.number_input(f"Costo de la reparación {i+1}", min_value=0.0, format="%.2f", key=f"cost_{i}")
            employee_id = st.number_input(f"ID del empleado que realizó la reparación {i+1}", min_value=1, key=f"employee_id_{i}")
            
            if vehicle_id and repair_date and description and cost and employee_id:
                repairs_data.append((vehicle_id, repair_date, description, cost, employee_id))
        
        if st.button("Insertar reparaciones"):
            if repairs_data:
                insert_repairs_bulk(repairs_data)
            else:
                st.warning("Por favor, ingresa todos los datos requeridos para las reparaciones.")
    
    elif option == "Cargar reparaciones desde Excel":
        st.header("Cargar Reparaciones desde un archivo Excel")
        uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            required_columns = ['vehicle_id', 'repair_date', 'description', 'cost', 'employee_id']
            if all(column in df.columns for column in required_columns):
                insert_repairs_from_dataframe(df)
            else:
                st.error("El archivo debe contener las columnas: 'vehicle_id', 'repair_date', 'description', 'cost', 'employee_id'.")

    elif option == "Consultar reparaciones":
        st.header("Consultar reparaciones")
        repairs = get_repairs()
        if repairs:
            st.write(repairs)
        else:
            st.info("No hay reparaciones registradas.")
