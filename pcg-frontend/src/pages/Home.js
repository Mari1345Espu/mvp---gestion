import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="container-fluid p-0">
      {/* Hero Section */}
      <div className="bg-primary text-white py-5">
        <div className="container">
          <div className="row align-items-center">
            <div className="col-md-6">
              <h1 className="display-4 fw-bold mb-4">Sistema de Gestión de Investigación</h1>
              <p className="lead mb-4">
                Plataforma integral para la gestión de proyectos de investigación, 
                convocatorias y grupos de investigación de la institución.
              </p>
              <Link to="/login" className="btn btn-light btn-lg">
                Iniciar Sesión
              </Link>
            </div>
            <div className="col-md-6">
              <img 
                src="/images/research-illustration.svg" 
                alt="Investigación" 
                className="img-fluid"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = 'https://via.placeholder.com/600x400?text=Investigación';
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container py-5">
        <h2 className="text-center mb-5">Características Principales</h2>
        <div className="row g-4">
          <div className="col-md-4">
            <div className="card h-100 border-0 shadow-sm">
              <div className="card-body text-center">
                <i className="bi bi-calendar-check fs-1 text-primary mb-3"></i>
                <h3 className="h5 mb-3">Gestión de Convocatorias</h3>
                <p className="text-muted">
                  Administre convocatorias de investigación, siga su estado y gestione las propuestas.
                </p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card h-100 border-0 shadow-sm">
              <div className="card-body text-center">
                <i className="bi bi-people fs-1 text-success mb-3"></i>
                <h3 className="h5 mb-3">Grupos de Investigación</h3>
                <p className="text-muted">
                  Coordine grupos de investigación y gestione sus proyectos y actividades.
                </p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card h-100 border-0 shadow-sm">
              <div className="card-body text-center">
                <i className="bi bi-graph-up fs-1 text-info mb-3"></i>
                <h3 className="h5 mb-3">Seguimiento de Proyectos</h3>
                <p className="text-muted">
                  Monitoree el avance de los proyectos y gestione sus recursos eficientemente.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="bg-light py-5">
        <div className="container text-center">
          <h2 className="mb-4">¿Listo para comenzar?</h2>
          <p className="lead mb-4">
            Únase a nuestra comunidad de investigadores y comience a gestionar sus proyectos.
          </p>
          <Link to="/login" className="btn btn-primary btn-lg">
            Acceder al Sistema
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-dark text-white py-4">
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <h5>Sistema de Gestión de Investigación</h5>
              <p className="mb-0">
                Plataforma desarrollada para la gestión eficiente de proyectos de investigación.
              </p>
            </div>
            <div className="col-md-6 text-md-end">
              <p className="mb-0">
                © {new Date().getFullYear()} Todos los derechos reservados
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Home; 