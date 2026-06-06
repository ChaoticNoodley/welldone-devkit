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

**WellDone DevKit Linux** é um fork do projeto original (Windows/PowerShell) completamente reescrito em Python para rodar em qualquer distribuição Linux. Mantém o visual cyberpunk neon, navegação por teclado e os mesmos módulos, adaptados e expandidos para o ecossistema Linux.

> Configure um PC do zero em minutos, sem abrir navegador.

---

## Requisitos

| Requisito | Detalhe |
|-----------|---------|
| Python    | 3.10+   |
| Terminal  | Com suporte a ANSI true-color |

Python 3 já vem instalado na maioria das distros modernas. Nenhuma dependência externa necessária.

---

## Distros suportadas

| Distro/família               | Package manager detectado      |
|-----------------------------|-------------------------------|
| Arch, CachyOS, Manjaro       | `pacman` / `yay` / `paru`     |
| Debian, Ubuntu, Mint, Pop!OS | `apt`                         |
| Fedora, RHEL, CentOS Stream  | `dnf` / `yum`                 |
| openSUSE                     | `zypper`                      |
| Void Linux                   | `xbps-install`                |
| Alpine Linux                 | `apk`                         |
| Qualquer distro (fallback)   | `flatpak`                     |

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
Instala as ferramentas base de desenvolvimento:
- **git** — controle de versão
- **curl** / **wget** — transferência de dados
- **nvm** — gerenciador de versões do Node.js
- **Node.js LTS** — runtime JavaScript (via nvm)
- **VS Code** — editor de código (via PM nativo ou flatpak)

### Terminal Theme
Configura um terminal com visual cyberpunk neon:
- **Starship** — prompt moderno e rápido (equivalente ao Oh My Posh do original)
- **JetBrains Mono Nerd Font** — fonte com suporte a ícones
- **Tema WellDone Neon** — paleta cyan `#00eaff` · pink `#ff00c8` · green `#0aff9d`

### Git Setup
Configura o Git globalmente:
- Nome, email, branch padrão (`main`), editor (VS Code)
- `pull.rebase`, `core.autocrlf` e alias `git lg` (log colorido e compacto)

### SSH Manager
Gera e gerencia chaves SSH Ed25519 para o GitHub:
- Inicia o `ssh-agent` automaticamente
- Exibe e copia a chave pública para o clipboard
- Suporta `xclip`, `xsel` e `wl-copy` (X11 e Wayland)

### Pasta Inicial
Configura a pasta de abertura automática do terminal:
- Cria a pasta de projetos escolhida
- Adiciona o `cd` no `.bashrc`, `.zshrc` ou `config.fish`
- Todo novo terminal já abre direto na pasta de trabalho

### Apps Opcionais
Menu de seleção múltipla — instala via PM nativo ou flatpak:
- **Discord** — comunicação
- **Spotify** — música
- **Steam** — jogos
- **Postman** — cliente de API
- **Notion** — produtividade
- **OpenClaude** — interface open-source para Claude AI (via npm)

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
├── welldone.py                          ← entrada principal (TUI)
└── scripts/
    ├── utils/
    │   ├── colors.py                    ← paleta neon (ANSI true-color)
    │   ├── distro.py                    ← detecção de distro e package manager
    │   └── ui.py                        ← engine TUI (painéis, menu, boot screen)
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

Para adicionar suporte a um novo package manager, edite `scripts/utils/distro.py` — adicione a entrada em `managers` e mapeie os pacotes em `PACKAGE_MAP`.

---

## Licença

MIT © [WellytonSdJ](https://github.com/WellytonSdJ)
