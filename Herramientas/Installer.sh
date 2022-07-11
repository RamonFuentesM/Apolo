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
sudo apt-get install python3-tk
sudo apt-get install -y python3-all-dev
pip install validators
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
git clone https://github.com/laramies/theHarvester
cd theHarvester/
pip3 install -r requirements/base.txt
pip3 install -r theHarvester/requirements.txt
python3 setup.py install
cd ..
error "Ocurrio un error al instalar nmap"

# Instalar lighthouse
echo "Descargando lighthouse..."
sleep 1
apt install npm -y
sudo npm cache clean -f
sudo npm install -g n
sudo n stable
npm install -g lighthouse
sudo apt install wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
error "Ocurrio un error al instalar lighthouse"

# Instalar Dependency-check
echo "Descargando theHarvester..."
sleep 1
unzip dependency-check-7.1.1-release.zip
set JAVA_HOME=%PROGRAMFILES%\Java\jdk-13.0.2
sudo apt install maven -y
error "Ocurrio un error al instalar nmap"

# Instalar Bolt CSRF
echo "Descargando theHarvester..."
sleep 1
sudo pip install -r Bolt/requirements.txt
error "Ocurrio un error al instalar nmap"

echo "--> Actualizando paquetes e instalando dependencias..."
sleep 1
apt update -y
error "Ocurrio un error al actualizar los paquetes"


