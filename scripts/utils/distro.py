"""
Detects the current Linux distribution and available package manager.
Supports: pacman, yay, paru, apt, dnf, yum, zypper, xbps-install, apk, flatpak
"""

import shutil
import subprocess
from pathlib import Path


def detect_distro() -> dict:
    """Read /etc/os-release and return distro info."""
    info = {}
    try:
        with open("/etc/os-release") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    info[k] = v.strip('"')
    except FileNotFoundError:
        pass
    return info


def detect_package_manager() -> dict | None:
    managers = [
        {
            "name": "yay (AUR)", "cmd": "yay",
            "install": ["-S", "--noconfirm"], "update": ["-Sy"],
            "check": lambda pkg: _check_output(["yay", "-Qi", pkg]),
        },
        {
            "name": "paru (AUR)", "cmd": "paru",
            "install": ["-S", "--noconfirm"], "update": ["-Sy"],
            "check": lambda pkg: _check_output(["paru", "-Qi", pkg]),
        },
        {
            "name": "pacman", "cmd": "pacman",
            "install": ["-S", "--noconfirm"], "update": ["-Sy"],
            "check": lambda pkg: _check_output(["pacman", "-Qi", pkg]),
        },
        {
            "name": "apt", "cmd": "apt",
            "install": ["install", "-y"], "update": ["update"],
            "check": lambda pkg: _check_output(["dpkg", "-s", pkg]),
        },
        {
            "name": "dnf", "cmd": "dnf",
            "install": ["install", "-y"], "update": ["check-update"],
            "check": lambda pkg: _check_output(["rpm", "-q", pkg]),
        },
        {
            "name": "yum", "cmd": "yum",
            "install": ["install", "-y"], "update": ["check-update"],
            "check": lambda pkg: _check_output(["rpm", "-q", pkg]),
        },
        {
            "name": "zypper", "cmd": "zypper",
            "install": ["install", "-y"], "update": ["refresh"],
            "check": lambda pkg: _check_output(["rpm", "-q", pkg]),
        },
        {
            "name": "xbps-install", "cmd": "xbps-install",
            "install": ["-Sy"], "update": ["-S"],
            "check": lambda pkg: _check_output(["xbps-query", pkg]),
        },
        {
            "name": "apk", "cmd": "apk",
            "install": ["add"], "update": ["update"],
            "check": lambda pkg: _check_output(["apk", "info", "-e", pkg]),
        },
    ]

    for mgr in managers:
        if shutil.which(mgr["cmd"]):
            return mgr

    if shutil.which("flatpak"):
        return {
            "name": "flatpak", "cmd": "flatpak",
            "install": ["install", "-y"], "update": ["update"],
            "check": lambda pkg: False,
        }

    return None


def _check_output(cmd: list) -> bool:
    try:
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    except Exception:
        return False


def require_sudo() -> str:
    return "sudo" if shutil.which("sudo") else ""


def install_package(pkg_name: str, pm: dict) -> bool:
    # Apenas PMs de sistema precisam de sudo
    # AUR helpers e flatpak gerenciam permissões internamente
    needs_sudo = pm["cmd"] in {"pacman", "apt", "dnf", "yum", "zypper", "xbps-install", "apk"}

    cmd = []
    if needs_sudo and require_sudo():
        cmd.append("sudo")
    cmd.append(pm["cmd"])
    cmd.extend(pm["install"])
    cmd.append(pkg_name)

    result = subprocess.run(cmd)
    return result.returncode == 0


def update_db(pm: dict) -> bool:
    if not pm.get("update"):
        return True
    needs_sudo = pm["cmd"] in {"pacman", "apt", "dnf", "yum", "zypper", "xbps-install", "apk"}
    cmd = []
    if needs_sudo and require_sudo():
        cmd.append("sudo")
    cmd.append(pm["cmd"])
    cmd.extend(pm["update"])
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


PACKAGE_MAP = {
    "git": {
        "pacman": "git", "apt": "git", "dnf": "git",
        "yum": "git", "zypper": "git", "xbps-install": "git", "apk": "git",
    },
    "curl": {
        "pacman": "curl", "apt": "curl", "dnf": "curl",
        "yum": "curl", "zypper": "curl", "xbps-install": "curl", "apk": "curl",
    },
    "wget": {
        "pacman": "wget", "apt": "wget", "dnf": "wget",
        "yum": "wget", "zypper": "wget", "xbps-install": "wget", "apk": "wget",
    },
    "vscode": {
        "yay (AUR)": "visual-studio-code-bin",
        "paru (AUR)": "visual-studio-code-bin",
        "flatpak": "com.visualstudio.code",
    },
    "starship": {
        "pacman": "starship",
        "yay (AUR)": "starship",
        "paru (AUR)": "starship",
        "dnf": "starship",
        "zypper": "starship",
        "apk": "starship",
        "flatpak": "sh.starship.Starship",
        "__curl__": "https://starship.rs/install.sh",
    },
    "jetbrains-mono-nerd": {
        "pacman": "ttf-jetbrains-mono-nerd",
        "yay (AUR)": "ttf-jetbrains-mono-nerd",
        "paru (AUR)": "ttf-jetbrains-mono-nerd",
        "apt": "fonts-jetbrains-mono",
        "dnf": "jetbrains-mono-fonts",
        "zypper": "jetbrains-mono-fonts",
        "__manual__": True,
    },
    "discord": {
        "yay (AUR)": "discord",
        "paru (AUR)": "discord",
        "flatpak": "com.discordapp.Discord",
    },
    "spotify": {
        "yay (AUR)": "spotify",
        "paru (AUR)": "spotify",
        "flatpak": "com.spotify.Client",
    },
    "steam": {
        "pacman": "steam",
        "apt": "steam",
        "dnf": "steam",
        "zypper": "steam",
        "flatpak": "com.valvesoftware.Steam",
    },
    "postman": {
        "yay (AUR)": "postman-bin",
        "paru (AUR)": "postman-bin",
        "flatpak": "com.getpostman.Postman",
    },
    "notion": {
        "yay (AUR)": "notion-app-electron",
        "paru (AUR)": "notion-app-electron",
        "flatpak": "io.notion.Notion",
    },
    "obsidian": {
        "pacman": "obsidian",
        "yay (AUR)": "obsidian",
        "paru (AUR)": "obsidian",
        "dnf": "obsidian",
        "flatpak": "md.obsidian.Obsidian",
    },
    "teams": {
        "yay (AUR)": "teams-for-linux",
        "paru (AUR)": "teams-for-linux",
        "flatpak": "com.github.IsmaelMartinez.teams_for_linux",
    },
    "opera-gx": {
        "yay (AUR)": "opera-gx",
        "paru (AUR)": "opera-gx",
        "flatpak": "com.opera.opera-gx",
    },
    "heroic": {
        "yay (AUR)": "heroic-games-launcher-bin",
        "paru (AUR)": "heroic-games-launcher-bin",
        "flatpak": "com.heroicgameslauncher.hgl",
    },
    "lutris": {
        "pacman": "lutris",
        "yay (AUR)": "lutris",
        "paru (AUR)": "lutris",
        "apt": "lutris",
        "dnf": "lutris",
        "zypper": "lutris",
        "flatpak": "net.lutris.Lutris",
    },
}


def resolve_package(logical: str, pm: dict) -> str | None:
    mapping = PACKAGE_MAP.get(logical, {})
    return mapping.get(pm["name"]) or mapping.get(pm["cmd"])