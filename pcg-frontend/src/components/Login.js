import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';
import logo from '../assets/logo.png';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Limpiar error anterior
    
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await axios.post('http://localhost:8000/api/v1/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        // Obtener el perfil del usuario y redirigir según el rol
        try {
          const profileRes = await axios.get('http://localhost:8000/usuarios/me', {
            headers: { Authorization: `Bearer ${response.data.access_token}` }
          });
          const rol = profileRes.data.rol_nombre;
          if (rol === 'Administrador') {
            navigate('/admin-dashboard');
          } else if (rol === 'Líder de Grupo') {
            navigate('/lider-dashboard');
          } else if (rol === 'Investigador') {
            navigate('/investigador-dashboard');
          } else if (rol === 'Evaluador') {
            navigate('/evaluador-dashboard');
          } else {
            navigate('/dashboard'); // ruta por defecto
          }
        } catch (profileErr) {
          setError('No se pudo obtener el perfil del usuario');
        }
      }
    } catch (err) {
      console.error('Error de login:', err);
      // Manejar diferentes tipos de errores
      if (err.response) {
        // Error de respuesta del servidor
        setError(err.response.data.detail || 'Error al iniciar sesión');
      } else if (err.request) {
        // Error de red
        setError('No se pudo conectar con el servidor');
      } else {
        // Otros errores
        setError('Error al iniciar sesión');
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="logo-container">
          <img src={logo} alt="Logo Universidad" className="logo" />
        </div>
        <h2>Iniciar Sesión</h2>
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Correo Electrónico</label>
            <input
              type="email"
              className="form-control"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              className="form-control"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" class="btn btn-success" className="btn-block">
            Ingresar
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login; 