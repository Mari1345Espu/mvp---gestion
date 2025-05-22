import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { authService } from '../../services/authService';

const ResetPassword: React.FC = () => {
  const navigate = useNavigate();
  const { token } = useParams<{ token: string }>();
  const [formData, setFormData] = useState({
    newPassword: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    if (!token) {
      setError('Token de restablecimiento no válido');
      return;
    }

    if (formData.newPassword !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    try {
      await authService.resetPassword(token, formData.newPassword);
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setError('Error al restablecer la contraseña. Por favor, intente nuevamente.');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h5" component="h1" gutterBottom>
            Restablecer Contraseña
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Contraseña restablecida exitosamente
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              margin="normal"
              label="Nueva Contraseña"
              type="password"
              name="newPassword"
              value={formData.newPassword}
              onChange={handleChange}
              required
            />
            <TextField
              fullWidth
              margin="normal"
              label="Confirmar Nueva Contraseña"
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
            <Box sx={{ mt: 3 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
              >
                Restablecer Contraseña
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default ResetPassword; 