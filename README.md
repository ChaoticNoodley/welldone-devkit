```
██╗    ██╗███████╗██╗     ██╗     ██████╗  ██████╗ ███╗   ██╗███████╗
██║    ██║██╔════╝██║     ██║     ██╔══██╗██╔═══██╗████╗  ██║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║  ██║██║   ██║██╔██╗ ██║█████╗
██║███╗██║██╔══╝  ██║     ██║     ██║  ██║██║   ██║██║╚██╗██║██╔══╝
╚███╔███╔╝███████╗███████╗███████╗██████╔╝╚██████╔╝██║ ╚████║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝
               ░▒▓  D E V K I T  v2.0  L I N U X  ▓▒░
```

**Fork Linux do [WellDone DevKit](https://github.com/WellytonSdJ/welldone-devkit) — instalador interativo de ambiente de desenvolvimento para Linux.**

---

## O que é?

**WellDone DevKit Linux** é um fork do projeto original (Windows/PowerShell) reescrito em Python para rodar em qualquer distribuição Linux. Mantém o visual cyberpunk neon, navegação por teclado e os mesmos módulos, adaptados para o ecossistema Linux.

---

## Requisitos

| Requisito | Detalhe |
|-----------|---------|
| Python    | 3.10+   |
| Terminal  | Com suporte a ANSI true-color |

Python 3 já vem instalado na maioria das distros modernas. Nenhuma dependência externa necessária.

---

## Distros suportadas

| Distro/família               | Package manager detectado |
|-----------------------------|--------------------------|
| Arch, CachyOS, Manjaro       | `pacman` / `yay` / `paru` |
| Debian, Ubuntu, Mint, Pop!OS | `apt`                    |
| Fedora, RHEL, CentOS Stream  | `dnf` / `yum`            |
| openSUSE                     | `zypper`                 |
| Void Linux                   | `xbps-install`           |
| Alpine Linux                 | `apk`                    |
| Qualquer distro (fallback)   | `flatpak`                |

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/ChaoticNoodley/welldone-devkit
cd welldone-devkit

# Execute
python3 welldone.py
```

---

## Módulos

### Dev Essentials
Instala as ferramentas base:
- **git** — controle de versão
- **curl** / **wget** — transferência de dados
- **nvm** — gerenciador de versões do Node.js
- **Node.js LTS** — runtime JavaScript (via nvm)
- **VS Code** — editor de código (via PM nativo ou flatpak)

### Terminal Theme
Configura um terminal com visual cyberpunk neon:
- **Starship** — prompt moderno e rápido (equivalente ao Oh My Posh)
- **JetBrains Mono Nerd Font** — fonte com suporte a ícones
- **Tema WellDone Neon** — paleta cyan `#00eaff` · pink `#ff00c8` · green `#0aff9d`

### Git Setup
Configura o Git globalmente (nome, email, editor, aliases, etc.)

### SSH Manager
Gera e gerencia chaves SSH Ed25519 para o GitHub. Suporta cópia para clipboard via `xclip`, `xsel` ou `wl-copy`.

### Apps Opcionais
Menu de seleção múltipla com instalação via PM nativo ou flatpak:
- Discord, Spotify, Steam, Postman, Notion, OpenClaude

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
├── welldone.py                         ← entrada principal (TUI)
└── scripts/
    ├── utils/
    │   ├── colors.py                   ← paleta neon (ANSI true-color)
    │   ├── distro.py                   ← detecção de distro e package manager
    │   └── ui.py                       ← engine TUI (painéis, menu, boot screen)
    └── modules/
        ├── install_dev_essentials.py
        ├── install_terminal_theme.py
        ├── setup_git.py
        ├── manage_ssh.py
        └── install_optional_apps.py
```

---

## Contribuindo

1. Fork o repositório
2. Crie uma branch: `git checkout -b feat/novo-modulo`
3. Commit: `git commit -m "feat: adiciona módulo X"`
4. Push: `git push origin feat/novo-modulo`
5. Abra um Pull Request

Para adicionar suporte a um novo package manager, edite `scripts/utils/distro.py` — adicione a entrada em `managers` e mapeie os pacotes em `PACKAGE_MAP`.

---

## Licença

MIT © [WellytonSdJ](https://github.com/WellytonSdJ)
