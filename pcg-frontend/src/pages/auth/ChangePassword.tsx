import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  Alert,
} from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';

const ChangePassword: React.FC = () => {
  const navigate = useNavigate();
  const { user, changePassword } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    if (formData.newPassword !== formData.confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await changePassword(user.id, formData.currentPassword, formData.newPassword);
      setSuccess(true);
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      setError('Error al cambiar la contraseña');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Cambiar Contraseña
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Contraseña cambiada exitosamente
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <form onSubmit={handleSubmit}>
          <Box sx={{ mb: 3 }}>
            <TextField
              required
              fullWidth
              type="password"
              label="Contraseña Actual"
              name="currentPassword"
              value={formData.currentPassword}
              onChange={handleChange}
            />
          </Box>
          <Box sx={{ mb: 3 }}>
            <TextField
              required
              fullWidth
              type="password"
              label="Nueva Contraseña"
              name="newPassword"
              value={formData.newPassword}
              onChange={handleChange}
            />
          </Box>
          <Box sx={{ mb: 3 }}>
            <TextField
              required
              fullWidth
              type="password"
              label="Confirmar Nueva Contraseña"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
            />
          </Box>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading}
            >
              Cambiar Contraseña
            </Button>
            <Button
              variant="outlined"
              onClick={() => navigate('/dashboard')}
            >
              Cancelar
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default ChangePassword; 