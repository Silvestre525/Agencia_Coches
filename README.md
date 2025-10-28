# Construye la imagen y levanta los servicios (DB y API)
docker-compose up --build -d

# Muestra los contenedores en ejecución
docker ps

# Detiene y elimina los contenedores y la red
docker-compose down