#Libreria
import pyodbc
import seaborn as sns
import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
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

#Exploracion de la tabla transaccion:
print("Leyendo datos de la tabla transaccion...")
df_transaccion = pd.read_sql("SELECT * FROM transaccion", conn)

#Verificacion que se leyo la tabla correctamente:
print("Datos cargados de la tabla:")
print(df_transaccion.head())

#Detalle de la variable:
X = df_transaccion[['monto']].copy()

#Escalar monto para mayor exactitud:
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#Aplicar clustering:
kmeans = KMeans(n_clusters=3, random_state=42)
df_transaccion['clusters'] = kmeans.fit_predict(X_scaled)

#Visualización de cluster:
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.stripplot(data=df_transaccion, x='clusters', y='monto', jitter=True, palette='Set2')
plt.title('Distribución de montos por tipo de clusters')
plt.xlabel('Grupo de clusters')
plt.ylabel('Monto')
plt.show()

#Visualizar las transacciones sospechosas:
promedios = df_transaccion.groupby('clusters')['monto'].mean()
cluster_sospechoso = promedios.idxmax()
print(f"Cluster sospechoso identificado: {cluster_sospechoso}")
print(df_transaccion[df_transaccion['clusters'] == cluster_sospechoso])

#Cierro la conexión al final:
conn.close()