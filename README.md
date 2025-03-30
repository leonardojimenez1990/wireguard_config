Claro, aquí tienes el contenido del archivo README.md corregido para mostrar correctamente en la web:

```markdown
# wireguard_config

## Descripción
Este proyecto proporciona scripts para configurar y monitorear fácilmente una interfaz WireGuard en sistemas basados en Linux. Incluye herramientas para instalar los paquetes necesarios, crear un archivo de configuración de WireGuard y monitorear el tráfico en tiempo real.

## Requisitos previos
- Sistema operativo basado en Linux.
- Privilegios de superusuario (root).
- Conexión a Internet para instalar paquetes.

## Instalación

### Clonar el repositorio
```bash
git clone https://github.com/leonardojimenez1990/wireguard_config.git
cd wireguard_config
```

### Instalar paquetes necesarios
Ejecute el script `install_packages.sh` para actualizar el sistema e instalar WireGuard y las herramientas de monitorización necesarias.
```bash
sudo bash install_packages.sh
```

## Configuración

### Crear archivo de configuración de WireGuard
Ejecute el script `create_wg_config.sh` para generar un archivo de configuración de ejemplo en `/etc/wireguard/wg0.conf`.
```bash
sudo bash create_wg_config.sh
```
Este script creará un archivo de configuración con valores de ejemplo. Edite el archivo con sus valores reales antes de continuar:
```ini
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
```

## Uso

### Levantar la interfaz WireGuard y monitorear tráfico
Ejecute el script `wg_monitor.sh` para levantar la interfaz WireGuard y acceder a un menú interactivo de monitorización.
```bash
sudo bash wg_monitor.sh
```
El menú proporcionará las siguientes opciones:
1. Mostrar estadísticas de WireGuard (`wg show wg0`)
2. iftop (tráfico en tiempo real, interfaz interactiva)
3. vnstat en modo live (estadísticas en vivo)
4. nload (uso de ancho de banda en tiempo real)
5. bmon (visualización gráfica de tráfico)
6. tcpdump (captura de paquetes, presione Ctrl+C para detener)
7. Detener la interfaz WireGuard y salir

## Contribuciones
Las contribuciones son bienvenidas. Para contribuir, siga estos pasos:
1. Haga un fork del repositorio.
2. Cree una nueva rama (`git checkout -b feature-nueva`).
3. Realice sus cambios y haga commit (`git commit -am 'Añadir nueva característica'`).
4. Haga push a la rama (`git push origin feature-nueva`).
5. Cree un nuevo Pull Request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo LICENSE para obtener más detalles.

## Contacto
Para preguntas o soporte, puede contactar a Leonardo Jimenez a través de su perfil de GitHub.
```

Este README proporciona una guía clara y detallada para cualquier usuario o colaborador del proyecto.
