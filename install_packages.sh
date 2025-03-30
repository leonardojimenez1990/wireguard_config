#!/bin/bash
# Script para actualizar el sistema e instalar WireGuard y herramientas de monitorización.
# Autor: [Tu Nombre]
# Fecha: [Fecha]

# Verificar que se ejecute como root
if [ "$EUID" -ne 0 ]; then
    echo "Ejecute este script como root."
    exit 1
fi

echo "Actualizando repositorios y actualizando el sistema..."
apt update && apt upgrade -y

echo "Instalando WireGuard y herramientas de monitorización..."
apt install -y wireguard wireguard-tools openresolv iftop vnstat nload tcpdump bmon

echo "Instalación completada."


