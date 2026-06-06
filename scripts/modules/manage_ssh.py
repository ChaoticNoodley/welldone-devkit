"""
SSH Manager — gera e gerencia chaves SSH Ed25519.
Equivalente Linux do manage_ssh.ps1.
"""

import subprocess
from pathlib import Path

from scripts.utils.colors import *
from scripts.utils.ui import ask, confirm, pause, run_step, show_module_header


def _start_ssh_agent():
    """Inicia o ssh-agent e retorna variáveis de ambiente."""
    result = subprocess.run(
        ["bash", "-c", "eval $(ssh-agent -s) && echo $SSH_AUTH_SOCK && echo $SSH_AGENT_PID"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def _copy_to_clipboard(text: str) -> bool:
    """Tenta copiar texto para o clipboard (xclip, xsel ou wl-copy)."""
    for cmd in [["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"], ["wl-copy"]]:
        try:
            result = subprocess.run(cmd, input=text, text=True, capture_output=True)
            if result.returncode == 0:
                return True
        except FileNotFoundError:
            continue
    return False


def run(pm: dict):
    show_module_header("GERENCIADOR SSH")

    ssh_dir  = Path.home() / ".ssh"
    key_file = ssh_dir / "id_ed25519"
    pub_file = key_file.with_suffix(".pub")

    print()

    if pub_file.exists():
        pub = pub_file.read_text().strip()
        print(f"  {GREEN}✓ Chave SSH existente encontrada:{NC}")
        print()
        print(f"  {CYAN}Chave pública:{NC}")
        print(f"  {GRAY}{pub}{NC}")
        print()
        print(f"  {YELLOW}Adicione em: {WHITE}https://github.com/settings/ssh/new{NC}")
        print()

        if not confirm("Deseja gerar uma nova chave (sobrescreve a atual)?"):
            if confirm("Copiar chave para o clipboard?"):
                if _copy_to_clipboard(pub):
                    print(f"  {GREEN}✓ Chave copiada para o clipboard!{NC}")
                else:
                    print(f"  {YELLOW}Clipboard não disponível. Copie manualmente acima.{NC}")
            pause()
            return

    email = ask("Email para a chave SSH (ex: seu@email.com)")
    if not email:
        print(f"  {RED}Email não pode ser vazio.{NC}")
        pause()
        return

    ssh_dir.mkdir(mode=0o700, parents=True, exist_ok=True)

    steps = [
        ("Gerando chave Ed25519", lambda: subprocess.run(
            ["ssh-keygen", "-t", "ed25519", "-C", email, "-f", str(key_file), "-N", ""],
            capture_output=False
        ).returncode == 0),
        ("Iniciando ssh-agent",   _start_ssh_agent),
        ("Adicionando chave ao agente", lambda: subprocess.run(
            ["bash", "-c", f"eval $(ssh-agent -s) && ssh-add {key_file}"]
        ).returncode == 0),
    ]

    for label, fn in steps:
        run_step(label, fn)

    print()
    print(f"  {GREEN}✓ Chave SSH gerada!{NC}")
    print()

    if pub_file.exists():
        pub = pub_file.read_text().strip()
        print(f"  {CYAN}Sua chave pública:{NC}")
        print(f"  {GRAY}{pub}{NC}")
        print()
        print(f"  {YELLOW}Adicione em: {WHITE}https://github.com/settings/ssh/new{NC}")
        print()

        if confirm("Copiar chave para o clipboard?"):
            if _copy_to_clipboard(pub):
                print(f"  {GREEN}✓ Chave copiada!{NC}")
            else:
                print(f"  {YELLOW}Clipboard não disponível (instale xclip, xsel ou wl-clipboard).{NC}")

    pause()
