# Imagen base de Python
FROM python:3.9

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del proyecto al contenedor
COPY . .

# Puerto expuesto por la aplicación Flask
EXPOSE 8000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app.py"]
