# 📁  Sistema de Gestión de Proyectos CTI - Universidad de Cundinamarca

Este sistema permite la gestión integral de proyectos de Ciencia, Tecnología e Innovación (CTI), facilitando el seguimiento, evaluación y control de los mismos. La plataforma permite múltiples roles (Administrador CTI, Investigador, Líder de grupo, Evaluador externo, Evaluador asesor, Superadministrador).

## 🚀 Características principales

- Registro y autenticación de usuarios con roles personalizados.
- Gestión de proyectos de investigación.
- Evaluación de proyectos con criterios y porcentaje mínimo de aprobación.
- Seguimiento de avances, cronogramas, productos, recursos y reportes.
- Módulos específicos para cada rol.
- Panel de administración para control general del sistema.
- Compatible con dispositivos móviles y escritorio.

##  Tecnologías utilizadas

- **Frontend:** React + TypeScript + Bootstrap
- **Backend:** Django + Django REST Framework
- **Base de datos:** PostgreSQL
- **Control de versiones:** Git + GitHub

##  Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/Mari1345Espu/mvp---gestion.git
cd mvp---gestion
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 3. Frontend

```bash
cd frontend/pcg-frontend
npm install
npm start
```

## 🧑‍💻 Roles y funcionalidades

| Rol               | Funcionalidades principales                                                                 |
|-------------------|---------------------------------------------------------------------------------------------|
| Investigador       | Crea proyectos, carga productos, avanza en cronograma.                                     |
| Líder de grupo     | Supervisa proyectos del grupo, puede enviar a evaluación.                                  |
| Evaluador externo  | Evalúa el proyecto con puntuación (≥75% para aprobación).                                  |
| Evaluador asesor   | Realiza evaluaciones parciales de los avances.                                             |
| Administrador CTI  | Administra usuarios, convoca proyectos, controla estados.                                  |
| Superadministrador | Accede a todos los módulos y gestiona todo el sistema.                                     |

## 📝 Licencia

Este proyecto es de uso académico para la Universidad de Cundinamarca. Todos los derechos reservados.
