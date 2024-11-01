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

def insert_employee(name, identification_number):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO employees (name, identification_number) VALUES (%s, %s)"""
        try:
            cursor.execute(query, (name, identification_number))
            connection.commit()
            st.success("¡Empleado insertado exitosamente!")
        except Error as e:
            st.error(f"Error al insertar el empleado: {e}")
        finally:
            cursor.close()
            connection.close()

def get_employees():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM employees"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            st.error(f"Error al consultar empleados: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

def employees_interface():
    st.title("Gestión de Empleados")
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar empleado", "Consultar empleados"])

    if option == "Insertar empleado":
        st.header("Insertar un empleado")
        name = st.text_input("Nombre")
        identification_number = st.text_input("Número de Identificación")
        
        if st.button("Insertar empleado"):
            if name and identification_number:
                insert_employee(name, identification_number)
            else:
                st.warning("Por favor, completa los campos requeridos.")
    
    elif option == "Consultar empleados":
        st.header("Consultar empleados")
        employees = get_employees()
        if employees:
            st.write(employees)
        else:
            st.info("No hay empleados registrados.")
