#!/bin/bash
# Script para crear un archivo de configuración de ejemplo para WireGuard.
# Autor: leonardo jimenez
# Fecha: 30032025

# Verificar que se ejecute como root
if [ "$EUID" -ne 0 ]; then
    echo "Ejecute este script como root."
    exit 1
fi

WG_CONF="/etc/wireguard/wg0.conf"

if [ -f "$WG_CONF" ]; then
    echo "El archivo de configuración $WG_CONF ya existe."
else
    echo "Creando archivo de configuración de ejemplo en $WG_CONF..."
    cat <<EOF > "$WG_CONF"
[Interface]
# Reemplace 'TU_CLAVE_PRIVADA' por la clave privada de su cliente.
PrivateKey = TU_CLAVE_PRIVADA
# Dirección IP asignada al cliente dentro de la VPN.
Address = 10.8.0.2/24
# Servidor DNS a utilizar (puede ser interno o público).
DNS = 10.8.1.3

[Peer]
# Reemplace 'CLAVE_PUBLICA_DEL_SERVER' con la clave pública del servidor.
PublicKey = CLAVE_PUBLICA_DEL_SERVER
# Clave precompartida para mayor seguridad (opcional).
PresharedKey = CLAVE_PRECOMPARTIDA
# Todo el tráfico se enruta a través de la VPN.
AllowedIPs = 0.0.0.0/0, ::/0
# Mantiene viva la conexión (útil en entornos NAT).
PersistentKeepalive = 25
# Dirección IP pública o dominio del servidor y puerto.
Endpoint = 192.168.1.7:51820
EOF
    echo "Archivo de configuración creado."
    echo "Edítelo con sus valores reales antes de continuar."
fi

