"""
Dev Essentials — instala ferramentas base de desenvolvimento.
Equivalente Linux do install_dev_essentials.ps1
"""

import os
import shutil
import subprocess
import sys
import termios
import tty

from scripts.utils.colors import *
from scripts.utils.distro import install_package, resolve_package
from scripts.utils.ui import pause, run_step, show_module_header, term_width, draw_row, draw_divider, draw_bottom, draw_top, draw_empty, show_header


TOOLS = [
    {
        "id": "git",
        "label": "git",
        "desc": "Controle de versão",
    },
    {
        "id": "curl-wget",
        "label": "curl + wget",
        "desc": "Transferência de dados",
    },
    {
        "id": "nvm",
        "label": "nvm",
        "desc": "Gerenciador de versões do Node.js",
    },
    {
        "id": "node",
        "label": "Node.js LTS",
        "desc": "Runtime JavaScript (via nvm)",
    },
    {
        "id": "vscode",
        "label": "VS Code",
        "desc": "Editor de código",
    },
]


def _getch() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch += sys.stdin.read(2)
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def _select_tools() -> list:
    selected = [True] * len(TOOLS)
    cursor = 0

    while True:
        os.system("clear")
        w = term_width()
        show_header("Dev Essentials — selecione o que instalar")

        draw_empty(w)
        for i, tool in enumerate(TOOLS):
            is_cur = i == cursor
            is_sel = selected[i]
            check = f"{GREEN}[✓]{NC}" if is_sel else f"{GRAY}[ ]{NC}"
            desc  = f"{GRAY}{tool['desc']}{NC}"
            label = f"{BG_SELECT}{WHITE}{BOLD} {tool['label']}{NC}" if is_cur else f"{WHITE} {tool['label']}{NC}"
            draw_row(f"  {check} {label}  {desc}", w)

        draw_empty(w)
        draw_divider(w)
        draw_row(f"  {GRAY}[↑↓]  Navegar   [Espaço]  Marcar   [Enter]  Instalar   [Q]  Cancelar{NC}", w)
        draw_bottom(w)

        key = _getch()
        if key in ("\x1b[A", "w", "W"):
            cursor = (cursor - 1) % len(TOOLS)
        elif key in ("\x1b[B", "s", "S"):
            cursor = (cursor + 1) % len(TOOLS)
        elif key == " ":
            selected[cursor] = not selected[cursor]
        elif key in ("\r", "\n"):
            return [TOOLS[i] for i, s in enumerate(selected) if s]
        elif key in ("q", "Q", "\x1b"):
            return []


def _install_nvm():
    if shutil.which("nvm") or subprocess.run(
        ["bash", "-c", "source ~/.nvm/nvm.sh && nvm --version"],
        capture_output=True
    ).returncode == 0:
        print(f"  {GRAY}nvm já instalado, pulando.{NC}")
        return True
    result = subprocess.run(
        ["bash", "-c",
         "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"],
        capture_output=False
    )
    return result.returncode == 0


def _install_node_lts():
    result = subprocess.run(
        ["bash", "-c", "source ~/.nvm/nvm.sh && nvm install --lts && nvm use --lts"],
        capture_output=False
    )
    return result.returncode == 0


def _install_vscode(pm: dict):
    # Verifica se já está instalado
    if shutil.which("code") or shutil.which("codium") or shutil.which("code-insiders"):
        print(f"  {GRAY}VS Code já instalado, pulando.{NC}")
        return True

    pkg = resolve_package("vscode", pm)
    if pkg:
        return install_package(pkg, pm)
    if shutil.which("flatpak"):
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

    chosen = _select_tools()

    if not chosen:
        print(f"  {GRAY}Nenhuma ferramenta selecionada.{NC}")
        pause()
        return

    ids = {t["id"] for t in chosen}

    print()
    if "git" in ids:
        run_step("Instalando git", lambda: install_package(resolve_package("git", pm) or "git", pm))
    if "curl-wget" in ids:
        run_step("Instalando curl", lambda: install_package(resolve_package("curl", pm) or "curl", pm))
        run_step("Instalando wget", lambda: install_package(resolve_package("wget", pm) or "wget", pm))
    if "nvm" in ids:
        run_step("Instalando nvm", _install_nvm)
    if "node" in ids:
        run_step("Instalando Node.js LTS", _install_node_lts)
    if "vscode" in ids:
        run_step("Instalando VS Code", lambda: _install_vscode(pm))

    print()
    print(f"  {GREEN}✓ Dev Essentials instalados!{NC}")
    print(f"  {GRAY}Reinicie o terminal para ativar nvm e Node.js.{NC}")
    pause()