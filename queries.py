import streamlit as st
import mysql.connector
import os
import pandas as pd

def queries_interface():
    query_option = st.sidebar.selectbox("Selecciona una consulta", [
        "Consulta 1: Máximo salario en Empleados",
        "Consulta 2: Total de ventas y precio promedio de cada vehículo vendido",
        "Consulta 3: Promedio de ventas por año",
        "Consulta 4: Reparaciones recientes por vehículo (LEFT JOIN)",
        "Consulta 5: Precio mínimo de vehículos",
        "Consulta 6: Mínimo y máximo precio de vehículos por marca",
        "Consulta 7: Ventas y pagos de cada cliente (INNER JOIN)",
        "Consulta 8: Vehículos sin reparaciones (RIGHT JOIN)",
        "Consulta 9: Total de pagos recibidos por año",
        "Consulta 10: Empleado que realizó la reparación más costosa",
        "Consulta 11: Cantidad de ventas realizadas por cliente",
        "Consulta 12: Cantidad de reparaciones realizadas por cada empleado",
        "Consulta 13: Vehículos y total gastado en reparaciones",
        "Consulta 14: Clientes que han realizado pagos (INNER JOIN)",
        "Consulta 15: Promedio de capacidad de motor por marca"
    ])

    if query_option == "Consulta 1: Máximo salario en Empleados":
        consulta_max_salario()
    elif query_option == "Consulta 2: Total de ventas y precio promedio de cada vehículo vendido":
        consulta_ventas_vehiculos()
    elif query_option == "Consulta 3: Promedio de ventas por año":
        consulta_promedio_ventas()
    elif query_option == "Consulta 4: Reparaciones recientes por vehículo (LEFT JOIN)":
        consulta_reparaciones_vehiculos()
    elif query_option == "Consulta 5: Precio mínimo de vehículos":
        consulta_precio_minimo_vehiculos()
    elif query_option == "Consulta 6: Mínimo y máximo precio de vehículos por marca":
        consulta_min_max_precio_vehiculos()
    elif query_option == "Consulta 7: Ventas y pagos de cada cliente (INNER JOIN)":
        consulta_ventas_pagos_cliente()
    elif query_option == "Consulta 8: Vehículos sin reparaciones (RIGHT JOIN)":
        consulta_vehiculos_sin_reparaciones()
    elif query_option == "Consulta 9: Total de pagos recibidos por año":
        consulta_pagos_por_anio()
    elif query_option == "Consulta 10: Empleado que realizó la reparación más costosa":
        consulta_empleado_reparacion_costosa()
    elif query_option == "Consulta 11: Cantidad de ventas realizadas por cliente":
        consulta_ventas_por_cliente()
    elif query_option == "Consulta 12: Cantidad de reparaciones realizadas por cada empleado":
        consulta_reparaciones_por_empleado()
    elif query_option == "Consulta 13: Vehículos y total gastado en reparaciones":
        consulta_total_reparaciones_vehiculo()
    elif query_option == "Consulta 14: Clientes que han realizado pagos (INNER JOIN)":
        consulta_clientes_con_pagos()
    elif query_option == "Consulta 15: Promedio de capacidad de motor por marca":
        consulta_promedio_capacidad_motor()

def execute_query(query, columns=None, message="Resultados:"):
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        if columns:
            df = pd.DataFrame(results, columns=columns)
            st.write(message)
            st.table(df)  
        else:
            if results and len(results) == 1 and len(results[0]) == 1:
                st.write(f"{message} {results[0][0]}")
            else:
                st.write(message)
                for row in results:
                    st.write(row)

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def consulta_max_salario():
    st.header("Consulta: Máximo salario en Empleados")
    execute_query("SELECT MAX(salary) FROM employees", message="El salario máximo es:")

def consulta_ventas_vehiculos():
    st.header("Consulta: Total de ventas y precio promedio de cada vehículo vendido")
    execute_query("""
        SELECT v.brand, v.reference, COUNT(s.sale_id) AS total_sales, AVG(s.total_price) AS avg_price
        FROM vehicles v
        INNER JOIN sales s ON v.vehicle_id = s.vehicle_id
        GROUP BY v.vehicle_id
    """, columns=["Marca", "Referencia", "Ventas Totales", "Precio Promedio"])

def consulta_promedio_ventas():
    st.header("Consulta: Promedio de ventas por año")
    execute_query("""
        SELECT YEAR(s.sale_date) AS year, AVG(s.total_price) AS average_price
        FROM sales s
        GROUP BY year
    """, columns=["Año", "Precio Promedio"])

