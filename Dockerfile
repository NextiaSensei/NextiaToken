
# Imagen base ligera con Python 3.10
FROM python:3.10-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl git build-essential software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Instalar Slither y sus dependencias
RUN pip install --no-cache-dir slither-analyzer==0.11.4 evm-cfg-builder==0.4.1 crytic-compile==0.3.4

# Instalar compilador Solidity >=0.8.21
RUN curl -L https://github.com/ethereum/solidity/releases/download/v0.8.21/solc-static-linux -o /usr/bin/solc && \
    chmod +x /usr/bin/solc

# Carpeta de trabajo
WORKDIR /code

# Slither se ejecutará por defecto
ENTRYPOINT ["slither"]
