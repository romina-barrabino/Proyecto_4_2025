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

#Visualizacion 2 = Saldos_actuales por persona por mes

#Exploracion de la tabla cuenta:
print("Leyendo datos de la tabla cuenta...")
df_cuenta = pd.read_sql("SELECT * FROM cuenta", conn)

#Verificacion que se leyo la tabla correctamente:
print("Datos cargados de la tabla:")
print(df_cuenta.head())

#Transformacion:
#a) Uso la tabla transaccion para recopilar las fechas:
print("Procesando datos de transaccion...")
df_transaccion = pd.read_sql("SELECT * FROM transaccion", conn)
df_transaccion['fecha'] = pd.to_datetime(df_transaccion['fecha'])
df_transaccion['mes'] = df_transaccion['fecha'].dt.to_period('M')

#b) Ordeno por fecha para que el último saldo del mes sea correcto:
df_transaccion.sort_values(by=['id_usuario', 'mes', 'fecha'], inplace=True)

#c) Obtengo el último saldo mensual por usuario:
df_saldo_final = df_transaccion.groupby(['id_usuario', 'mes']).last().reset_index()

#d) Cambio el nombre de saldo actual por saldo final mes:
df_saldo_final.rename(columns={'saldo_actual': 'saldo_final_mes'}, inplace=True)

#Comparo por mes el tipo de rotacion de los empleado
print("Generando el grafico")
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_saldo_final, x='mes', y='saldo_final_mes', hue='id_usuario', marker="o")
plt.xticks(rotation=45)
plt.title("Saldo mensual por persona")
plt.xlabel("Mes")
plt.ylabel("Saldo final")
plt.tight_layout()
plt.show()
print("Gráfico mostrado correctamente")

#Cierro la conexión al final
conn.close()