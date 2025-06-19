#Libreria
import pyodbc
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns #permite visualizar datos que se ajustan a modelos estadísticos simples
from dotenv import load_dotenv

#Cargo las variables desde el archivo .env
load_dotenv()

#Llamo a los parametros desde el archivo .env
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_UID")
password = os.getenv("SQL_PWD")
driver = os.getenv("SQL_DRIVER")

#Conexión a SQL Server
print(" Preparando cadena de conexión...")
conn_str = f'''
    DRIVER={{{driver}}};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    TrustServerCertificate=yes;
'''
conn = None
try:
    print("Intentando conectar a SQL Server...")
    conn = pyodbc.connect(conn_str, timeout=5)
    print("Conexión exitosa.")
except pyodbc.Error as e:
    print("Error de conexión:")
    print(e)
if not conn:
    print("El script se detiene porque no se pudo establecer conexión.")
    exit()

#Visualizacion 1 = Transacciones por persona por mes

#Exploracion de la tabla cuenta:
print("Leyendo datos de la tabla cuenta...")
df_cuenta = pd.read_sql("SELECT * FROM cuenta", conn)

#Verificacion que se leyo la tabla correctamente:
print("Datos cargados de la tabla:")
print(df_cuenta.head())

#Transformacion:
#a) Modificacion de las fechas de la tabla transaccion para separar las columnas por mes:
print("Procesando datos de transaccion...")
df_transaccion = pd.read_sql("SELECT * FROM transaccion", conn)
df_transaccion['fecha'] = pd.to_datetime(df_transaccion['fecha'])
df_transaccion['mes'] = df_transaccion['fecha'].dt.to_period('M')
#b) Unir los datos de la tabla cuenta con la tabla transaccion
df_transaccion = df_transaccion.merge(df_cuenta, on='id_cuenta', how='left')
print("Procesamiento completado.")

#Creacion de la columna movimiento para el grafico
df_transaccion = df_transaccion.groupby(['id_usuario', 'meses']).agg({
    'monto': 'sum'
}).reset_index()
df_transaccion.rename(columns={'monto': 'movimiento'}, inplace=True)

#Comparo los resultados de la encuesta por empleado
print("Generando el gráfico")
sns.set_theme(style="darkgrid")
plt.figure(figsize=(14, 6))
sns.lineplot(data=df_transaccion, x='meses', y='movimiento', hue='id_usuario', marker="o")
plt.title("Transacciones por persona por mes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
print("Gráfico mostrado correctamente")

#Cierro la conexión al final
conn.close()