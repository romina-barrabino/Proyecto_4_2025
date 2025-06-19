#Libreria
import pyodbc
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
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

#Anomalia = Analizo si se realizo un retiro de dinero alto.

#Examino la tabla transaccion y creo un dataframe:
query = """
SELECT id_transaccion, tipo_de_transaccion, monto
FROM transaccion
WHERE tipo_de_transaccion = 'retiro'
"""
df_retiros = pd.read_sql(query, conn)

#Escalo los montos (recomendacion para mayor precision):
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_retiros[['monto']])

#Elijo el modelo de scikit-learn:
modelo = IsolationForest(contamination=0.05, random_state=42)
df_retiros['anomalía'] = modelo.fit_predict(X_scaled)

#Defino como True si es un retiro anómalo:
df_retiros['es_anómalo'] = df_retiros['anomalía'] == -1

#Verifico que detecte los retiros anomalos:
print("Retiros anómalos detectados:")
print(df_retiros[df_retiros['es_anómalo']])

#Adjunto un detalle para tener en cuenta sobre los retiros:
print("Estadísticas de los retiros:")
print("Monto promedio:", np.mean(df_retiros['monto']))
print("Máximo retiro:", np.max(df_retiros['monto']))
print("Mínimo retiro:", np.min(df_retiros['monto']))

#Cierro la conexión al final
conn.close()