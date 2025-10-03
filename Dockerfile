# Imagen base
FROM python:3.10

# Instalar Slither
RUN pip install slither-analyzer

# Instalar dependencias para solc
RUN apt-get update && apt-get install -y curl git build-essential

# Instalar solc >=0.8
RUN curl -L https://github.com/ethereum/solidity/releases/download/v0.8.21/solc-static-linux -o /usr/bin/solc && \
    chmod +x /usr/bin/solc

# Carpeta de trabajo
WORKDIR /code

# Por defecto corre Slither
ENTRYPOINT ["slither"]
