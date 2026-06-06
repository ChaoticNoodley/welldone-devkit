"""
Dev Essentials — instala ferramentas base de desenvolvimento.
Equivalente Linux do install_dev_essentials.ps1
"""

import shutil
import subprocess

from scripts.utils.colors import *
from scripts.utils.distro import install_package, resolve_package
from scripts.utils.ui import (
    ask, confirm, pause, run_step, show_module_header
)


def _install_nvm():
    """Instala nvm via script oficial."""
    if shutil.which("nvm") or (
        subprocess.run(
            ["bash", "-c", "source ~/.nvm/nvm.sh && nvm --version"],
            capture_output=True
        ).returncode == 0
    ):
        print(f"  {GRAY}nvm já instalado, pulando.{NC}")
        return True

    result = subprocess.run(
        ["bash", "-c",
         "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"],
        capture_output=False
    )
    return result.returncode == 0


def _install_node_lts():
    """Instala Node.js LTS via nvm."""
    result = subprocess.run(
        ["bash", "-c", "source ~/.nvm/nvm.sh && nvm install --lts && nvm use --lts"],
        capture_output=False
    )
    return result.returncode == 0


def _install_vscode(pm: dict):
    """Instala VS Code; usa flatpak como fallback universal."""
    pkg = resolve_package("vscode", pm)
    if pkg:
        return install_package(pkg, pm)

    # Fallback: flatpak
    if shutil.which("flatpak"):
        print(f"  {GRAY}Usando flatpak como fallback para VS Code...{NC}")
        subprocess.run(
            ["flatpak", "remote-add", "--if-not-exists", "flathub",
             "https://flathub.org/repo/flathub.flatpakrepo"],
            capture_output=True
        )
        result = subprocess.run(
            ["flatpak", "install", "-y", "flathub", "com.visualstudio.code"]
        )
        return result.returncode == 0

    print(f"  {YELLOW}VS Code: instale manualmente em https://code.visualstudio.com/download{NC}")
    return False


def run(pm: dict):
    show_module_header("DEV ESSENTIALS")

    tools = [
        ("git",   lambda: install_package(resolve_package("git", pm) or "git", pm)),
        ("curl",  lambda: install_package(resolve_package("curl", pm) or "curl", pm)),
        ("wget",  lambda: install_package(resolve_package("wget", pm) or "wget", pm)),
        ("nvm",   _install_nvm),
        ("Node.js LTS (via nvm)", _install_node_lts),
        ("VS Code", lambda: _install_vscode(pm)),
    ]

    print()
    for label, fn in tools:
        run_step(label, fn)

    print()
    print(f"  {GREEN}✓ Dev Essentials instalados!{NC}")
    print(f"  {GRAY}Reinicie o terminal para ativar nvm e Node.js.{NC}")
    pause()
