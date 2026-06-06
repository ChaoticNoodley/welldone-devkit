"""
Apps Opcionais — menu de seleção múltipla de apps via flatpak/PM.
Equivalente Linux do install_optional_apps.ps1.
"""

import shutil
import subprocess

from scripts.utils.colors import *
from scripts.utils.distro import install_package
from scripts.utils.ui import pause, run_step, show_module_header, term_width, draw_row, draw_divider, draw_bottom, B, PINK, NC


APPS = [
    {"id": "discord",    "label": "Discord",     "category": "Comunidade"},
    {"id": "spotify",    "label": "Spotify",      "category": "Música"},
    {"id": "steam",      "label": "Steam",        "category": "Games"},
    {"id": "postman",    "label": "Postman",      "category": "Dev Tools"},
    {"id": "notion",     "label": "Notion",       "category": "Produtividade"},
    {"id": "openclaude", "label": "OpenClaude",   "category": "Dev Tools"},
]

FLATPAK_IDS = {
    "discord": "com.discordapp.Discord",
    "spotify": "com.spotify.Client",
    "steam":   "com.valvesoftware.Steam",
    "postman": "com.getpostman.Postman",
    "notion":  "io.notion.Notion",
}

NATIVE_PKGS = {
    "steam": {"pacman": "steam", "apt": "steam"},
}


def _ensure_flatpak() -> bool:
    if not shutil.which("flatpak"):
        return False
    subprocess.run(
        ["flatpak", "remote-add", "--if-not-exists", "flathub",
         "https://flathub.org/repo/flathub.flatpakrepo"],
        capture_output=True
    )
    return True


def _install_via_flatpak(app_id: str) -> bool:
    flatpak_id = FLATPAK_IDS.get(app_id)
    if not flatpak_id:
        return False
    if not _ensure_flatpak():
        print(f"\n  {YELLOW}Flatpak não encontrado. Instale com:{NC}")
        print(f"  {WHITE}sudo apt install flatpak  {GRAY}# ou pacman -S flatpak{NC}\n")
        return False
    result = subprocess.run(["flatpak", "install", "-y", "flathub", flatpak_id])
    return result.returncode == 0


def _install_openclaude() -> bool:
    if not shutil.which("npm"):
        print(f"\n  {YELLOW}npm não encontrado. Instalando nvm + Node.js...{NC}\n")

        nvm = subprocess.run(
            ["bash", "-c",
             "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash"],
        )
        if nvm.returncode != 0:
            print(f"  {RED}✗ Falha ao instalar nvm.{NC}")
            return False

        node = subprocess.run(
            ["bash", "-c", "source ~/.nvm/nvm.sh && nvm install --lts && nvm use --lts"]
        )
        if node.returncode != 0:
            print(f"  {RED}✗ Falha ao instalar Node.js.{NC}")
            return False

    result = subprocess.run(
        ["bash", "-c",
         "source ~/.nvm/nvm.sh 2>/dev/null; "
         "npm install -g node-addon-api node-gyp && "
         "npm install -g @gitlawb/openclaude && "
         "sudo ln -sf $(source ~/.nvm/nvm.sh && which openclaude) /usr/local/bin/openclaude"]
    )
    return result.returncode == 0


def _install_app(app_id: str, pm: dict) -> bool:
    if app_id == "openclaude":
        return _install_openclaude()

    native = NATIVE_PKGS.get(app_id, {}).get(pm["cmd"])
    if native:
        return install_package(native, pm)

    return _install_via_flatpak(app_id)


def _multi_select_menu(apps: list) -> list:
    import sys, termios, tty

    selected = [False] * len(apps)
    cursor = 0

    def getch():
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

    while True:
        import os
        os.system("clear")
        w = term_width()

        from scripts.utils.ui import show_header, draw_top, draw_empty
        show_header("Apps Opcionais — selecione com [Espaço]")

        for i, app in enumerate(apps):
            is_cur = i == cursor
            is_sel = selected[i]

            check = f"{GREEN}[✓]{NC}" if is_sel else f"{GRAY}[ ]{NC}"
            cat   = f"{GRAY}{app['category']}{NC}"

            if is_cur:
                label = f"{BG_SELECT}{WHITE}{BOLD} {app['label']}{NC}"
            else:
                label = f"{WHITE} {app['label']}{NC}"

            draw_row(f"  {check} {label}  {cat}", w)

        draw_divider(w)
        draw_row(f"  {GRAY}[↑↓]  Navegar   [Espaço]  Selecionar   [Enter]  Instalar   [Q]  Cancelar{NC}", w)
        draw_bottom(w)

        key = getch()
        if key in ("\x1b[A", "w", "W"):
            cursor = (cursor - 1) % len(apps)
        elif key in ("\x1b[B", "s", "S"):
            cursor = (cursor + 1) % len(apps)
        elif key == " ":
            selected[cursor] = not selected[cursor]
        elif key in ("\r", "\n"):
            return [apps[i] for i, s in enumerate(selected) if s]
        elif key in ("q", "Q", "\x1b"):
            return []


def run(pm: dict):
    show_module_header("APPS OPCIONAIS")

    chosen = _multi_select_menu(APPS)

    if not chosen:
        print(f"  {GRAY}Nenhum app selecionado.{NC}")
        pause()
        return

    print()
    for app in chosen:
        run_step(f"Instalando {app['label']}", lambda a=app: _install_app(a["id"], pm))

    print()
    print(f"  {GREEN}✓ Apps instalados!{NC}")
    pause()