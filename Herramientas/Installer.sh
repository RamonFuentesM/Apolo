#!/bin/bash

# Pedir permisos de sudo
if [[ $EUID -ne 0 ]]; then    
	echo "Necesitas sudo para realizar la instalcion"     
	exit 1 
fi
echo "--> Actualizando paquetes e instalando dependencias..."
sleep 1
apt update -y
error "Ocurrio un error al actualizar los paquetes"

# Instalar python3
echo "Descargando python3..."
sleep 1
apt-get install -y python3-apt python3-pip 
error "Ocurrio un error al instalar python3"

# Instalar Nmap
echo "Descargando Nmap..."
sleep 1
apt install nmap -y
error "Ocurrio un error al instalar nmap"

# Instalar Hydra
echo "Descargando Hydra..."
sleep 1
apt install hydra -y
error "Ocurrio un error al instalar hydra"

# Instalar WhatWeb
echo "Descargando WhatWeb..."
sleep 1
apt install whatweb -y
error "Ocurrio un error al instalar nmap"

# Instalar theHarvester
echo "Descargando theHarvester..."
sleep 1
pip3 install -r theHarvester/requirements.txt
error "Ocurrio un error al instalar nmap"

# Instalar lighthouse
echo "Descargando lighthouse..."
sleep 1
apt install npm -y
npm install -g lighthouse
error "Ocurrio un error al instalar lighthouse"



