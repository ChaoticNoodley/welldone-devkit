"""
Apps Opcionais — menu de seleção múltipla de apps via PM nativo ou flatpak.
Equivalente Linux do install_optional_apps.ps1.
"""

import os
import shutil
import subprocess
import sys
import termios
import tty

from scripts.utils.colors import *
from scripts.utils.distro import install_package
from scripts.utils.ui import (
    pause, run_step, show_module_header, term_width,
    draw_row, draw_divider, draw_bottom, draw_top, draw_empty,
    show_header, B, PINK, NC
)

# ─── App list ─────────────────────────────────────────────────────────────────

APPS = [
    {"id": "discord",    "label": "Discord",         "category": "Comunidade"},
    {"id": "spotify",    "label": "Spotify",          "category": "Música"},
    {"id": "steam",      "label": "Steam",             "category": "Games"},
    {"id": "epic",       "label": "Epic Games",        "category": "Games"},
    {"id": "postman",    "label": "Postman",           "category": "Dev Tools"},
    {"id": "hoppscotch", "label": "Hoppscotch",        "category": "Dev Tools"},
    {"id": "notion",     "label": "Notion",            "category": "Produtividade"},
    {"id": "obsidian",   "label": "Obsidian",          "category": "Produtividade"},
    {"id": "teams",      "label": "Microsoft Teams",   "category": "Trabalho"},
    {"id": "opera-gx",   "label": "Opera GX",          "category": "Browser"},
    {"id": "openclaude", "label": "OpenClaude",         "category": "Dev Tools"},
]

# ─── Package maps ─────────────────────────────────────────────────────────────

FLATPAK_IDS = {
    "discord":  "com.discordapp.Discord",
    "spotify":  "com.spotify.Client",
    "steam":    "com.valvesoftware.Steam",
    "postman":  "com.getpostman.Postman",
    "notion":   "io.notion.Notion",
    "obsidian": "md.obsidian.Obsidian",
    "teams":    "com.github.IsmaelMartinez.teams_for_linux",
    "opera-gx": "com.opera.opera-gx",
    # heroic e lutris têm ID próprio, tratados em _install_epic
    "heroic":   "com.heroicgameslauncher.hgl",
    "lutris":   "net.lutris.Lutris",
}

