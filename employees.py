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

def insert_employee(name, position, salary):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO employees (name, position, salary)
                   VALUES (%s, %s, %s)"""
        try:
            cursor.execute(query, (name, position, salary))
            connection.commit()
            st.success("¡Empleado insertado exitosamente!")
        except Error as e:
            st.error(f"Error al insertar el empleado: {e}")
        finally:
            cursor.close()
            connection.close()

def insert_employees_from_dataframe(df):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """INSERT INTO employees (name, position, salary)
                   VALUES (%s, %s, %s)"""
        try:
            for _, row in df.iterrows():
                cursor.execute(query, (row['name'], row['position'], row['salary']))
            connection.commit()
            st.success("¡Empleados insertados exitosamente desde el archivo!")
        except Error as e:
            st.error(f"Error al insertar empleados desde el archivo: {e}")
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
    option = st.sidebar.selectbox("Selecciona una operación", ["Insertar empleado", "Cargar empleados desde Excel", "Consultar empleados"])

    if option == "Insertar empleado":
        st.header("Insertar un empleado")
        name = st.text_input("Nombre")
        position = st.text_input("Posición")
        salary = st.number_input("Salario", min_value=0.0, format="%.2f")
        
        if st.button("Insertar empleado"):
            if name and position:
                insert_employee(name, position, salary)
            else:
                st.warning("Por favor, completa los campos requeridos.")

    elif option == "Cargar empleados desde Excel":
        st.header("Cargar empleados desde un archivo Excel")
        uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            required_columns = ['name', 'position', 'salary']
            if all(column in df.columns for column in required_columns):
                insert_employees_from_dataframe(df)
            else:
                st.error("El archivo debe contener las columnas: 'name', 'position', 'salary'.")

    elif option == "Consultar empleados":
        st.header("Consultar empleados")
        employees = get_employees()
        if employees:
            st.write(employees)
        else:
            st.info("No hay empleados registrados.")