def consulta_reparaciones_vehiculos():
    st.header("Consulta: Reparaciones recientes por vehículo (LEFT JOIN)")
    execute_query("""
        SELECT v.reference AS Vehículo, r.repair_date AS Fecha_Última_Reparación
        FROM vehicles v
        LEFT JOIN repairs r ON v.vehicle_id = r.vehicle_id
    """, columns=["Vehículo", "Fecha de Última Reparación"])

def consulta_precio_minimo_vehiculos():
    st.header("Consulta: Precio mínimo de vehículos")
    execute_query("SELECT MIN(price) FROM vehicles", message="El precio mínimo es:")

def consulta_min_max_precio_vehiculos():
    st.header("Consulta: Mínimo y máximo precio de vehículos por marca")
    execute_query("""
        SELECT brand, MIN(price) AS Min_Price, MAX(price) AS Max_Price
        FROM vehicles
        GROUP BY brand
    """, columns=["Marca", "Precio Mínimo", "Precio Máximo"])

def consulta_ventas_pagos_cliente():
    st.header("Consulta: Ventas y pagos de cada cliente (INNER JOIN)")
    execute_query("""
        SELECT c.name AS Cliente, COUNT(s.sale_id) AS Total_Ventas, SUM(p.amount) AS Total_Pagado
        FROM customers c
        INNER JOIN sales s ON c.customer_id = s.customer_id
        INNER JOIN payments p ON s.sale_id = p.sale_id
        GROUP BY c.customer_id
    """, columns=["Cliente", "Total Ventas", "Total Pagado"])

def consulta_vehiculos_sin_reparaciones():
    st.header("Consulta: Vehículos sin reparaciones (RIGHT JOIN)")
    execute_query("""
        SELECT v.reference AS Vehículo
        FROM repairs r
        RIGHT JOIN vehicles v ON r.vehicle_id = v.vehicle_id
        WHERE r.repair_id IS NULL
    """, columns=["Vehículo"])

def consulta_pagos_por_anio():
    st.header("Consulta: Total de pagos recibidos por año")
    execute_query("""
        SELECT YEAR(payment_date) AS Año, SUM(amount) AS Total_Pagos
        FROM payments
        GROUP BY Año
    """, columns=["Año", "Total Pagos"])

def consulta_empleado_reparacion_costosa():
    st.header("Consulta: Empleado que realizó la reparación más costosa")
    execute_query("""
        SELECT e.name AS Empleado, MAX(r.cost) AS Costo_Máximo
        FROM employees e
        JOIN repairs r ON e.employee_id = r.employee_id
        GROUP BY e.employee_id
        ORDER BY Costo_Máximo DESC LIMIT 1
    """, columns=["Empleado", "Costo Máximo"])

def consulta_ventas_por_cliente():
    st.header("Consulta: Cantidad de ventas realizadas por cliente")
    execute_query("""
        SELECT c.name AS Cliente, COUNT(s.sale_id) AS Ventas
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id
    """, columns=["Cliente", "Cantidad de Ventas"])

def consulta_reparaciones_por_empleado():
    st.header("Consulta: Cantidad de reparaciones realizadas por cada empleado")
    execute_query("""
        SELECT e.name AS Empleado, COUNT(r.repair_id) AS Reparaciones
        FROM employees e
        JOIN repairs r ON e.employee_id = r.employee_id
        GROUP BY e.employee_id
    """, columns=["Empleado", "Reparaciones"])

def consulta_total_reparaciones_vehiculo():
    st.header("Consulta: Vehículos y total gastado en reparaciones")
    execute_query("""
        SELECT v.reference AS Vehículo, SUM(r.cost) AS Total_Reparaciones
        FROM vehicles v
        JOIN repairs r ON v.vehicle_id = r.vehicle_id
        GROUP BY v.vehicle_id
    """, columns=["Vehículo", "Total Gastado en Reparaciones"])

def consulta_clientes_con_pagos():
    st.header("Consulta: Clientes que han realizado pagos (INNER JOIN)")
    execute_query("""
        SELECT DISTINCT c.name AS Cliente
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        JOIN payments p ON s.sale_id = p.sale_id
    """, columns=["Cliente"])

def consulta_promedio_capacidad_motor():
    st.header("Consulta: Promedio de capacidad de motor por marca")
    execute_query("""
        SELECT brand AS Marca, AVG(engine_capacity) AS Promedio_Capacidad_Motor
        FROM vehicles
        GROUP BY brand
    """, columns=["Marca", "Promedio Capacidad de Motor"])

st.title("Consultas de Base de Datos para Dealership")
st.write("Seleccione una consulta en el menú de la izquierda para ver los resultados.")

queries_interface()