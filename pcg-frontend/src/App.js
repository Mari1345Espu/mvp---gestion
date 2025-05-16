import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import Usuarios from './pages/Usuarios';
import Home from './pages/Home';
import Login from './pages/Login';
import Roles from './pages/Roles';
import Permisos from './pages/Permisos';
import Estados from './pages/Estados';
import Convocatorias from './pages/Convocatorias';
import GrupoInvestigacion from './pages/GrupoInvestigacion';
import Dashboard from './pages/Dashboard';
import { AuthContext, AuthProvider } from './context/AuthContext';
import RoleBasedRoute from './components/RoleBasedRoute';

function PrivateRoute({ children }) {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? children : <Navigate to="/login" />;
}

function App() {
  const { auth, logout, isAuthenticated } = useContext(AuthContext);

  return (
    <Router>
      <nav className="navbar navbar-expand navbar-dark bg-dark">
        <div className="container">
          <Link className="navbar-brand" to="/">PCG Frontend</Link>
          <div className="navbar-nav">
            {!isAuthenticated && <Link className="nav-link" to="/login">Login</Link>}
          {isAuthenticated && (
              <>
                <Link className="nav-link" to="/usuarios">Usuarios</Link>
                <Link className="nav-link" to="/roles">Roles</Link>
                <Link className="nav-link" to="/permisos">Permisos</Link>
                <Link className="nav-link" to="/estados">Estados</Link>
                <Link className="nav-link" to="/convocatorias">Convocatorias</Link>
                <Link className="nav-link" to="/grupoinvestigacion">Grupos de Investigación</Link>
                <Link className="nav-link" to="/">Dashboard</Link>
                <button className="btn btn-link nav-link" onClick={logout}>Logout</button>
              </>
            )}
          </div>
        </div>
      </nav>
      <div className="container mt-4">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          } />
          <Route path="/usuarios" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI', 'Líder de Grupo']}>
              <Usuarios />
            </RoleBasedRoute>
          } />
          <Route path="/roles" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI']}>
              <Roles />
            </RoleBasedRoute>
          } />
          <Route path="/permisos" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI']}>
              <Permisos />
            </RoleBasedRoute>
          } />
          <Route path="/estados" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI']}>
              <Estados />
            </RoleBasedRoute>
          } />
          <Route path="/convocatorias" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI']}>
              <Convocatorias />
            </RoleBasedRoute>
          } />
          <Route path="/grupoinvestigacion" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI']}>
              <GrupoInvestigacion />
            </RoleBasedRoute>
          } />
          <Route path="/" element={
            <RoleBasedRoute allowedRoles={['Administrador CTI', 'Líder de Grupo', 'Investigador', 'Evaluador']}>
              <Dashboard />
            </RoleBasedRoute>
          } />
          {/* Add more routes here */}
        </Routes>
      </div>
    </Router>
  );
}

export default function AppWrapper() {
  return (
    <AuthProvider>
      <App />
    </AuthProvider>
  );
}
