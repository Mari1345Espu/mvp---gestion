import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Avatar,
  TextField,
  Button,
  Grid,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';
import { updateUserProfile, uploadAvatar } from '../../services/userService';
import { User } from '../../types';

const Perfil = () => {
  const { user } = useAuth();
  const [formData, setFormData] = useState<Partial<User>>({
    nombre: '',
    email: '',
    telefono: '',
  });
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        nombre: user.nombre || '',
        email: user.email || '',
        telefono: user.telefono || '',
      });
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAvatarFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      if (!user?.id) {
        throw new Error('Usuario no encontrado');
      }

      // Actualizar perfil
      await updateUserProfile(formData);

      // Subir avatar si se seleccionó uno
      if (avatarFile) {
        await uploadAvatar(avatarFile);
      }

      setSuccess('Perfil actualizado exitosamente');
    } catch (err) {
      setError('Error al actualizar el perfil');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <Container>
        <Alert severity="error">Usuario no encontrado</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ p: 3 }}>
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Avatar
            src={user.avatar_url}
            alt={user.nombre}
            sx={{ width: 120, height: 120, mx: 'auto', mb: 2 }}
          />
          <Typography variant="h6" gutterBottom>
            {user.nombre}
          </Typography>
          <Typography color="textSecondary" gutterBottom>
            {user.rol_nombre}
          </Typography>
          <Divider sx={{ my: 2 }} />
          <Button
            variant="outlined"
            component="label"
            sx={{ mt: 2 }}
          >
            Cambiar Avatar
            <input
              type="file"
              hidden
              accept="image/*"
              onChange={handleAvatarChange}
            />
          </Button>
        </Box>

        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                margin="normal"
                type="email"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Teléfono"
                name="telefono"
                value={formData.telefono}
                onChange={handleChange}
                margin="normal"
              />
            </Grid>
          </Grid>

          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mt: 2 }}>
              {success}
            </Alert>
          )}

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button
              variant="outlined"
              onClick={() => setFormData({
                nombre: user.nombre || '',
                email: user.email || '',
                telefono: user.telefono || '',
              })}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Guardar Cambios'}
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default Perfil; 