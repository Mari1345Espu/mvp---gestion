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
import { Link } from 'react-router-dom';
import { authService } from '../../services/authService';

const ForgotPassword: React.FC = () => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);

    try {
      await authService.forgotPassword(email);
      setSuccess(true);
    } catch (err) {
      setError('Error al solicitar el restablecimiento de contraseña. Por favor, intente nuevamente.');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h5" component="h1" gutterBottom>
            Recuperar Contraseña
          </Typography>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Ingrese su correo electrónico y le enviaremos instrucciones para restablecer su contraseña.
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Se han enviado las instrucciones a su correo electrónico.
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              margin="normal"
              label="Correo Electrónico"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <Box sx={{ mt: 3 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
              >
                Enviar Instrucciones
              </Button>
            </Box>
            <Box sx={{ mt: 2, textAlign: 'center' }}>
              <Link to="/login" style={{ textDecoration: 'none' }}>
                Volver al inicio de sesión
              </Link>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default ForgotPassword; 