import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import dashboardService from '../services/dashboardService';

// Agregar Bootstrap Icons si están disponibles
// Si no, puedes agregarlos en tu index.html: 
// <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchDashboardData() {
      setLoading(true);
      setError(null);
      try {
        const data = await dashboardService.getDashboardData();
        setDashboardData(data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setError('Error al cargar los datos. Por favor, intente nuevamente.');
      }
      setLoading(false);
    }
    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{height: '60vh'}}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid py-4">
      <h2 className="mb-4 fw-bold">Dashboard Administrativo</h2>
      
      {error && (
        <div className="alert alert-danger alert-dismissible fade show" role="alert">
          {error}
          <button type="button" className="btn-close" onClick={() => setError(null)}></button>
        </div>
      )}

      <div className="row g-4">
        <div className="col-md-4">
          <Link to="/usuarios" className="text-decoration-none">
            <div className="card shadow border-0 h-100 hover-card">
              <div className="card-body d-flex align-items-center">
                <div className="me-3">
                  <i className="bi bi-people-fill fs-1 text-primary"></i>
                </div>
                <div>
                  <h5 className="card-title mb-1 text-dark">Usuarios</h5>
                  <h2 className="fw-bold mb-0 text-dark">{dashboardData?.stats?.usuarios || 0}</h2>
                  <p className="card-text text-muted">Total de usuarios registrados</p>
                </div>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-4">
          <Link to="/roles" className="text-decoration-none">
            <div className="card shadow border-0 h-100 hover-card">
              <div className="card-body d-flex align-items-center">
                <div className="me-3">
                  <i className="bi bi-person-badge-fill fs-1 text-success"></i>
                </div>
                <div>
                  <h5 className="card-title mb-1 text-dark">Roles</h5>
                  <h2 className="fw-bold mb-0 text-dark">{dashboardData?.stats?.roles || 0}</h2>
                  <p className="card-text text-muted">Total de roles definidos</p>
                </div>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-4">
          <Link to="/grupoinvestigacion" className="text-decoration-none">
            <div className="card shadow border-0 h-100 hover-card">
              <div className="card-body d-flex align-items-center">
                <div className="me-3">
                  <i className="bi bi-diagram-3-fill fs-1 text-info"></i>
                </div>
                <div>
                  <h5 className="card-title mb-1 text-dark">Grupos de Investigación</h5>
                  <h2 className="fw-bold mb-0 text-dark">{dashboardData?.stats?.grupos || 0}</h2>
                  <p className="card-text text-muted">Total de grupos de investigación</p>
                </div>
              </div>
            </div>
          </Link>
        </div>
      </div>

      <div className="row mt-4 g-4">
        <div className="col-md-6">
          <div className="card shadow border-0 h-100">
            <div className="card-header bg-white">
              <h5 className="card-title mb-0">Convocatorias Recientes</h5>
            </div>
            <div className="card-body">
              {dashboardData?.recientes?.convocatorias?.length > 0 ? (
                <div className="list-group list-group-flush">
                  {dashboardData.recientes.convocatorias.map((convocatoria) => (
                    <Link 
                      key={convocatoria.id} 
                      to={`/convocatorias/${convocatoria.id}`}
                      className="list-group-item list-group-item-action"
                    >
                      <div className="d-flex w-100 justify-content-between">
                        <h6 className="mb-1">{convocatoria.titulo}</h6>
                        <small className="text-muted">
                          {new Date(convocatoria.fecha_creacion).toLocaleDateString()}
                        </small>
                      </div>
                      <p className="mb-1 text-muted">{convocatoria.descripcion}</p>
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="text-muted">No hay convocatorias recientes</p>
              )}
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card shadow border-0 h-100">
            <div className="card-header bg-white">
              <h5 className="card-title mb-0">Proyectos Recientes</h5>
            </div>
            <div className="card-body">
              {dashboardData?.recientes?.proyectos?.length > 0 ? (
                <div className="list-group list-group-flush">
                  {dashboardData.recientes.proyectos.map((proyecto) => (
                    <Link 
                      key={proyecto.id} 
                      to={`/proyectos/${proyecto.id}`}
                      className="list-group-item list-group-item-action"
                    >
                      <div className="d-flex w-100 justify-content-between">
                        <h6 className="mb-1">{proyecto.titulo}</h6>
                        <small className="text-muted">
                          {new Date(proyecto.fecha_creacion).toLocaleDateString()}
                        </small>
                      </div>
                      <p className="mb-1 text-muted">{proyecto.descripcion}</p>
                    </Link>
                  ))}
                </div>
              ) : (
                <p className="text-muted">No hay proyectos recientes</p>
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="row mt-4 g-4">
        <div className="col-md-6">
          <Link to="/convocatorias" className="text-decoration-none">
            <div className="card shadow border-0 h-100 hover-card">
              <div className="card-body">
                <div className="d-flex align-items-center mb-3">
                  <i className="bi bi-calendar-event fs-1 text-warning me-3"></i>
                  <h5 className="card-title mb-0 text-dark">Convocatorias</h5>
                </div>
                <p className="card-text text-muted">Gestione las convocatorias activas y sus estados</p>
              </div>
            </div>
          </Link>
        </div>
        <div className="col-md-6">
          <Link to="/permisos" className="text-decoration-none">
            <div className="card shadow border-0 h-100 hover-card">
              <div className="card-body">
                <div className="d-flex align-items-center mb-3">
                  <i className="bi bi-shield-lock fs-1 text-danger me-3"></i>
                  <h5 className="card-title mb-0 text-dark">Permisos</h5>
                </div>
                <p className="card-text text-muted">Administre los permisos del sistema</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
