```
██╗    ██╗███████╗██╗     ██╗     ██████╗  ██████╗ ███╗   ██╗███████╗
██║    ██║██╔════╝██║     ██║     ██╔══██╗██╔═══██╗████╗  ██║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║  ██║██║   ██║██╔██╗ ██║█████╗
██║███╗██║██╔══╝  ██║     ██║     ██║  ██║██║   ██║██║╚██╗██║██╔══╝
╚███╔███╔╝███████╗███████╗███████╗██████╔╝╚██████╔╝██║ ╚████║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
               ░▒▓  D E V K I T  v2.1  L I N U X  ▓▒░
```

**Fork Linux do [WellDone DevKit](https://github.com/WellytonSdJ/welldone-devkit): instalador interativo de ambiente de desenvolvimento para qualquer distribuição Linux.**

---

## O que é?

**WellDone DevKit Linux** é um fork do projeto original (Windows/PowerShell) reescrito em Python para rodar em qualquer distribuição Linux. Mantém o visual cyberpunk neon, navegação por teclado e os mesmos módulos do original, adaptados e expandidos para o ecossistema Linux.

> Configure um PC do zero em minutos, sem abrir navegador.

---

## Requisitos

| Requisito | Detalhe |
|-----------|---------|
| Python | 3.10+ |
| Terminal | Com suporte a ANSI true-color |

Python 3 já vem instalado na maioria das distros modernas. Nenhuma dependência externa necessária.

---

## Distros suportadas

O script detecta automaticamente o package manager disponível e usa o correto para cada distro. Para apps que não estão nos repositórios oficiais, usa flatpak como fallback universal.

| Distro/família | Package manager |
|---|---|
| Arch, CachyOS, Manjaro | `pacman` |
| Arch (com AUR helper) | `yay` ou `paru` |
| Debian, Ubuntu, Mint, Pop!OS | `apt` |
| Fedora, RHEL, CentOS Stream | `dnf` / `yum` |
| openSUSE | `zypper` |
| Void Linux | `xbps-install` |
| Alpine Linux | `apk` |
| Qualquer distro (fallback) | `flatpak` |

---

## Instalação

```bash
git clone https://github.com/ChaoticNoodley/welldone-devkit
cd welldone-devkit
python3 welldone.py
```

---

## Módulos

### Dev Essentials

Instala as ferramentas base usando o PM nativo da sua distro:

- **git** — disponível em todas as distros
- **curl** e **wget** — disponível em todas as distros
- **nvm** — instalado via script oficial
- **Node.js LTS** — instalado via nvm
- **VS Code** — via AUR no Arch, flatpak nas demais

### Terminal Theme

- **Starship** — disponível no pacman, dnf, zypper e apk; script oficial como fallback
- **JetBrains Mono Nerd Font** — `ttf-jetbrains-mono-nerd` no Arch, `fonts-jetbrains-mono` no Debian/Ubuntu, download manual nas demais
- **Tema WellDone Neon** — paleta cyan `#00eaff` · pink `#ff00c8` · green `#0aff9d`

### Git Setup

Configura o Git globalmente: nome, email, branch padrão (`main`), editor (VS Code), `pull.rebase`, `core.autocrlf` e o alias `git lg` para log colorido.

### SSH Manager

Gera chaves SSH Ed25519 para o GitHub, inicia o `ssh-agent` automaticamente e copia a chave pública para o clipboard. Suporta `xclip`, `xsel` e `wl-copy` (X11 e Wayland).

### Pasta Inicial

Cria uma pasta de projetos e configura o terminal para abrir nela automaticamente. Edita `.bashrc`, `.zshrc` ou `config.fish` dependendo do shell detectado.

### Apps Opcionais

Menu de seleção múltipla. Tenta instalar pelo PM nativo da sua distro primeiro; usa flatpak como fallback. Para Epic Games e Hoppscotch você escolhe o método antes de instalar.

| App | Categoria | Disponibilidade nativa |
|---|---|---|
| Discord | Comunidade | AUR, Flatpak |
| Spotify | Música | AUR, Flatpak |
| Steam | Games | pacman, apt, dnf, zypper |
| Epic Games | Games | Heroic (AUR) ou Lutris (pacman, apt, dnf, zypper) |
| Postman | Dev Tools | AUR, Flatpak |
| Hoppscotch | Dev Tools | CLI npm / AppImage / .deb |
| Notion | Produtividade | AUR, Flatpak |
| Obsidian | Produtividade | pacman, dnf, AUR |
| Microsoft Teams | Trabalho | AUR, Flatpak |
| Opera GX | Browser | AUR, Flatpak |
| OpenClaude | Dev Tools | npm (Node.js instalado automaticamente se necessário) |

---

## Navegação da TUI

| Tecla | Ação |
|-------|------|
| `↑` / `W` | Item anterior |
| `↓` / `S` | Próximo item |
| `Enter` | Selecionar |
| `Espaço` | Marcar/desmarcar (multi-select) |
| `Q` | Sair / voltar |

---

## Estrutura do projeto

```
welldone-devkit/
├── welldone.py                      ← entrada principal (TUI)
└── scripts/
    ├── utils/
    │   ├── colors.py                ← paleta neon (ANSI true-color)
    │   ├── distro.py                ← detecção de distro e package manager
    │   └── ui.py                    ← engine TUI (painéis, menu, boot screen)
    └── modules/
        ├── install_dev_essentials.py
        ├── install_terminal_theme.py
        ├── setup_git.py
        ├── manage_ssh.py
        ├── setup_start_folder.py
        └── install_optional_apps.py
```

---

## Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feat/novo-modulo`
3. Commit: `git commit -m "feat: adiciona módulo X"`
4. Push: `git push origin feat/novo-modulo`
5. Abra um Pull Request

Para adicionar suporte a um novo package manager, edite `scripts/utils/distro.py` e adicione a entrada em `managers` e os pacotes em `PACKAGE_MAP`.

---

## Licença

MIT © [WellytonSdJ](https://github.com/WellytonSdJ)