<h1 align="center">⚙️ TLS Distributed Workers</h1>

<p align="center">
  <strong>TLS-secured distributed computing system with a client-coordinator-worker pipeline for parallel matrix operations</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/TLS%2FSSL-Secure-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/XML--RPC-Distributed-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white"/>
</p>

---

## 📖 About

A Blockchain / Distributed Systems project implementing a **secure distributed computation framework** using Python. A Coordinator node splits matrix computation tasks across multiple Worker nodes, all communicating over TLS-encrypted XML-RPC connections.

## ✨ Features

- 🔒 **TLS Encryption** — All node communication secured via SSL certificates
- 🗂️ **Task Distribution** — Coordinator splits matrix jobs across workers
- ➕ **Matrix Operations** — Distributed addition and multiplication
- 📡 **XML-RPC** — Remote procedure calls between nodes
- 📜 **Self-Signed Certs** — Auto-generated via `generate_cert.py`

## 🛠️ Tech Stack

| | |
|---|---|
| Language | Python |
| Communication | XML-RPC over TLS/SSL |
| Computation | NumPy |
| Security | OpenSSL (`pyOpenSSL`) |

## 🚀 Getting Started

```bash
git clone https://github.com/HamzaSaeed31/TLS-Distributed-Workers.git
cd TLS-Distributed-Workers

pip install pyopenssl numpy

# Step 1 — generate TLS certificate
python generate_cert.py

# Step 2 — start coordinator
python Coordinator.py

# Step 3 — start one or more workers (separate terminals)
python Worker.py

# Step 4 — run client to submit task
python Client.py
```

## 📐 Architecture

```
Client
  │── submit matrix task ──►  Coordinator
                                  │── subtask ──►  Worker 1
                                  │── subtask ──►  Worker 2
                                  │◄─ results ────  Workers
  │◄── final result ────────  Coordinator
```
