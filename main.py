import streamlit as st
from employees import employees_interface
from customers import customers_interface

option = st.sidebar.selectbox("Selecciona una tabla", ["Empleados", "Clientes", "Vehículos", "Ventas", "Pagos", "Reparaciones"])

if option == "Empleados":
    employees_interface()
elif option == "Clientes":
    customers_interface()

