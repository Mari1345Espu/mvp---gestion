import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import AuthLayout from '../layouts/AuthLayout';
import MainLayout from '../layouts/MainLayout';

// Páginas públicas
import Home from '../pages/Home';
import Login from '../pages/auth/Login';
import Register from '../pages/auth/Register';
import ForgotPassword from '../pages/auth/ForgotPassword';
import ResetPassword from '../pages/auth/ResetPassword';

// Páginas protegidas
import Dashboard from '../pages/dashboard/Dashboard';
import ProyectoDetalle from '../pages/dashboard/ProyectoDetalle';
import ProyectoForm from '../pages/dashboard/ProyectoForm';
import Perfil from '../pages/dashboard/Perfil';

// Páginas de administrador
import AdminDashboard from '../pages/admin/Dashboard';
import AdminUsers from '../pages/admin/Users';
import AdminProjects from '../pages/admin/Projects';
import AdminLocations from '../pages/admin/Locations';
import AdminConvocatorias from '../pages/admin/Convocatorias';
import AdminEvaluators from '../pages/admin/Evaluators';
import AdminReports from '../pages/admin/Reports';
import AdminClosure from '../pages/admin/Closure';

// Páginas de líder de grupo
import GroupLeaderDashboard from '../pages/group-leader/GroupLeaderDashboard';
import GrupoInvestigacion from '../pages/group-leader/GrupoInvestigacion';

// Páginas de investigador
import ResearcherDashboard from '../pages/researcher/ResearcherDashboard';

// Páginas de evaluadores
import InternalEvaluatorDashboard from '../pages/internal-evaluator/InternalEvaluatorDashboard';
import ExternalEvaluatorDashboard from '../pages/external-evaluator/ExternalEvaluatorDashboard';

// Páginas de roles y permisos
import Roles from '../pages/roles/Roles';
import Permisos from '../pages/roles/Permisos';
import Estados from '../pages/roles/Estados';

// Componente para rutas protegidas
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
};

// Componente para rutas de admin
const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isAdmin, loading } = useAuth();

  if (loading) {
    return <div>Cargando...</div>;
  }

  if (!isAuthenticated || !isAdmin) {
    return <Navigate to="/" />;
  }

  return <>{children}</>;
};

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Rutas públicas */}
      <Route path="/" element={<Home />} />
      <Route
        path="/login"
        element={
          <AuthLayout>
            <Login />
          </AuthLayout>
        }
      />
      <Route
        path="/register"
        element={
          <AuthLayout>
            <Register />
          </AuthLayout>
        }
      />
      <Route
        path="/forgot-password"
        element={
          <AuthLayout>
            <ForgotPassword />
          </AuthLayout>
        }
      />
      <Route
        path="/reset-password/:token"
        element={
          <AuthLayout>
            <ResetPassword />
          </AuthLayout>
        }
      />

      {/* Rutas protegidas */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard/proyectos/:id"
        element={
          <ProtectedRoute>
            <ProyectoDetalle />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard/proyectos/nuevo"
        element={
          <AdminRoute>
            <ProyectoForm />
          </AdminRoute>
        }
      />
      <Route
        path="/dashboard/proyectos/editar/:id"
        element={
          <AdminRoute>
            <ProyectoForm />
          </AdminRoute>
        }
      />
      <Route
        path="/dashboard/perfil"
        element={
          <ProtectedRoute>
            <Perfil />
          </ProtectedRoute>
        }
      />

      {/* Rutas de administrador */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/users"
        element={
          <ProtectedRoute>
            <AdminUsers />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/projects"
        element={
          <ProtectedRoute>
            <AdminProjects />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/locations"
        element={
          <ProtectedRoute>
            <AdminLocations />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/convocatorias"
        element={
          <ProtectedRoute>
            <AdminConvocatorias />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/evaluators"
        element={
          <ProtectedRoute>
            <AdminEvaluators />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/reports"
        element={
          <ProtectedRoute>
            <AdminReports />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin/closure"
        element={
          <ProtectedRoute>
            <AdminClosure />
          </ProtectedRoute>
        }
      />

      {/* Rutas de líder de grupo */}
      <Route
        path="/group-leader"
        element={
          <ProtectedRoute>
            <GroupLeaderDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/group-leader/grupo"
        element={
          <ProtectedRoute>
            <GrupoInvestigacion />
          </ProtectedRoute>
        }
      />

      {/* Rutas de investigador */}
      <Route
        path="/researcher"
        element={
          <ProtectedRoute>
            <ResearcherDashboard />
          </ProtectedRoute>
        }
      />

      {/* Rutas de evaluadores */}
      <Route
        path="/internal-evaluator"
        element={
          <ProtectedRoute>
            <InternalEvaluatorDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/external-evaluator"
        element={
          <ProtectedRoute>
            <ExternalEvaluatorDashboard />
          </ProtectedRoute>
        }
      />

      {/* Rutas de roles y permisos */}
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

      {/* Ruta por defecto */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

export default AppRoutes; 