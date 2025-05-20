import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Navbar() {
  const { isAuthenticated, auth, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar navbar-expand-lg" style={{ backgroundColor: '#28a745' }}>
      <div className="container">
        <Link className="navbar-brand text-white fw-bold" to="/">
          <i className="bi bi-journal-bookmark-fill me-2"></i>Observatorio UDEC
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            {isAuthenticated && (
              <>
                <li className="nav-item"><Link className="nav-link text-white" to="/usuarios">Usuarios</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/roles">Roles</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/permisos">Permisos</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/estados">Estados</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/convocatorias">Convocatorias</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/grupoinvestigacion">Grupos de Investigación</Link></li>
                <li className="nav-item"><Link className="nav-link text-white" to="/">Dashboard</Link></li>
              </>
            )}
          </ul>
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            {!isAuthenticated && (
              <li className="nav-item"><Link className="nav-link text-white" to="/login">Login</Link></li>
            )}
            {isAuthenticated && (
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle text-white d-flex align-items-center" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <i className="bi bi-person-circle fs-4 me-1"></i>
                  <span>{auth?.user?.username || 'Perfil'}</span>
                </a>
                <ul className="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                  <li><Link className="dropdown-item" to="/perfil"><i className="bi bi-person-lines-fill me-2"></i>Ver Perfil</Link></li>
                  <li><hr className="dropdown-divider" /></li>
                  <li><button className="dropdown-item text-danger" onClick={handleLogout}><i className="bi bi-box-arrow-right me-2"></i>Cerrar sesión</button></li>
                </ul>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar; 