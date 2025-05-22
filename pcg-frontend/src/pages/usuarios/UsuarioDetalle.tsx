import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Avatar,
  Chip,
  Grid,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { getUser } from '../../services/userService';
import { User } from '../../types';

const UsuarioDetalle: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [usuario, setUsuario] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsuario = async () => {
      try {
        if (!id) return;
        const data = await getUser(parseInt(id));
        setUsuario(data);
      } catch (err) {
        setError('Error al cargar los detalles del usuario');
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUsuario();
  }, [id]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !usuario) {
    return (
      <Container>
        <Alert severity="error" sx={{ mt: 2 }}>
          {error || 'Usuario no encontrado'}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Avatar
            src={usuario.avatar_url}
            alt={usuario.nombre}
            sx={{ width: 64, height: 64, mr: 2 }}
          />
          <Box>
            <Typography variant="h4" component="h1">
              {usuario.nombre}
            </Typography>
            <Typography color="textSecondary">
              {usuario.email}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip
            label={usuario.rol}
            color="primary"
          />
          <Chip
            label={usuario.estado_id === 1 ? 'Activo' : 'Inactivo'}
            color={usuario.estado_id === 1 ? 'success' : 'default'}
          />
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Información Personal
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Nombre
                </Typography>
                <Typography>{usuario.nombre}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Correo Electrónico
                </Typography>
                <Typography>{usuario.email}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Teléfono
                </Typography>
                <Typography>{usuario.telefono || 'No especificado'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Estado
                </Typography>
                <Typography>{usuario.estado_id === 1 ? 'Activo' : 'Inactivo'}</Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Información del Sistema
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Rol
                </Typography>
                <Typography>{usuario.rol}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Fecha de Creación
                </Typography>
                <Typography>
                  {new Date(usuario.fecha_registro).toLocaleDateString()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Última Actualización
                </Typography>
                <Typography>
                  {new Date(usuario.ultima_sesion).toLocaleDateString()}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate(`/usuarios/${usuario.id}/editar`)}
        >
          Editar Usuario
        </Button>
        <Button
          variant="outlined"
          onClick={() => navigate('/usuarios')}
        >
          Volver
        </Button>
      </Box>
    </Container>
  );
};

export default UsuarioDetalle; 