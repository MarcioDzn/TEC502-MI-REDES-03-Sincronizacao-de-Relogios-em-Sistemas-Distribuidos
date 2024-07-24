# Usa uma imagem base Python
FROM python:3.8.10-slim

# Copia o script Python para o contêiner
COPY . /app

# Define o diretório de trabalho
WORKDIR /app

# Atualiza e instala o iputils-ping
RUN apt-get update && apt-get install -y iputils-ping

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

RUN pip install -r requirements.txt

# Expõe a porta utilizada
EXPOSE 8088

# Comando para executar o script Python
CMD ["python", "main.py"]