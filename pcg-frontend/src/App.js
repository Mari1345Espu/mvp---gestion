import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Roles from './pages/Roles';
import Permisos from './pages/Permisos';
import Estados from './pages/Estados';
import Convocatorias from './pages/Convocatorias';
import GrupoInvestigacion from './pages/GrupoInvestigacion';
import Usuarios from './pages/Usuarios';
import Navbar from './components/Navbar';
import './App.css';

// Componente para rutas protegidas
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{height: '100vh'}}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Cargando...</span>
        </div>
      </div>
    );
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Componente principal envuelto en el Router
function AppContent() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="app-container">
      {isAuthenticated && <Navbar />}
      <div className="content-container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/roles" 
            element={
              <ProtectedRoute>
                <Roles />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/permisos" 
            element={
              <ProtectedRoute>
                <Permisos />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/estados" 
            element={
              <ProtectedRoute>
                <Estados />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/convocatorias" 
            element={
              <ProtectedRoute>
                <Convocatorias />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/grupoinvestigacion" 
            element={
              <ProtectedRoute>
                <GrupoInvestigacion />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/usuarios" 
            element={
              <ProtectedRoute>
                <Usuarios />
              </ProtectedRoute>
            } 
          />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </div>
  );
}

// Componente raíz que envuelve todo con los providers necesarios
function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App;
