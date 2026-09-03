# FisioEffort-Studio-App 🏋️‍♂️

The app for the FisioEffort studio will be a useful tool for its administration. In this application, managers can check the number of enrolled children in each class, verify if a new student has already taken their free trial class, and confirm if students have made their monthly payments. All these requirements will be integrated into a modern and efficient app, accessible from multiple devices.

## 📊 Estado del Proyecto

| Módulo / Requerimiento | Tecnología Implementada | Estado Actual |
| :--- | :--- | :--- |
| **Infraestructura de Datos** | PostgreSQL | 🟢 Completado (Esquemas migrados y relacionales) |
| **Capa de API (CRUD)** | Django REST Framework | 🟢 Completado (ViewSets y Serializadores activos) |
| **Seguridad y Entorno** | Python `python-dotenv` | 🟢 Completado (Aislamiento de credenciales) |
| **Lógica de Reglas de Negocio** | Django Models / Views | 🟢 Completado (Filtros, Soft Delete, cálculo de cupos en tiempo real) |
| **Interfaz de Usuario (Cliente)** | Vue.js 3 + Vite | 🟢 Completado (Tema oscuro, reactividad, buscador integrado) |
| **Módulo de Pagos** | Django / Vue | 🟡 En progreso (Próximo objetivo: caja registradora) |

---

## 🚀 Guía de Instalación Local (Respaldo)

Para levantar el proyecto desde cero en cualquier equipo sin conflictos de dependencias:

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd FisioEffort-Studio-App
```

### 2. Configuración del Backend (Django)
Asegúrate de tener instalado Python y PostgreSQL.
```bash
# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1 

# 2. Instalar dependencias exactas
pip install -r requirements.txt

# 3. Aplicar migraciones a la base de datos
python manage.py migrate

# 4. Iniciar el servidor
python manage.py runserver
```
### 3. Configuración del Frontend (Vue + Vite)
En una nueva terminal, entra a la carpeta de fissioeffort-cliente.

```bash

# 1. Instalar dependencias (usando flag legacy para evitar conflictos estrictos de linting)
npm install --legacy-peer-deps

# 2. Levantar el servidor de desarrollo
npm run dev
```
