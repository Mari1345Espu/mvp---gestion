import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAuth?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requireAuth = true,
}) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (requireAuth && !Boolean(isAuthenticated)) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (!requireAuth && Boolean(isAuthenticated)) {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute; 