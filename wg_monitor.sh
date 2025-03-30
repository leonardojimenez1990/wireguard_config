#!/bin/bash
# Script principal para levantar la interfaz WireGuard y monitorear el tráfico en tiempo real.
# Autor: leonardo jimenez
# Fecha: 30032025

# Verificar que se ejecute como root
if [ "$EUID" -ne 0 ]; then
    echo "Ejecute este script como root."
    exit 1
fi

WG_CONF="/etc/wireguard/wg0.conf"

# Verificar que el archivo de configuración existe
if [ ! -f "$WG_CONF" ]; then
    echo "El archivo de configuración $WG_CONF no se encontró."
    echo "Ejecute primero el script create_wg_config.sh."
    exit 1
fi

# Mostrar el contenido del archivo de configuración
echo "Mostrando el contenido de $WG_CONF:"
cat "$WG_CONF"
echo ""

# Levantar la interfaz WireGuard
echo "Levantando la interfaz WireGuard wg0..."
wg-quick up wg0
if [ $? -ne 0 ]; then
    echo "Error al levantar la interfaz. Revise la configuración en $WG_CONF."
    exit 1
fi
echo "La interfaz wg0 se ha activado correctamente."

# Menú interactivo de monitorización
while true; do
    echo ""
    echo "Menú de monitorización para la interfaz wg0:"
    echo "  1) Mostrar estadísticas de WireGuard (wg show wg0)"
    echo "  2) iftop (tráfico en tiempo real, interfaz interactiva)"
    echo "  3) vnstat en modo live (estadísticas en vivo)"
    echo "  4) nload (uso de ancho de banda en tiempo real)"
    echo "  5) bmon (visualización gráfica de tráfico)"
    echo "  6) tcpdump (captura de paquetes, presione Ctrl+C para detener)"
    echo "  7) Detener la interfaz WireGuard y salir"
    read -p "Seleccione una opción [1-7]: " OPCION

    case $OPCION in
        1)
            echo "Mostrando estadísticas de WireGuard..."
            wg show wg0
            ;;
        2)
            echo "Ejecutando iftop en la interfaz wg0..."
            iftop -i wg0
            ;;
        3)
            echo "Ejecutando vnstat en modo live..."
            vnstat -l -i wg0
            ;;
        4)
            echo "Ejecutando nload para la interfaz wg0..."
            nload wg0
            ;;
        5)
            echo "Ejecutando bmon para la interfaz wg0..."
            bmon -p wg0
            ;;
        6)
            echo "Ejecutando tcpdump en la interfaz wg0 (Ctrl+C para detener)..."
            tcpdump -i wg0 -nn -vv
            ;;
        7)
            echo "Deteniendo la interfaz WireGuard wg0..."
            wg-quick down wg0
            echo "Interfaz detenida. Saliendo..."
            exit 0
            ;;
        *)
            echo "Opción no válida. Intente de nuevo."
            ;;
    esac
done

