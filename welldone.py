#!/usr/bin/env python3
"""
WellDone DevKit: Linux Edition
Instalador interativo de ambiente de desenvolvimento para Linux.
Fork do projeto original (Windows/PowerShell) por WellytonSdJ.

Uso: python3 welldone.py
"""

import sys
import os

# Se liga de que a raiz do projeto esteja no caminho
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.utils.colors import *
from scripts.utils.distro import detect_distro, detect_package_manager
from scripts.utils.ui import clear, pause, show_boot_screen, show_menu

from scripts.modules import (
    install_dev_essentials,
    install_optional_apps,
    install_terminal_theme,
    manage_ssh,
    setup_git,
)


def run_all(pm: dict):
    """Executa todos os módulos em sequência."""
    from scripts.utils.ui import show_module_header
    show_module_header("INSTALANDO TUDO")
    print(f"  {CYAN}Executando todos os módulos em sequência...{NC}")
    print()
    pause()

    install_dev_essentials.run(pm)
    install_terminal_theme.run(pm)
    setup_git.run(pm)
    manage_ssh.run(pm)
    install_optional_apps.run(pm)

    from scripts.utils.ui import show_module_header
    show_module_header("SETUP COMPLETO")
    print(f"  {GREEN}✓ Tudo instalado e configurado!{NC}")
    print()
    print(f"  {GRAY}Próximos passos:{NC}")
    print(f"  {CYAN}1.{NC} Feche e reabra o terminal")
    print(f"  {CYAN}2.{NC} Configure a fonte JetBrainsMono Nerd Font no seu terminal")
    print(f"  {CYAN}3.{NC} Adicione sua chave SSH no GitHub")
    print()
    pause()


def main():
    # Detecção do Environment
    distro = detect_distro()
    pm = detect_package_manager()

    if pm is None:
        print(f"{RED}✗ Nenhum gerenciador de pacotes compatível encontrado.{NC}")
        print(f"{GRAY}  Suportados: pacman, apt, dnf, yum, zypper, xbps-install, apk, flatpak{NC}")
        sys.exit(1)

    show_boot_screen(distro, pm["name"])

    menu_items = [
        {"label": "Dev Essentials",   "action": lambda: install_dev_essentials.run(pm)},
        {"label": "Terminal Theme",   "action": lambda: install_terminal_theme.run(pm)},
        {"label": "Git Setup",        "action": lambda: setup_git.run(pm)},
        {"label": "SSH Manager",      "action": lambda: manage_ssh.run(pm)},
        {"label": "Apps Opcionais",   "action": lambda: install_optional_apps.run(pm)},
        {"separator": True},
        {"label": "Instalar Tudo",    "action": lambda: run_all(pm)},
    ]

    while True:
        choice = show_menu(
            menu_items,
            subtitle=f"v2.0 Linux  |  github.com/WellytonSdJ/welldone-devkit"
        )

        if choice is None:
            break

        choice["action"]()

    # Tchau-Tchau do Well-chan
    clear()
    print()
    print(f"{CYAN}  Até mais! WellDone DevKit encerrado.{NC}")
    print(f"{GRAY}  github.com/WellytonSdJ/welldone-devkit{NC}")
    print()


if __name__ == "__main__":
    main()
