"""
Git Setup — configura git globalmente.
Equivalente Linux do setup_git.ps1 (100% compatível, git config é cross-platform).
"""

import shutil
import subprocess

from scripts.utils.colors import *
from scripts.utils.ui import ask, confirm, pause, run_step, show_module_header


def run(pm: dict):
    show_module_header("CONFIGURAÇÃO DO GIT")

    if not shutil.which("git"):
        print(f"  {RED}✗ Git não encontrado. Execute 'Dev Essentials' primeiro.{NC}")
        pause()
        return

    # Show current config
    cur_name  = subprocess.run(["git", "config", "--global", "user.name"],
                                capture_output=True, text=True).stdout.strip()
    cur_email = subprocess.run(["git", "config", "--global", "user.email"],
                                capture_output=True, text=True).stdout.strip()

    print()
    if cur_name:
        print(f"  {GRAY}Configuração atual:{NC}")
        print(f"  {CYAN}Nome:  {WHITE}{cur_name}{NC}")
        print(f"  {CYAN}Email: {WHITE}{cur_email}{NC}")
        print()
        if not confirm("Deseja reconfigurar?"):
            pause()
            return

    print()
    name  = ask("Nome completo (ex: Wellyston Souza)")
    email = ask("Email do GitHub")

    if not name or not email:
        print(f"  {RED}Nome e email não podem ser vazios.{NC}")
        pause()
        return

    print()
    steps = [
        ("Configurando user.name",       lambda: subprocess.run(["git", "config", "--global", "user.name",  name])),
        ("Configurando user.email",      lambda: subprocess.run(["git", "config", "--global", "user.email", email])),
        ("Branch padrão → main",         lambda: subprocess.run(["git", "config", "--global", "init.defaultBranch", "main"])),
        ("Editor padrão → VS Code",      lambda: subprocess.run(["git", "config", "--global", "core.editor", "code --wait"])),
        ("Pull → rebase",                lambda: subprocess.run(["git", "config", "--global", "pull.rebase", "true"])),
        ("core.autocrlf → input (Linux)",lambda: subprocess.run(["git", "config", "--global", "core.autocrlf", "input"])),
        ("Alias: git lg (log bonito)",   lambda: subprocess.run([
            "git", "config", "--global", "alias.lg",
            "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
        ])),
    ]

    for label, fn in steps:
        run_step(label, lambda f=fn: f().returncode == 0)

    print()
    print(f"  {GREEN}✓ Git configurado com sucesso!{NC}")
    print(f"  {GRAY}Use {WHITE}git lg{GRAY} para um log colorido e compacto.{NC}")
    pause()
