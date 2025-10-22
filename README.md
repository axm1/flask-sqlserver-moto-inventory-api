# 🏍️ Motorcycle Inventory API — Flask + SQL Server

A **RESTful API** built with **Flask (Python)** and **SQL Server**, designed to manage and query motorcycle inventory data such as brands, models, and availability by location.  
This project demonstrates secure backend development, database integration, and API design for a dealership or inventory system.

---

## 🚀 Features

- ✅ Built with **Flask** and **pyodbc** (SQL Server connection)
- 🔒 Basic token-based **authorization**
- 🌐 **CORS enabled** for frontend integration
- 📦 Structured REST API endpoints
- 🧠 Clear separation of concerns (routes, connection, config)
- 🧩 Easy to expand for CRUD or dashboard integration

---

## 🗂️ API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/preguntas_iniciales` | `GET` | Retrieve initial questions (demo data) |
| `/marcas` | `GET` | List all motorcycle brands |
| `/modelos_por_marcas?id_marca={id}` | `GET` | Get models by brand |
| `/ubicaciones` | `GET` | List all locations |
| `/disponibilidad_modelo_por_ubicacion?id_modelo={id}` | `GET` | Get availability count of each model per location |

🔐 **Authorization required:**  
Each request must include a valid token in the HTTP header:
```bash
Authorization: your_token_here
Python 3.12+

Flask

Flask-CORS

pyodbc

SQL Server

dotenv

Gunicorn (for production deployment)

Clone the repository

git clone https://github.com/axm1/flask-sqlserver-moto-inventory-api.git
cd flask-sqlserver-moto-inventory-a
