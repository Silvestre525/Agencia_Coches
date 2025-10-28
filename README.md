# 🐳 Proyecto Final: API REST de Autos Dockerizada (FastAPI + MySQL)

Este proyecto cumple con la consigna del TP, demostrando la contenerización completa de un stack backend utilizando Docker Compose, FastAPI (Python) como servicio API y MySQL como servicio de base de datos persistente.

**Tecnologías:**
* **Backend:** Python 3.11, FastAPI, SQLAlchemy, PyMySQL.
* **Contenerización:** Docker, Docker Compose (v3.8).
* **Base de Datos:** MySQL 8.0.


## 🚀 1. Despliegue Rápido (Quick Start)

Para ejecutar esta aplicación, solo necesita tener **Git** y **Docker Desktop** (o Docker Engine) instalados.

1.  **Clonar el Repositorio:**
    ```bash
    git clone [ENLACE_DE_TU_REPOSITORIO]
    cd [nombre-de-tu-carpeta]
    ```

2.  **Configurar Variables de Entorno:**
    Asegúrese de que el archivo `.env` exista en la raíz del proyecto. Estas variables son cruciales para la conexión entre los contenedores. (Los valores predeterminados son suficientes para la prueba).

3.  **Construir y Ejecutar el Stack:**
    El comando `docker-compose up` construye la imagen de la API y levanta la red con ambos servicios.
    ```bash
    # La opción --build asegura que el Dockerfile se compile
    docker-compose up --build -d
    ```


## 🌐 2. Uso y Acceso

Una vez que los contenedores estén levantados, la API es accesible en el puerto **8000** de su máquina local.

* **Documentación de la API (Swagger UI):**
    `http://localhost:8000/docs`

* **Ejemplo de Consulta (cURL):**
    Dado que la aplicación incluye **datos de prueba (seed data)**, puede consultar la lista de autos inmediatamente:
    ```bash
    # Consulta la lista de autos insertados automáticamente
    curl http://localhost:8000/autos/
    ```

### 4. Explicación Técnica (Puntos Clave del TP)

```markdown
## 🛠️ 3. Puntos Técnicos y Ciclo de Vida del Contenedor

#### A. Gestión de Dependencias y Ciclo de Vida

1.  **Dockerfile:** Define una imagen limpia (`python:3.11-slim`), instala dependencias (`requirements.txt`), y usa `CMD ["uvicorn"...]` como comando de inicio.
2.  **Docker Compose (`docker-compose.yml`):**
    * Orquesta dos servicios: `api` y `db` (MySQL).
    * **Conexión Interna:** El servicio `api` utiliza el nombre de servicio **`db`** como host, conectándose al puerto **3306** interno. (Nota: El puerto `3307:3306` en el servicio `db` es solo para acceso externo, no para la comunicación entre contenedores).
    * **Persistencia:** Utiliza un `volume` (`mysql_data`) para asegurar que los datos de MySQL persistan si el contenedor `db` se detiene o se reinicia.
    * **Resiliencia (`healthcheck`):** La dependencia `db: condition: service_healthy` combinada con el `healthcheck` de MySQL garantiza que la API no intentará iniciar hasta que la base de datos esté lista para aceptar conexiones.

#### B. Solución de Resiliencia del Código (Punto Avanzado)

A pesar del `healthcheck` de Docker Compose, la aplicación implementa una lógica de reintento en el código Python para manejar la ventana de tiempo donde la base de datos puede estar lista pero lenta para responder a consultas de SQLAlchemy:

* **Archivo `db_init.py`:** Contiene la función `initialize_db_and_seed()`.
* **Mecanismo de Reintento:** Esta función intenta ejecutar la creación de tablas (`Base.metadata.create_all`) hasta **10 veces** con un retraso de 2 segundos, capturando los errores de `OperationalError` de MySQL.
* **Seed Data:** Tras la conexión exitosa, la función `seed_data()` inserta datos de prueba si la tabla está vacía, haciendo que la API sea funcional inmediatamente.
* **Ejecución:** Esta lógica se dispara mediante el evento de inicio de FastAPI: `@app.on_event("startup")` en `main.py`.


## 🛑 4. Mantenimiento y Cierre

* **Verificar Contenedores:**
    ```bash
    docker ps
    ```
* **Ver Logs:**
    ```bash
    docker-compose logs -f
    ```
* **Detener y Limpiar (Contenedores y Red):**
    ```bash
    docker-compose down
    ```
* **Eliminar Datos Persistentes (Volumen):**
    *(Solo si desea que MySQL se inicialice de nuevo completamente)*
    ```bash
    docker volume rm [nombre_del_directorio_actual]_mysql_data
    ```