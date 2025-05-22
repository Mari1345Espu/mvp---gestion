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
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { RegisterData } from '../../types';

interface RegisterFormData {
  nombre: string;
  apellido: string;
  email: string;
  password: string;
  confirmPassword: string;
  telefono: string;
}

const Register: React.FC = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState<RegisterFormData>({
    nombre: '',
    apellido: '',
    email: '',
    password: '',
    confirmPassword: '',
    telefono: '',
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

    if (formData.password !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    try {
      const { confirmPassword, ...registerData } = formData;
      const registerPayload: RegisterData = {
        nombre: registerData.nombre,
        apellido: registerData.apellido,
        email: registerData.email,
        password: registerData.password,
        telefono: registerData.telefono,
        rol: 'investigador',
        rol_id: 1,
        estado_id: 1,
        activo: true,
        fecha_registro: new Date().toISOString(),
        ultima_sesion: new Date().toISOString()
      };
      await register(registerPayload);
      navigate('/login');
    } catch (err) {
      setError('Error al registrar usuario');
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
            Registro
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Crea tu cuenta para continuar
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
            label="Nombre"
            name="nombre"
            value={formData.nombre}
            onChange={handleChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Apellido"
            name="apellido"
            value={formData.apellido}
            onChange={handleChange}
            margin="normal"
            required
          />
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
            label="Teléfono"
            name="telefono"
            value={formData.telefono}
            onChange={handleChange}
            margin="normal"
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
          <TextField
            fullWidth
            label="Confirmar Contraseña"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
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
            Registrarse
          </Button>
          <Box sx={{ textAlign: 'center' }}>
            <Link
              component="button"
              variant="body2"
              onClick={() => navigate('/login')}
            >
              ¿Ya tienes una cuenta? Inicia sesión
            </Link>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default Register; 