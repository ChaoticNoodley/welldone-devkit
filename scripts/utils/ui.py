"""
TUI engine — terminal UI with cyberpunk neon panels, menus, and helpers.
Mirrors the visual style of welldone-devkit's PowerShell ui.ps1.
"""

import os
import shutil
import sys
import termios
import tty
from typing import Callable

from scripts.utils.colors import *

# ─── Box drawing characters ────────────────────────────────────────────────────
B = {
    "TL": "╔", "TR": "╗", "BL": "╚", "BR": "╝",
    "H":  "═", "V":  "║",
    "TLs": "╟", "TRs": "╢", "Hs": "─",
    "ML": "╠", "MR": "╣", "MT": "╦", "MB": "╩", "MX": "╬",
}

LOGO = r"""
██╗    ██╗███████╗██╗     ██╗     ██████╗  ██████╗ ███╗   ██╗███████╗
██║    ██║██╔════╝██║     ██║     ██╔══██╗██╔═══██╗████╗  ██║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║  ██║██║   ██║██╔██╗ ██║█████╗
██║███╗██║██╔══╝  ██║     ██║     ██║  ██║██║   ██║██║╚██╗██║██╔══╝
╚███╔███╔╝███████╗███████╗███████╗██████╔╝╚██████╔╝██║ ╚████║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
               ░▒▓  D E V K I T  v2.0  L I N U X  ▓▒░
""".strip("\n")


# ─── Terminal size ─────────────────────────────────────────────────────────────

def term_width() -> int:
    return shutil.get_terminal_size((80, 24)).columns


def term_height() -> int:
    return shutil.get_terminal_size((80, 24)).lines


# ─── ANSI helpers ─────────────────────────────────────────────────────────────

def clear():
    print("\033[2J\033[H", end="", flush=True)


def visible_len(s: str) -> int:
    """Length of string without ANSI escape codes."""
    import re
    return len(re.sub(r"\033\[[0-9;]*[a-zA-Z]", "", s))


def pad_visible(s: str, width: int) -> str:
    vl = visible_len(s)
    return s + " " * max(0, width - vl)


def center_text(s: str, width: int) -> str:
    vl = visible_len(s)
    pad = max(0, (width - vl) // 2)
    return " " * pad + s


# ─── Box drawing helpers ───────────────────────────────────────────────────────

def draw_top(w: int):
    inner = w - 2
    print(f"{PINK}{B['TL']}{B['H'] * inner}{B['TR']}{NC}")


def draw_bottom(w: int):
    inner = w - 2
    print(f"{PINK}{B['BL']}{B['H'] * inner}{B['BR']}{NC}")


def draw_divider(w: int):
    inner = w - 2
    print(f"{PINK}{B['ML']}{B['H'] * inner}{B['MR']}{NC}")


def draw_row(content: str, w: int):
    inner = w - 2
    padded = pad_visible(content, inner)
    print(f"{PINK}{B['V']}{NC}{padded}{PINK}{B['V']}{NC}")


def draw_empty(w: int):
    draw_row("", w)


# ─── Header ───────────────────────────────────────────────────────────────────

def show_header(subtitle: str = ""):
    w = term_width()
    draw_top(w)
    for line in LOGO.split("\n"):
        draw_row(f"  {CYAN}{line}{NC}", w)
    draw_row("", w)
    if subtitle:
        draw_row(f"  {GRAY}{subtitle}{NC}", w)
    draw_divider(w)


# ─── Module header (used inside modules) ──────────────────────────────────────

def show_module_header(title: str):
    clear()
    w = term_width()
    draw_top(w)
    draw_row(f"  {BOLD}{CYAN}{title}{NC}", w)
    draw_divider(w)
    draw_empty(w)


# ─── Keyboard input ───────────────────────────────────────────────────────────

def getch() -> str:
    """Read a single keypress (raw mode)."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


# ─── Interactive menu ──────────────────────────────────────────────────────────

def show_menu(items: list[dict], subtitle: str = "") -> dict | None:
    """
    Renders a full-screen menu with arrow-key navigation.
    items: list of dicts with 'label' and 'action', or {'separator': True}
    Returns the selected item dict, or None if user pressed Q/Esc.
    """
    navigable = [i for i in items if not i.get("separator")]
    sel = 0

    while True:
        clear()
        w = term_width()
        show_header(subtitle)

        for idx, item in enumerate(items):
            if item.get("separator"):
                draw_row(f"  {GRAY}{'─' * 20}{NC}", w)
                continue

            nav_idx = navigable.index(item)
            is_sel = nav_idx == sel

            if is_sel:
                prefix = f"{BG_SELECT}{CYAN}{BOLD} › {NC}{BG_SELECT}{WHITE}{BOLD}"
                suffix = f"{NC}"
            else:
                prefix = f"{GRAY}   "
                suffix = NC

            draw_row(f"{prefix}{item['label']}{suffix}", w)

        draw_divider(w)
        draw_row(f"  {GRAY}[↑↓ / W S]  Navegar   [Enter]  Selecionar   [Q]  Sair{NC}", w)
        draw_bottom(w)

        key = getch()

        if key in ("\x1b[A", "w", "W"):   # up
            sel = (sel - 1) % len(navigable)
        elif key in ("\x1b[B", "s", "S"): # down
            sel = (sel + 1) % len(navigable)
        elif key in ("\r", "\n"):          # enter
            return navigable[sel]
        elif key in ("q", "Q", "\x1b"):   # quit
            return None


# ─── Step runner ──────────────────────────────────────────────────────────────

def run_step(label: str, fn: Callable) -> bool:
    """Runs a step, printing status. Returns True on success."""
    w = term_width()
    print(f"  {CYAN}▸ {WHITE}{label}...{NC}", end=" ", flush=True)
    try:
        result = fn()
        if result is False:
            print(f"{RED}✗{NC}")
            return False
        print(f"{GREEN}✓{NC}")
        return True
    except Exception as e:
        print(f"{RED}✗  ({e}){NC}")
        return False


# ─── Prompts ──────────────────────────────────────────────────────────────────

def confirm(question: str) -> bool:
    ans = input(f"  {YELLOW}? {WHITE}{question} {GRAY}[s/N]{NC} ").strip().lower()
    return ans in ("s", "y", "sim", "yes")


def pause():
    input(f"\n  {GRAY}Pressione Enter para continuar...{NC}")


def ask(prompt: str) -> str:
    return input(f"  {CYAN}› {WHITE}{prompt}: {NC}").strip()


# ─── Boot screen ──────────────────────────────────────────────────────────────

def show_boot_screen(distro_info: dict, pm_name: str):
    clear()
    w = term_width()
    draw_top(w)
    for line in LOGO.split("\n"):
        draw_row(f"  {CYAN}{line}{NC}", w)
    draw_empty(w)
    draw_divider(w)

    name = distro_info.get("PRETTY_NAME") or distro_info.get("NAME", "Linux")
    draw_row(f"  {GRAY}Distro detectada:{NC}  {WHITE}{name}{NC}", w)
    draw_row(f"  {GRAY}Package manager: {NC}  {GREEN}{pm_name}{NC}", w)
    draw_empty(w)
    draw_row(f"  {PINK}Bem-vindo ao WellDone DevKit — Linux Edition{NC}", w)
    draw_bottom(w)
    pause()
