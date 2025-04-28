# Usa uma imagem oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos da sua API para dentro da imagem
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta (ajuste para a porta que seu Flask usa)
EXPOSE 5000

# Comando para rodar a API
CMD ["python", "app.py"]
