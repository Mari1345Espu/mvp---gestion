import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Avatar,
  Box,
  Alert,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { userService } from '../../services/userService';
import { User } from '../../types';

interface ProfileFormData {
  nombre: string;
  email: string;
  telefono: string;
}

interface UpdateProfileRequest {
  id: number;
  data: ProfileFormData;
}

interface UploadAvatarRequest {
  id: number;
  file: File;
}

const Profile: React.FC = () => {
  const navigate = useNavigate();
  const { user, setUser } = useAuth();
  const [formData, setFormData] = useState({
    nombre: user?.nombre || '',
    email: user?.email || '',
    telefono: user?.telefono || '',
  });
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setAvatarFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    try {
      if (!user?.id) {
        throw new Error('Usuario no encontrado');
      }

      const updatedUser = await userService.updateUserProfile(formData);

      if (avatarFile) {
        const response = await userService.uploadAvatar(avatarFile);
        updatedUser.avatar_url = response.avatar_url;
      }

      setUser(updatedUser);
      setSuccess('Perfil actualizado exitosamente');
    } catch (err) {
      setError('Error al actualizar el perfil');
      console.error('Error:', err);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper sx={{ p: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Mi Perfil
        </Typography>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        {success && (
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        )}
        <form onSubmit={handleSubmit}>
          <Box display="flex" flexDirection="column" alignItems="center" mb={3}>
            <Avatar
              src={user?.avatar_url}
              alt={user?.nombre}
              sx={{ width: 100, height: 100, mb: 2 }}
            />
            <input
              accept="image/*"
              type="file"
              id="avatar-upload"
              hidden
              onChange={handleAvatarChange}
            />
            <label htmlFor="avatar-upload">
              <Button variant="outlined" component="span">
                Cambiar Foto
              </Button>
            </label>
          </Box>
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
          <Box sx={{ mt: 2 }}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
            >
              Guardar Cambios
            </Button>
          </Box>
        </form>
      </Paper>
    </Container>
  );
};

export default Profile; 