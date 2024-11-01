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

def insert_employees_bulk(employees_data):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO employees (name, position, salary)
                   VALUES (%s, %s, %s)"""
        try:
            cursor.executemany(query, employees_data)
            connection.commit()
            st.success("¡Empleados insertados exitosamente!")
        except Error as e:
            st.error(f"Error al insertar los empleados: {e}")
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
        st.header("Insertar empleado")
        employee_data = []
        
        name = st.text_input("Nombre")
        position = st.text_input("Posición")
        salary = st.number_input("Salario", min_value=0.0, format="%.2f")
        
        if st.button("Insertar empleado"):
            if name and position:
                employee_data.append((name, position, salary))
                insert_employees_bulk(employee_data)
            else:
                st.warning("Por favor, completa los datos del empleado.")
    
    elif option == "Consultar empleados":
        st.header("Consultar empleados")
        employees = get_employees()
        if employees:
            st.write(employees)
        else:
            st.info("No hay empleados registrados.")
