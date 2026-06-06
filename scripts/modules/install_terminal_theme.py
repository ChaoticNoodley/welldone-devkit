"""
Terminal Theme — instala Starship prompt + JetBrains Mono Nerd Font.
Equivalente Linux do install_terminal_theme.ps1 (usa Starship no lugar de Oh My Posh).
"""

import os
import shutil
import subprocess
from pathlib import Path

from scripts.utils.colors import *
from scripts.utils.distro import install_package, resolve_package
from scripts.utils.ui import confirm, pause, run_step, show_module_header

STARSHIP_CONFIG = """
# WellDone Neon — Starship theme
# Paleta: cyan #00eaff · pink #ff00c8 · green #0aff9d

format = \"\"\"
$os$username$directory$git_branch$git_status$nodejs$python$rust$cmd_duration
$character\"\"\"

right_format = \"$time\"

[character]
success_symbol = \"[›](bold #00eaff)\"
error_symbol   = \"[›](bold #ff0066)\"

[directory]
style            = \"bold #00eaff\"
truncation_length = 3
truncate_to_repo = true

[git_branch]
symbol = \" \"
style  = \"bold #ff00c8\"
format = \"[$symbol$branch]($style) \"

[git_status]
style  = \"bold #ffdd00\"
format = \"([$all_status$ahead_behind]($style) )\"

[nodejs]
symbol = \" \"
style  = \"bold #0aff9d\"
format = \"[$symbol($version )]($style)\"

[python]
symbol = \" \"
style  = \"bold #ffdd00\"
format = \"[$symbol($version )]($style)\"

[rust]
symbol = \"󱘗 \"
style  = \"bold #ff6600\"
format = \"[$symbol($version )]($style)\"

[cmd_duration]
min_time  = 2_000
style     = \"bold #888888\"
format    = \"[⏱ $duration]($style) \"

[time]
disabled   = false
style      = \"bold #666688\"
format     = \"[$time]($style)\"
time_format = \"%H:%M\"

[os]
disabled = false
style    = \"bold #ffffff\"

[username]
show_always = false
style_user  = \"bold #00eaff\"
format      = \"[$user]($style) in \"
"""


def _install_starship(pm: dict):
    if shutil.which("starship"):
        return True

    # Instalador de pacotes primeiro
    pkg = resolve_package("starship", pm)
    if pkg and not pkg.startswith("sh."):
        result = install_package(pkg, pm)
        if result:
            return True

    # Fallback
    print(f"  {GRAY}Instalando Starship via script oficial...{NC}")
    result = subprocess.run(
        ["bash", "-c", "curl -sS https://starship.rs/install.sh | sh -s -- -y"],
        capture_output=False
    )
    return result.returncode == 0


def _install_font(pm: dict):
    pkg = resolve_package("jetbrains-mono-nerd", pm)
    if pkg:
        return install_package(pkg, pm)

    # Manual download do fallback
    print(f"  {YELLOW}Baixando JetBrainsMono Nerd Font manualmente...{NC}")
    fonts_dir = Path.home() / ".local/share/fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.zip"
    tmp = "/tmp/JetBrainsMono.zip"
    r1 = subprocess.run(["curl", "-L", "-o", tmp, url])
    if r1.returncode != 0:
        return False
    r2 = subprocess.run(["unzip", "-o", tmp, "*.ttf", "-d", str(fonts_dir)])
    subprocess.run(["fc-cache", "-fv"], capture_output=True)
    return r2.returncode == 0


def _configure_starship():
    config_dir = Path.home() / ".config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "starship.toml"
    config_file.write_text(STARSHIP_CONFIG)
    return True


def _add_starship_to_shell():
    """Adds starship init to the detected shell's rc file."""
    shell = os.environ.get("SHELL", "")
    home = Path.home()

    configs = {
        "bash": (home / ".bashrc",    'eval "$(starship init bash)"'),
        "zsh":  (home / ".zshrc",     'eval "$(starship init zsh)"'),
        "fish": (home / ".config/fish/config.fish", "starship init fish | source"),
    }

    for sh, (rc, line) in configs.items():
        if sh in shell:
            content = rc.read_text() if rc.exists() else ""
            if "starship init" not in content:
                with rc.open("a") as f:
                    f.write(f"\n# WellDone DevKit — Starship prompt\n{line}\n")
            return True

    # Adiciona todos os arquivos rc comuns se o shell não for identificado
    for sh, (rc, line) in configs.items():
        if rc.exists():
            content = rc.read_text()
            if "starship init" not in content:
                with rc.open("a") as f:
                    f.write(f"\n# WellDone DevKit — Starship prompt\n{line}\n")
    return True


def run(pm: dict):
    show_module_header("TERMINAL THEME — STARSHIP + NERD FONT")

    print()
    steps = [
        ("Instalando Starship prompt",          lambda: _install_starship(pm)),
        ("Instalando JetBrains Mono Nerd Font", lambda: _install_font(pm)),
        ("Aplicando tema WellDone Neon",        _configure_starship),
        ("Configurando shell",                  _add_starship_to_shell),
    ]

    for label, fn in steps:
        run_step(label, fn)

    print()
    print(f"  {GREEN}✓ Tema aplicado!{NC}")
    print(f"  {GRAY}Configure a fonte {WHITE}JetBrainsMono Nerd Font{GRAY} no seu emulador de terminal.{NC}")
    print(f"  {GRAY}Reinicie o terminal para ver o Starship ativo.{NC}")
    pause()