# Pacotes nativos por PM — apenas quando realmente disponíveis
NATIVE_PKGS = {
    "steam":    {"pacman": "steam", "apt": "steam"},
    "obsidian": {"pacman": "obsidian"},  # AUR
    "lutris":   {"pacman": "lutris", "apt": "lutris", "dnf": "lutris"},
    "heroic":   {"pacman": "heroic-games-launcher-bin"},  # AUR
    "opera-gx": {"pacman": "opera-gx"},  # AUR
    "teams":    {"pacman": "teams-for-linux"},  # AUR
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _ensure_flatpak() -> bool:
    if not shutil.which("flatpak"):
        print(f"\n  {YELLOW}Flatpak não encontrado. Instale com:{NC}")
        print(f"  {WHITE}sudo apt install flatpak  {GRAY}# ou pacman -S flatpak{NC}\n")
        return False
    subprocess.run(
        ["flatpak", "remote-add", "--if-not-exists", "flathub",
         "https://flathub.org/repo/flathub.flatpakrepo"],
        capture_output=True
    )
    return True


def _install_flatpak(flatpak_id: str) -> bool:
    if not _ensure_flatpak():
        return False
    result = subprocess.run(["flatpak", "install", "-y", "flathub", flatpak_id])
    return result.returncode == 0


def _install_native_or_flatpak(app_id: str, pm: dict) -> bool:
    """Tenta PM nativo primeiro, flatpak como fallback."""
    native = NATIVE_PKGS.get(app_id, {}).get(pm["cmd"])
    if native:
        return install_package(native, pm)
    flatpak_id = FLATPAK_IDS.get(app_id)
    if flatpak_id:
        return _install_flatpak(flatpak_id)
    return False


def _simple_choice_menu(title: str, options: list[str]) -> int:
    """
    Menu simples de escolha numerada.
    Retorna índice (0-based) da opção escolhida, ou -1 para cancelar.
    """
    os.system("stty sane")
    w = term_width()
    os.system("clear")
    draw_top(w)
    draw_row(f"  {BOLD}{CYAN}{title}{NC}", w)
    draw_divider(w)
    draw_empty(w)
    for i, opt in enumerate(options, 1):
        draw_row(f"  {GRAY}[{NC}{CYAN}{i}{NC}{GRAY}]{NC}  {WHITE}{opt}{NC}", w)
    draw_empty(w)
    draw_row(f"  {GRAY}[0]  Cancelar{NC}", w)
    draw_bottom(w)

    while True:
        try:
            ans = input(f"\n  {CYAN}›{NC} {WHITE}Opção: {NC}").strip()
            if ans == "0":
                return -1
            n = int(ans)
            if 1 <= n <= len(options):
                return n - 1
        except (ValueError, EOFError):
            pass
        print(f"  {RED}Opção inválida.{NC}")


# ─── Instaladores específicos ─────────────────────────────────────────────────

def _install_epic(pm: dict) -> bool:
    choice = _simple_choice_menu(
        "EPIC GAMES — escolha o launcher",
        [
            "Heroic Games Launcher  (focado em Epic / GOG)",
            "Lutris                 (gerenciador universal de jogos)",
            "Ambos",
        ]
    )
    if choice == -1:
        return False
    ok = True
    if choice in (0, 2):
        run_step("Instalando Heroic", lambda: _install_native_or_flatpak("heroic", pm))
    if choice in (1, 2):
        run_step("Instalando Lutris", lambda: _install_native_or_flatpak("lutris", pm))
    return ok


def _install_hoppscotch(pm: dict) -> bool:
    options = ["CLI via npm  (universal — requer Node.js)", "AppImage    (sem instalação)"]
    if pm["cmd"] == "apt":
        options.append(".deb        (Debian / Ubuntu / Mint)")

    choice = _simple_choice_menu("HOPPSCOTCH — escolha o método", options)

    if choice == -1:
        return False

    if choice == 0:
        if not shutil.which("npm"):
            print(f"\n  {YELLOW}npm não encontrado. Instalando Node.js via nvm...{NC}\n")
            r = subprocess.run(
                ["bash", "-c",
                 "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && "
                 "source ~/.nvm/nvm.sh && nvm install --lts && nvm use --lts"],
                capture_output=False
            )
            if r.returncode != 0:
                print(f"  {RED}✗ Falha ao instalar Node.js.{NC}")
                return False

        result = subprocess.run(
            ["bash", "-c", "source ~/.nvm/nvm.sh 2>/dev/null; npm install -g @hoppscotch/cli"]
        )
        return result.returncode == 0

    elif choice == 1:
        print(f"\n  {CYAN}Baixando AppImage do Hoppscotch...{NC}")
        dest = os.path.expanduser("~/Applications/Hoppscotch.AppImage")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        url = "https://github.com/hoppscotch/hoppscotch/releases/latest/download/Hoppscotch_linux_x64.AppImage"
        r = subprocess.run(["curl", "-L", "-o", dest, url])
        if r.returncode == 0:
            os.chmod(dest, 0o755)
            print(f"  {GREEN}✓ Salvo em {dest}{NC}")
            return True
        return False

    elif choice == 2:
        print(f"\n  {CYAN}Baixando .deb do Hoppscotch...{NC}")
        dest = "/tmp/Hoppscotch.deb"
        url = "https://github.com/hoppscotch/hoppscotch/releases/latest/download/Hoppscotch_linux_amd64.deb"
        r1 = subprocess.run(["curl", "-L", "-o", dest, url])
        if r1.returncode != 0:
            return False
        r2 = subprocess.run(["sudo", "apt", "install", "-y", dest])
        return r2.returncode == 0

    return False


ddef _install_openclaude() -> bool:
    if not shutil.which("npm"):
        print(f"\n  {YELLOW}npm não encontrado. Instalando Node.js via nvm...{NC}\n")
        r = subprocess.run(
            ["bash", "-c",
             "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && "
             "source ~/.nvm/nvm.sh && nvm install --lts && nvm use --lts"],
            capture_output=False
        )
        if r.returncode != 0:
            print(f"  {RED}✗ Falha ao instalar Node.js.{NC}")
            return False

    result = subprocess.run(
        ["bash", "-c", "source ~/.nvm/nvm.sh 2>/dev/null; npm install -g @gitlawb/openclaude"]
    )
    return result.returncode == 0


# ─── Dispatcher principal ─────────────────────────────────────────────────────

def _install_app(app_id: str, pm: dict) -> bool:
    if app_id == "openclaude":
        return _install_openclaude()
    if app_id == "epic":
        return _install_epic(pm)
    if app_id == "hoppscotch":
        return _install_hoppscotch(pm)

    # Todos os outros: PM nativo → flatpak
    return _install_native_or_flatpak(app_id, pm)


# ─── Multi-select menu ────────────────────────────────────────────────────────

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


def _multi_select_menu(apps: list) -> list:
    selected = [False] * len(apps)
    cursor = 0

    while True:
        os.system("clear")
        w = term_width()
        show_header("Apps Opcionais — selecione com [Espaço]")

        for i, app in enumerate(apps):
            is_cur = i == cursor
            is_sel = selected[i]
            check = f"{GREEN}[✓]{NC}" if is_sel else f"{GRAY}[ ]{NC}"
            cat   = f"{GRAY}{app['category']}{NC}"
            label = f"{BG_SELECT}{WHITE}{BOLD} {app['label']}{NC}" if is_cur else f"{WHITE} {app['label']}{NC}"
            draw_row(f"  {check} {label}  {cat}", w)

        draw_divider(w)
        draw_row(f"  {GRAY}[↑↓]  Navegar   [Espaço]  Selecionar   [Enter]  Instalar   [Q]  Cancelar{NC}", w)
        draw_bottom(w)

        key = _getch()
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


# ─── Entry point ──────────────────────────────────────────────────────────────

def run(pm: dict):
    show_module_header("APPS OPCIONAIS")

    chosen = _multi_select_menu(APPS)

    if not chosen:
        print(f"  {GRAY}Nenhum app selecionado.{NC}")
        pause()
        return

    print()
    for app in chosen:
        # Apps com sub-menu de escolha precisam de tratamento especial no run_step
        if app["id"] in ("epic", "hoppscotch"):
            print(f"\n  {CYAN}▸ {WHITE}{app['label']}...{NC}")
            _install_app(app["id"], pm)
        else:
            run_step(f"Instalando {app['label']}", lambda a=app: _install_app(a["id"], pm))

    print()
    print(f"  {GREEN}✓ Pronto!{NC}")
    pause()