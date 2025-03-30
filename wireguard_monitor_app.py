#!/usr/bin/env python3
# Autor: leonardo jimenez
# Fecha: 30032025
"""
WireGuard Monitor App Mejorada
------------------------------
Esta aplicación gráfica permite:
  - Levantar la interfaz WireGuard (wg0) usando "wg-quick up wg0"
  - Detener la interfaz WireGuard usando "wg-quick down wg0"
  - Mostrar estadísticas actuales con "wg show wg0"
  - Iniciar un monitoreo periódico que actualiza en tiempo real las estadísticas de wg0

Buenas prácticas aplicadas:
  • Modularización: funciones separadas para lógica de comandos y GUI.
  • Type hints y docstrings para mayor claridad.
  • Uso del módulo logging para registrar eventos y errores.
  • Actualización segura de la GUI mediante el método after() de Tkinter.
  • Verificación de disponibilidad de comandos con shutil.which.
  • Manejo de excepciones y timeouts en la ejecución de subprocesos.
  
Requisitos:
  - Python 3
  - Tkinter (normalmente incluido en Python en Linux)
  - Los comandos 'wg', 'wg-quick' deben estar en el PATH y ser ejecutables.
  - Ejecutar con permisos de root.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import time
import logging
import os
import sys
import shutil
from typing import List, Optional

# Configurar logging (se puede redirigir a un archivo si se desea)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

# Constantes para comandos requeridos
REQUIRED_COMMANDS = ["wg", "wg-quick"]

def check_command_availability(cmd: str) -> bool:
    """
    Verifica que un comando esté disponible en el PATH.
    
    :param cmd: Nombre del comando a verificar.
    :return: True si está disponible, False de lo contrario.
    """
    return shutil.which(cmd) is not None

def execute_command(command: List[str], timeout: Optional[int] = 10) -> str:
    """
    Ejecuta un comando en el sistema y retorna su salida.
    
    :param command: Lista de argumentos que conforman el comando.
    :param timeout: Tiempo máximo de espera (en segundos).
    :return: Salida del comando.
    """
    logging.info("Ejecutando comando: %s", " ".join(command))
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        if result.returncode != 0:
            logging.error("Error ejecutando comando: %s", result.stderr)
            return f"Error:\n{result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired as e:
        logging.error("Tiempo de espera excedido para el comando: %s", e)
        return "Error: Tiempo de espera excedido.\n"
    except Exception as e:
        logging.exception("Excepción al ejecutar el comando:")
        return f"Excepción: {str(e)}\n"

class WireGuardMonitorApp(tk.Tk):
    def __init__(self) -> None:
        """
        Inicializa la aplicación y configura la ventana principal.
        """
        super().__init__()
        self.title("WireGuard Monitor")
        self.geometry("800x600")
        self.monitoring: bool = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        self._check_required_commands()
        self._create_widgets()

    def _check_required_commands(self) -> None:
        """
        Verifica que todos los comandos necesarios estén disponibles.
        """
        missing = [cmd for cmd in REQUIRED_COMMANDS if not check_command_availability(cmd)]
        if missing:
            messagebox.showerror("Error", f"Los siguientes comandos no están disponibles en el PATH: {', '.join(missing)}.\n"
                                          "Instale las dependencias necesarias antes de ejecutar la aplicación.")
            self.destroy()
            sys.exit(1)
    
    def _create_widgets(self) -> None:
        """
        Crea y posiciona los widgets de la interfaz.
        """
        button_frame = tk.Frame(self)
        button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.btn_start = tk.Button(button_frame, text="Levantar wg0", width=15,
                                   command=self.start_interface)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(button_frame, text="Detener wg0", width=15,
                                  command=self.stop_interface)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.btn_stats = tk.Button(button_frame, text="Mostrar estadísticas", width=20,
                                   command=self.show_stats)
        self.btn_stats.pack(side=tk.LEFT, padx=5)

        self.btn_start_monitor = tk.Button(button_frame, text="Iniciar monitoreo", width=20,
                                           command=self.start_monitor)
        self.btn_start_monitor.pack(side=tk.LEFT, padx=5)

        self.btn_stop_monitor = tk.Button(button_frame, text="Detener monitoreo", width=20,
                                          command=self.stop_monitor)
        self.btn_stop_monitor.pack(side=tk.LEFT, padx=5)

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=30)
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def append_text(self, text: str) -> None:
        """
        Agrega texto al widget de salida de forma segura en el hilo principal.
        
        :param text: Texto a agregar.
        """
        self.output_text.after(0, lambda: self._append_text(text))
        
    def _append_text(self, text: str) -> None:
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)

    def start_interface(self) -> None:
        """
        Levanta la interfaz WireGuard wg0 usando 'wg-quick up wg0'.
        """
        self.append_text("Levantando la interfaz WireGuard wg0...\n")
        threading.Thread(target=self._run_command_and_append,
                         args=(["wg-quick", "up", "wg0"],),
                         daemon=True).start()

    def stop_interface(self) -> None:
        """
        Detiene la interfaz WireGuard wg0 usando 'wg-quick down wg0'.
        """
        self.append_text("Deteniendo la interfaz WireGuard wg0...\n")
        threading.Thread(target=self._run_command_and_append,
                         args=(["wg-quick", "down", "wg0"],),
                         daemon=True).start()

    def show_stats(self) -> None:
        """
        Muestra las estadísticas actuales de WireGuard usando 'wg show wg0'.
        """
        self.append_text("Obteniendo estadísticas de wg0...\n")
        threading.Thread(target=self._run_command_and_append,
                         args=(["wg", "show", "wg0"],),
                         daemon=True).start()

    def _run_command_and_append(self, command: List[str]) -> None:
        """
        Ejecuta un comando y actualiza la salida en la interfaz.
        
        :param command: Comando a ejecutar.
        """
        output = execute_command(command)
        self.append_text(output + "\n")

    def start_monitor(self) -> None:
        """
        Inicia el monitoreo periódico de las estadísticas cada 5 segundos.
        """
        if self.monitoring:
            messagebox.showinfo("Monitoreo", "El monitoreo ya está en ejecución.")
            return
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.append_text("Monitoreo iniciado en la interfaz wg0...\n")

    def _monitor_loop(self) -> None:
        """
        Bucle que se ejecuta en un hilo separado y actualiza la salida de 'wg show wg0'
        cada 5 segundos de forma segura.
        """
        while self.monitoring:
            output = execute_command(["wg", "show", "wg0"])
            self.append_text("Actualización:\n" + output + "\n")
            time.sleep(5)

    def stop_monitor(self) -> None:
        """
        Detiene el monitoreo periódico.
        """
        if self.monitoring:
            self.monitoring = False
            self.append_text("Monitoreo detenido.\n")
        else:
            self.append_text("El monitoreo no estaba en ejecución.\n")

def check_root() -> None:
    """
    Verifica que la aplicación se ejecute con permisos de root.
    """
    if os.geteuid() != 0:
        messagebox.showerror("Permisos insuficientes",
                             "Esta aplicación debe ejecutarse como root.\nEjecute 'sudo python3 wireguard_monitor_app.py'")
        sys.exit(1)

if __name__ == "__main__":
    # Verificar permisos de root antes de iniciar la aplicación
    check_root()
    # Iniciar la aplicación en el hilo principal de Tkinter
    app = WireGuardMonitorApp()
    app.mainloop()

