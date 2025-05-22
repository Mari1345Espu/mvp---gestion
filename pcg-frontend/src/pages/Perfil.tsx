import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  Grid,
  Avatar,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { userService } from '../services/userService';

const Perfil: React.FC = () => {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    nombre: '',
    email: '',
    telefono: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      setFormData({
        nombre: user.nombre,
        email: user.email,
        telefono: user.telefono || '',
      });
      if (user.avatar_url) {
        setPreviewUrl(user.avatar_url);
      }
    }
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    setLoading(true);

    try {
      await userService.updateUserProfile(formData);
      if (selectedFile) {
        await userService.uploadAvatar(selectedFile);
      }
      setSuccess(true);
    } catch (err) {
      setError('Error al actualizar el perfil. Por favor, intente nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h5" component="h1" gutterBottom>
            Perfil de Usuario
          </Typography>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Perfil actualizado exitosamente
            </Alert>
          )}
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} sx={{ textAlign: 'center' }}>
                <Box sx={{ position: 'relative', display: 'inline-block' }}>
                  <Avatar
                    src={previewUrl || undefined}
                    sx={{ width: 100, height: 100, mb: 2 }}
                  />
                  <input
                    accept="image/*"
                    type="file"
                    id="avatar-upload"
                    hidden
                    onChange={handleFileChange}
                  />
                  <label htmlFor="avatar-upload">
                    <Button
                      variant="outlined"
                      component="span"
                      size="small"
                      sx={{ position: 'absolute', bottom: 0, right: 0 }}
                    >
                      Cambiar
                    </Button>
                  </label>
                </Box>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Nombre Completo"
                  name="nombre"
                  value={formData.nombre}
                  onChange={handleChange}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Correo Electrónico"
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Teléfono"
                  name="telefono"
                  value={formData.telefono}
                  onChange={handleChange}
                  required
                />
              </Grid>
            </Grid>
            <Box sx={{ mt: 3 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={loading}
              >
                {loading ? 'Actualizando...' : 'Actualizar Perfil'}
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
};

export default Perfil; 