# repairs.py
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

# Función para insertar múltiples reparaciones en bulk
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

# Función para consultar todas las reparaciones
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

# Función de interfaz específica para la tabla 'repairs'
def repairs_interface():
    st.title("Gestión de Reparaciones")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar reparaciones en bulk", "Consultar reparaciones"])

    if option == "Insertar reparaciones en bulk":
        st.header("Insertar múltiples reparaciones")
        
        num_repairs = st.number_input("Número de reparaciones a insertar", min_value=1, step=1)
        repairs_data = []
        
        for i in range(num_repairs):
            st.subheader(f"Reparación {i+1}")
            vehicle_id = st.number_input(f"ID del vehículo para la reparación {i+1}", min_value=1, key=f"vehicle_id_{i}")
            repair_date = st.date_input(f"Fecha de reparación {i+1}", key=f"repair_date_{i}")
            description = st.text_area(f"Descripción de la reparación {i+1}", key=f"description_{i}")
            cost = st.number_input(f"Costo de la reparación {i+1}", key=f"cost_{i}")
            employee_id = st.number_input(f"ID del empleado que realizó la reparación {i+1}", min_value=1, key=f"employee_id_{i}")
            
            if vehicle_id and repair_date and description and cost and employee_id:
                repairs_data.append((vehicle_id, repair_date, description, cost, employee_id))
        
        if st.button("Insertar reparaciones"):
            if repairs_data:
                insert_repairs_bulk(repairs_data)
            else:
                st.warning("Por favor, ingresa todos los datos requeridos para las reparaciones.")
    
    elif option == "Consultar reparaciones":
        st.header("Consultar reparaciones")
        repairs = get_repairs()
        if repairs:
            st.write(repairs)
        else:
            st.info("No hay reparaciones registradas.")
