import streamlit as st
import mysql.connector
import os

def queries_interface():
    query_option = st.sidebar.selectbox("Selecciona una consulta", [
        "Consulta 1: Máximo salario en Empleados",
        "Consulta 2: total de ventas y el precio promedio de cada vehículo vendido",
        "Consulta 3: Ventas por año (AVG)",
        "Consulta 4: Reparaciones recientes por vehículo (LEFT JOIN)",
        "Consulta 5: Precio mínimo de vehículos",
    ])

    if query_option == "Consulta 1: Máximo salario en Empleados":
        consulta_max_salario()
    elif query_option == "Consulta 2: Empleados con vehículos asignados":
        consulta_empleados_vehiculos()
    elif query_option == "Consulta 3: Ventas por año (AVG)":
        consulta_promedio_ventas()
    elif query_option == "Consulta 4: Reparaciones recientes por vehículo (LEFT JOIN)":
        consulta_reparaciones_vehiculos()
    elif query_option == "Consulta 5: Precio mínimo de vehículos":
        consulta_precio_minimo_vehiculos()

def consulta_max_salario():
    st.header("Consulta: Máximo salario en Empleados")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(salary) FROM employees")
        result = cursor.fetchone()
        st.write("El salario máximo es:", result[0])
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def consulta_empleados_vehiculos():
    st.header("Consulta: total de ventas y el precio promedio de cada vehículo vendido")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.brand, v.reference, COUNT(s.sale_id) AS total_sales, AVG(s.total_price) AS avg_price
            FROM vehicles v
            INNER JOIN sales s ON v.vehicle_id = s.vehicle_id
            GROUP BY v.vehicle_id;""")
        results = cursor.fetchall()
        st.write("total de ventas y el precio promedio de cada vehículo vendido:")
        for row in results:
            st.write(row)
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def consulta_promedio_ventas():
    st.header("Consulta: Promedio de ventas por año")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT YEAR(sale_date) AS year, AVG(total_price) AS average_price 
            FROM sales 
            GROUP BY year
        """)
        results = cursor.fetchall()
        st.write("Promedio de ventas por año:")
        for row in results:
            st.write(f"Año {row[0]}: {row[1]}")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def consulta_reparaciones_vehiculos():
    st.header("Consulta: Reparaciones recientes por vehículo (LEFT JOIN)")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT vehicles.reference, repairs.repair_date 
            FROM vehicles 
            LEFT JOIN repairs ON vehicles.vehicle_id = repairs.vehicle_id
        """)
        results = cursor.fetchall()
        st.write("Reparaciones recientes por vehículo:")
        for row in results:
            st.write(f"Vehículo {row[0]}: Última reparación el {row[1]}")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def consulta_precio_minimo_vehiculos():
    st.header("Consulta: Precio mínimo de vehículos")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(price) FROM vehicles")
        result = cursor.fetchone()
        st.write("El precio mínimo es:", result[0])
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def consulta_precio_minimo_vehiculos():
    st.header("Consulta: Precio mínimo de vehículos")
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT MIN(price) FROM vehicles")
        result = cursor.fetchone()
        st.write("El precio mínimo es:", result[0])
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()