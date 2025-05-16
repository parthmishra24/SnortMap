# SnortMap

**SnortMap** is a powerful and intuitive CLI tool for cybersecurity professionals to explore and simulate real-world attack vectors across multiple domains such as Web Applications, Active Directory, Cloud, and Mobile AppSec.

## 🚀 Features

- Domain-based attack navigation (Web, AD, Cloud, Mobile)
- Access level breakdown (No Access, User, Admin)
- Tool-specific suggestions with commands and reference links
- Beautiful Rich CLI interface
- Copy-to-clipboard support for commands
- Restart or Exit prompt after each interaction

## 📦 Installation

```bash
git clone https://github.com/parthmishra24/snortmap.git
```
```
cd snortmap
```
```
pip install -r requirements.txt
```
```
python -m cli.main
```

## 🧭 Usage

Follow the interactive prompts to:
- Select a domain (e.g., Active Directory)
- Choose your access level
- Select an attack vector
- View tools, commands, and references

## 📚 Example

```
? Select a domain to explore: Active Directory
? What is your access level in Active Directory? User Level
? Select an attack to explore further: Kerberoasting

───────────────────── Tool Info ─────────────────────
Tool     : Rubeus
Command  : Rubeus.exe kerberoast /user:targetuser /domain:example.com /rc4opsec
Link     : https://book.hacktricks.xyz/.../kerberoasting
```

## 📸 Demo Screenshots

### 🔷 Main Menu
![Main Menu](https://github.com/parthmishra24/snortmap/blob/main/screenshots/snortmap-menu.png)

### 🔧 Tool Panel
![Tool Panel](https://github.com/parthmishra24/snortmap/blob/main/screenshots/snortmap-tool-panel.png)

### 🔍 Search Result
![Search Result](https://github.com/parthmishra24/snortmap/blob/main/screenshots/snortmap-search-result.png)

### 🔁 Restart Option
![Restart Option](https://github.com/parthmishra24/snortmap/blob/main/screenshots/snortmap-start-over.png)

## 🧠 Knowledge Base Manager (manage_kb.py)

### Run:

```
python cli/manage_kb.py --add
python cli/manage_kb.py --edit
python cli/manage_kb.py --delete
```

### Add (--add)

- Select or create domain and access level

- Choose to select an existing attack or create a new one

- Add multiple tools for the same attack with commands and links

### Edit (--edit)

- Navigate by domain/access/attack

- Update description, command, or link of a specific tool

### Delete (--delete)

- Choose domain → access level → attack

- Decide whether to:

  - Delete the entire attack/vulnerability, or

  - Delete a specific tool under that attack

## 🤝 Contributing

Pull requests and suggestions are welcome!

---
Made with ❤️ by Parth Mishra
