"""
Detects the current Linux distribution and available package manager.
Supports: pacman, apt, dnf, yum, zypper, xbps-install, apk, flatpak
"""

import shutil
import subprocess
import sys
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
    """
    Returns a dict with:
      - name: friendly name
      - cmd: base command
      - install: install sub-command(s) as list
      - update: update db command(s) as list (can be None)
      - check: command to check if a package is installed
    """
    managers = [
        {
            "name": "pacman",
            "cmd": "pacman",
            "install": ["-S", "--noconfirm"],
            "update": ["-Sy"],
            "check": lambda pkg: _check_output(["pacman", "-Qi", pkg]),
        },
        {
            "name": "yay (AUR)",
            "cmd": "yay",
            "install": ["-S", "--noconfirm"],
            "update": ["-Sy"],
            "check": lambda pkg: _check_output(["yay", "-Qi", pkg]),
        },
        {
            "name": "paru (AUR)",
            "cmd": "paru",
            "install": ["-S", "--noconfirm"],
            "update": ["-Sy"],
            "check": lambda pkg: _check_output(["paru", "-Qi", pkg]),
        },
        {
            "name": "apt",
            "cmd": "apt",
            "install": ["install", "-y"],
            "update": ["update"],
            "check": lambda pkg: _check_output(["dpkg", "-s", pkg]),
        },
        {
            "name": "dnf",
            "cmd": "dnf",
            "install": ["install", "-y"],
            "update": ["check-update"],
            "check": lambda pkg: _check_output(["rpm", "-q", pkg]),
        },
        {
            "name": "yum",
            "cmd": "yum",
            "install": ["install", "-y"],
            "update": ["check-update"],
            "check": lambda pkg: _check_output(["rpm", "-q", pkg]),
        },
        {
            "name": "zypper",
            "cmd": "zypper",
            "install": ["install", "-y"],
            "update": ["refresh"],
            "check": lambda pkg: _check_output(["rpm", "-q", pkg]),
        },
        {
            "name": "xbps-install",
            "cmd": "xbps-install",
            "install": ["-Sy"],
            "update": ["-S"],
            "check": lambda pkg: _check_output(["xbps-query", pkg]),
        },
        {
            "name": "apk",
            "cmd": "apk",
            "install": ["add"],
            "update": ["update"],
            "check": lambda pkg: _check_output(["apk", "info", "-e", pkg]),
        },
    ]

    for mgr in managers:
        if shutil.which(mgr["cmd"]):
            return mgr

    # Fallback: flatpak
    if shutil.which("flatpak"):
        return {
            "name": "flatpak",
            "cmd": "flatpak",
            "install": ["install", "-y"],
            "update": ["update"],
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
    """Returns 'sudo' if available and needed, else empty string."""
    if shutil.which("sudo"):
        return "sudo"
    return ""


def install_package(pkg_name: str, pm: dict) -> bool:
    """Run install command for a given package. Returns True on success."""
    sudo = require_sudo()
    cmd = []
    if sudo:
        cmd.append(sudo)
    cmd.append(pm["cmd"])
    cmd.extend(pm["install"])
    cmd.append(pkg_name)

    result = subprocess.run(cmd)
    return result.returncode == 0


def update_db(pm: dict) -> bool:
    """Run package DB update. Returns True on success."""
    if not pm.get("update"):
        return True
    sudo = require_sudo()
    cmd = []
    if sudo:
        cmd.append(sudo)
    cmd.append(pm["cmd"])
    cmd.extend(pm["update"])
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


# Package name mapping per package manager
# Format: { "logical_name": { "pm_name": "actual_pkg_name" } }
PACKAGE_MAP = {
    "git": {
        "pacman": "git",
        "apt": "git",
        "dnf": "git",
        "yum": "git",
        "zypper": "git",
        "xbps-install": "git",
        "apk": "git",
    },
    "curl": {
        "pacman": "curl",
        "apt": "curl",
        "dnf": "curl",
        "yum": "curl",
        "zypper": "curl",
        "xbps-install": "curl",
        "apk": "curl",
    },
    "wget": {
        "pacman": "wget",
        "apt": "wget",
        "dnf": "wget",
        "yum": "wget",
        "zypper": "wget",
        "xbps-install": "wget",
        "apk": "wget",
    },
    "vscode": {
        "pacman": "code",          # AUR
        "yay (AUR)": "visual-studio-code-bin",
        "paru (AUR)": "visual-studio-code-bin",
        "apt": "code",             # requires microsoft repo
        "dnf": "code",
        "flatpak": "com.visualstudio.code",
    },
    "node": {
        # Installed via nvm — not the package manager
        "__nvm__": True,
    },
    "starship": {
        "pacman": "starship",
        "yay (AUR)": "starship",
        "apt": "starship",
        "dnf": "starship",
        "flatpak": "sh.starship.Starship",
        "__curl__": "https://starship.rs/install.sh",
    },
    "jetbrains-mono-nerd": {
        "pacman": "ttf-jetbrains-mono-nerd",
        "yay (AUR)": "ttf-jetbrains-mono-nerd",
        "paru (AUR)": "ttf-jetbrains-mono-nerd",
        "apt": "fonts-jetbrains-mono",
        "dnf": "jetbrains-mono-fonts",
        "__manual__": True,  # fallback: download from nerd fonts
    },
    "discord": {
        "pacman": "discord",
        "yay (AUR)": "discord",
        "apt": "discord",
        "flatpak": "com.discordapp.Discord",
    },
    "spotify": {
        "yay (AUR)": "spotify",
        "paru (AUR)": "spotify",
        "flatpak": "com.spotify.Client",
        "snap": "spotify",
    },
    "steam": {
        "pacman": "steam",
        "apt": "steam",
        "flatpak": "com.valvesoftware.Steam",
    },
    "postman": {
        "yay (AUR)": "postman-bin",
        "paru (AUR)": "postman-bin",
        "flatpak": "com.getpostman.Postman",
    },
    "notion": {
        "yay (AUR)": "notion-app-electron",
        "flatpak": "md.obsidian.Obsidian",  # closest flatpak alternative
    },
}


def resolve_package(logical: str, pm: dict) -> str | None:
    """Resolve logical package name to actual package name for detected PM."""
    mapping = PACKAGE_MAP.get(logical, {})
    return mapping.get(pm["name"]) or mapping.get(pm["cmd"])
