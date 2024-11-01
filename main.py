import streamlit as st
from employees import employees_interface
from customers import customers_interface
from vehicles import vehicles_interface
from sales import sales_interface
from payments import payments_interface
from repairs import repairs_interface
from queries import queries_interface


option = st.sidebar.selectbox("Selecciona una tabla", ["Empleados", "Clientes", "Vehículos", "Ventas", "Pagos", "Reparaciones", "Consultas"])

if option == "Empleados":
    employees_interface()
elif option == "Clientes":
    customers_interface()
elif option == "Vehículos":
    vehicles_interface()
elif option == "Ventas":
    sales_interface()
elif option == "Pagos":
    payments_interface()
elif option == "Reparaciones":
    repairs_interface()
elif option == "Consultas":
    queries_interface()
