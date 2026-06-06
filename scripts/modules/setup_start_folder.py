"""
Setup Start Folder — configura a pasta inicial do terminal.
"""

import os
import subprocess
import sys
import termios
from pathlib import Path

from scripts.utils.colors import *
from scripts.utils.ui import ask, pause, run_step, show_module_header


def run(pm: dict):
    show_module_header("PASTA INICIAL DO TERMINAL")

    print(f"  {CYAN}O que este módulo faz:{NC}")
    print(f"  {GRAY}1. Cria uma pasta de projetos no seu home{NC}")
    print(f"  {GRAY}2. Configura o terminal para abrir nela automaticamente{NC}")
    print(f"  {GRAY}3. Edita o arquivo de configuração do seu shell (.bashrc / .zshrc / fish){NC}")
    print()

    os.system("stty sane")
    termios.tcflush(sys.stdin, termios.TCIFLUSH)

    default = str(Path.home() / "Projetos")
    print(f"  {YELLOW}Pasta padrão sugerida: {WHITE}{default}{NC}")
    print(f"  {GRAY}(pressione Enter para aceitar ou digite outro caminho){NC}")
    print()

    folder = ask("Pasta inicial")
    if not folder:
        folder = default

    if len(folder) < 3 or not folder.startswith("/"):
        folder = default

    folder = os.path.expanduser(folder)

    print()
    print(f"  {CYAN}Configurando: {WHITE}{folder}{NC}")
    print()

    def criar_pasta():
        Path(folder).mkdir(parents=True, exist_ok=True)
        return True

    def configurar_shell():
        shell = os.environ.get("SHELL", "")
        home  = Path.home()
        line  = f"\n# WellDone: pasta inicial\ncd \"{folder}\"\n"

        configs = {
            "bash": home / ".bashrc",
            "zsh":  home / ".zshrc",
            "fish": home / ".config/fish/config.fish",
        }

        for sh, rc in configs.items():
            if sh in shell and rc.exists():
                content = rc.read_text()
                if "WellDone: pasta inicial" in content:
                    print(f"  {GRAY}  (shell já configurado anteriormente){NC}")
                    return True
                with rc.open("a") as f:
                    f.write(line)
                return True

        return False

    run_step("Criando pasta",      criar_pasta)
    run_step("Configurando shell", configurar_shell)

    print()
    print(f"  {GREEN}✓ Pronto!{NC}")
    print()
    print(f"  {GRAY}Pasta criada em:  {WHITE}{folder}{NC}")
    print(f"  {GRAY}Efeito ativo em:  {WHITE}novo terminal{NC}")
    print(f"  {GRAY}Para desfazer:    {WHITE}remova a linha 'cd \"{folder}\"' do seu .bashrc/.zshrc{NC}")
    print()
    pause()