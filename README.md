# 🦅 FALCON-C2 — Command & Control Framework

A red team Command and Control (C2) framework built for security research and penetration testing simulations. Designed to demonstrate real-world attack vectors in controlled environments.

> ⚠️ **Disclaimer:** This tool is built strictly for authorized security research, red team operations, and educational purposes. Do not use against systems you do not have explicit permission to test.

---

## What It Does

- Establishes encrypted communication between a C2 server and remote agents
- Supports concurrent multi-agent connections from a single control panel
- Executes remote tasks securely using AES-encrypted channels
- Simulates real-world attack vectors across 10+ test scenarios
- Built on Django MVC with a web-based admin interface

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Django (MVC) |
| Communication | Python Socket Programming |
| Encryption | AES Cryptography |
| Auth | JWT-based authentication |
| Frontend | HTML, CSS, JavaScript |

---

## Architecture
FALCON-C2/
├── app_admin/        # Admin panel and dashboard
├── app_auth/         # Authentication and JWT handling
├── app_team/         # Team/operator management
├── c2_api/           # Core C2 API endpoints
├── falcon_c2/        # Django project settings
├── payloads/         # Payload generation modules
├── templates/        # HTML templates
└── generate_listeners.py  # Listener setup utility

---

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Siddhimudgal1417/FALCON-C2.git
cd FALCON-C2

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

---

## Key Features

- 🔐 AES-encrypted command and data channels
- 🖥️ Web-based C2 dashboard for operator control
- 👥 Multi-agent concurrent connection support
- 🔑 JWT-based operator authentication
- 📡 Listener generation via `generate_listeners.py`
- 🧪 Tested across 10+ simulated attack scenarios

---

## Skills Demonstrated

`Python` `Django` `Socket Programming` `AES Cryptography` `JWT Auth` `OOP` `MVC Architecture` `REST APIs` `Cybersecurity`

---

## Author

**Siddhi Mudgal** · [LinkedIn](https://www.linkedin.com/in/https://www.linkedin.com/in/siddhi-mudgal/) · [GitHub](https://github.com/Siddhimudgal1417)
