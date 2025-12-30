<h1 align="center">⚔️ ServerSlayer</h1>
<h3 align="center">Kill Stray Development Servers • Free "Port in Use" Errors Instantly</h3>

<p align="center">
  <img src="https://img.shields.io/github/stars/supratikpm/ServerSlayer?style=for-the-badge&color=gold" alt="Stars">
  <img src="https://img.shields.io/badge/Works%20With-Antigravity%20%7C%20Cursor%20%7C%20Continue.dev-blueviolet?style=for-the-badge" alt="IDE Support">
  <img src="https://img.shields.io/badge/Safe-Never%20Kills%20DB%20%2F%20ngrok-green?style=for-the-badge" alt="Safe">
  <img src="https://img.shields.io/badge/Cross%20Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue?style=for-the-badge" alt="Cross Platform">
</p>

<p align="center">
  <strong>Portable AI agent to safely terminate stray localhost processes and free blocked ports.</strong><br>
  Works with <b>Node.js, Python/Django/Flask, Java/Spring Boot, Ruby/Rails, Go, PHP</b> and more.
</p>

---

## 🚨 The Problem: "Port Already in Use"

Every developer knows this pain:
```
Error: listen EADDRINUSE: address already in use :::3000
```

You forgot to stop a dev server. Now you're hunting PIDs manually. **Not anymore.**

---

## ✨ The Solution: One Slash Command

```
/killservers
```

That's it. ServerSlayer finds and safely kills stray development servers, idle localhost processes, and zombie dev servers — instantly.

---

## 🎯 Features

| Feature | Description |
| :--- | :--- |
| **Kill Stray Servers** | Terminate localhost processes blocking your ports |
| **Safe Port Killer** | Never kills databases, Docker, ngrok, or IDE processes |
| **Idle Server Detection** | Identifies unresponsive/zombie dev servers |
| **Cross-Platform** | Works on Windows, macOS, and Linux |
| **Multi-Framework** | Node.js, Python, Java, Ruby, Go, PHP support |
| **AI-Powered** | Slash commands work in Antigravity, Cursor, Continue.dev |

---

## 🚀 Quick Install

### For Antigravity / Cursor / Continue.dev / Windsurf

Copy the `.agent` folder to your project:

**Windows (PowerShell):**
```powershell
Copy-Item -Path "C:\Projects\ServerSlayer\.agent" -Destination ".\" -Recurse -Force
```

**macOS / Linux:**
```bash
cp -r /path/to/ServerSlayer/.agent ./
```

Done! Slash commands are now active.

---

## 📖 Slash Commands

| Command | What it does |
| :--- | :--- |
| `/listports` | 📋 List all running dev servers on localhost |
| `/killservers` | 🔪 Kill stray servers (graceful termination) |
| `/nukeports` | ☢️ Force kill all dev servers |
| `/killport 3000` | 🎯 Kill specific port |

---

<details>
<summary><b>📋 Cursor IDE Setup (.cursorrules)</b></summary>

Create `.cursorrules` in your project root:

```
You have access to ServerSlayer workflows in .agent/workflows/.
When the user mentions ports, servers, or "port in use" errors, suggest using:
- /listports - to see what's running
- /killservers - to safely kill dev servers
- /killport <port> - to kill a specific port
- /nukeports - for force kill

Always run the python script at .agent/tools/server_slayer_tools.py with appropriate arguments.
```

</details>

<details>
<summary><b>🤖 Claude / Any AI Assistant Setup</b></summary>

Add this to your system prompt:

```
You are equipped with ServerSlayer, a port management tool.

To list ports:
python .agent/tools/server_slayer_tools.py list

To kill servers (graceful):
python .agent/tools/server_slayer_tools.py kill --scope=project

To force kill:
python .agent/tools/server_slayer_tools.py kill --force --scope=project

To kill specific port:
python .agent/tools/server_slayer_tools.py kill --port 3000

SAFETY: Never kill ports 3306, 5432, 27017, 6379 (databases) or processes containing "ngrok", "docker", "vscode", "cursor".
```

</details>

---

## �️ Safety First: Protected Services

ServerSlayer **automatically protects** critical services:

| Category | Protected |
| :--- | :--- |
| **Databases** | MySQL (3306), PostgreSQL (5432), MongoDB (27017), Redis (6379), MSSQL (1433) |
| **Tunnels** | ngrok, SSH (22) |
| **IDE Processes** | Antigravity, VSCode, Cursor, JetBrains |
| **Containers** | Docker daemon |

---

## � Supported Frameworks

| Framework | Default Ports |
| :--- | :--- |
| **Node.js** (Next.js, Vite, CRA) | 3000, 3001, 5173 |
| **Python** (Django, Flask, FastAPI) | 8000, 5000 |
| **Java** (Spring Boot, Tomcat) | 8080 |
| **Ruby** (Rails) | 3000 |
| **Go** | 8080 |
| **PHP** | 8000 |

---

## 📁 Project Structure

```
.agent/                          # 👈 Copy this folder to any project
├── tools/
│   └── server_slayer_tools.py   # Core logic (cross-platform)
└── workflows/
    ├── listports.md             # /listports
    ├── killservers.md           # /killservers
    ├── killport.md              # /killport
    └── nukeports.md             # /nukeports
```

---

## 🤝 Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

**Help needed:**
- 🍎 macOS/Linux testing
- 🧩 More framework detection
- 🎬 Record a demo GIF

---

## ⭐ Star This Repo

If ServerSlayer saved you from "port already in use" hell:

<p align="center">
  <a href="https://github.com/supratikpm/ServerSlayer">
    <img src="https://img.shields.io/github/stars/supratikpm/ServerSlayer?style=for-the-badge&label=Star%20ServerSlayer&color=gold" alt="Star">
  </a>
</p>

---

## 🔍 Keywords

`kill stray servers` • `port already in use` • `terminate localhost processes` • `safe port killer` • `idle server killer` • `free blocked ports` • `dev server cleanup` • `antigravity ide` • `cursor rules` • `ai agent`

---

<p align="center">
  <strong>⚔️ Stray servers slain! Happy coding! 🚀</strong>
</p>

<p align="center">
  Made by <a href="https://github.com/supratikpm">@supratikpm</a>
</p>
