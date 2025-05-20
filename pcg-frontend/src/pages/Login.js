import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function Login() {
  const [form, setForm] = useState({ correo: '', contraseña: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Si ya está autenticado, redirigir al dashboard
    if (isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.correo === '' || form.contraseña === '') {
      setError('Por favor, complete todos los campos.');
      return;
    }
    
    setError('');
    setLoading(true);
    
    try {
      await login(form.correo, form.contraseña);
      // La redirección se manejará en el useEffect cuando isAuthenticated cambie
    } catch (err) {
      console.error('Error en login:', err);
      setError(err.response?.data?.detail || 'Error al iniciar sesión. Por favor, intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '400px' }}>
      <div className="card shadow-sm">
        <div className="card-body p-4">
          <h2 className="text-center mb-4">Iniciar Sesión</h2>
          {error && (
            <div className="alert alert-danger alert-dismissible fade show" role="alert">
              {error}
              <button type="button" className="btn-close" onClick={() => setError('')}></button>
            </div>
          )}
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label htmlFor="correo" className="form-label">Correo</label>
              <input
                type="email"
                id="correo"
                name="correo"
                className="form-control"
                value={form.correo}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
            <div className="mb-3">
              <label htmlFor="contraseña" className="form-label">Contraseña</label>
              <input
                type="password"
                id="contraseña"
                name="contraseña"
                className="form-control"
                value={form.contraseña}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
            <button 
              type="submit" 
              className="btn btn-primary w-100" 
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Iniciando sesión...
                </>
              ) : (
                'Ingresar'
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
