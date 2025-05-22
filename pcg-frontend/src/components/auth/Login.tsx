import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Link,
  Alert,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      await login({
        email: formData.email,
        password: formData.password
      });
      const from = (location.state as any)?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    } catch (err) {
      setError('Credenciales inválidas');
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Box sx={{ mb: 3, textAlign: 'center' }}>
          <img 
            src="/logo.png" 
            alt="Logo" 
            style={{ 
              width: '120px', 
              height: '120px',
              filter: 'brightness(0) saturate(100%) invert(48%) sepia(79%) saturate(2476%) hue-rotate(118deg) brightness(118%) contrast(119%)'
            }} 
          />
          <Typography variant="h4" component="h1" gutterBottom>
            Bienvenido
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Ingresa tus credenciales para continuar
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit} style={{ width: '100%' }}>
          <TextField
            fullWidth
            label="Correo Electrónico"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Contraseña"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            margin="normal"
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            size="large"
            sx={{ mt: 3, mb: 2 }}
          >
            Iniciar Sesión
          </Button>
          <Box sx={{ textAlign: 'center' }}>
            <Link
              component="button"
              variant="body2"
              onClick={() => navigate('/register')}
            >
              ¿No tienes una cuenta? Regístrate
            </Link>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default Login; 