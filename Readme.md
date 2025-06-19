# Aplicaciones a instalar: 
SQL Microsoft Server (creo en ella una base de datos que llamo "Empleados")
Visual Studio
Git (desde https://git-scm.com/downloads/win)

# Instalaciones requeridas:
pandas (pip install pandas)
seaborn (pip install seaborn) 
pyodc (pip install pyodbc)
scikit-learn (pip install scikit-learn)

# Estructura creada en SQL:
Transacciones (base de datos)
|_ usuario (tabla)
|_ cuenta (tabla)
|_ transaccion (tabla)

# Estructura creada en Visual Studio:
Proyecto_4_2025/
├── Imagenes/                         # Carpeta con capturas de pantalla del proyecto
├── Scripts/
│   ├── Creacion_tablas               # Contiene scripts SQL para crear tablas
│   ├── Carga_y_actualizacion_tablas  # Scripts para cargar y actualizar datos de las tablas
│   ├── Visualizacion_1         
│   ├── Visualizacion_2          
│   ├── Anomalias                
│   └── Clustering_y_sospechosos 
├── Readme.md                         # Archivo de documentación del proyecto
├── .env                              # Variables de entorno (usuarios y contraseñas SQL)
└── .gitignore                        # Archivos y carpetas excluidos del repositorio


# Instalaciones y/o scripts para la terminal de Visual Studio: 
a) Evitar la visualizacion de la carpeta .env en GitHub: git rm --cached .env
b) Verificacion de la instalacion de git: git --version

# Conexion entre Visual Studio y un repositorio en GitHub que llamare "Proyecto_2_2025"
git init
git add .
git commit -m "Iniciando proyecto en GitHub"