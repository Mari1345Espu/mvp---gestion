import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  CircularProgress,
  Alert,
  Chip,
  Avatar,
  Box,
} from '@mui/material';
import { getUsers } from '../../services/userService';
import { User } from '../../types';

const Usuarios: React.FC = () => {
  const navigate = useNavigate();
  const [usuarios, setUsuarios] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        const response = await getUsers();
        setUsuarios(response.content);
      } catch (err) {
        setError('Error al cargar los usuarios');
      } finally {
        setLoading(false);
      }
    };

    fetchUsuarios();
  }, []);

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Typography variant="h4" component="h1" gutterBottom>
            Usuarios
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/usuarios/nuevo')}
            sx={{ mb: 3 }}
          >
            Nuevo Usuario
          </Button>
        </Grid>
        {usuarios.map((usuario) => (
          <Grid item xs={12} sm={6} md={4} key={usuario.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar
                    src={usuario.avatar_url || usuario.foto}
                    alt={usuario.nombre}
                    sx={{ mr: 2 }}
                  />
                  <Box>
                    <Typography variant="h6">
                      {usuario.nombre} {usuario.apellido}
                    </Typography>
                    <Typography color="textSecondary">
                      {usuario.email || usuario.correo}
                    </Typography>
                  </Box>
                </Box>
                <Chip
                  label={usuario.rol}
                  color="primary"
                  size="small"
                  sx={{ mb: 2 }}
                />
                <Chip
                  label={usuario.activo ? 'Activo' : 'Inactivo'}
                  color={usuario.activo ? 'success' : 'default'}
                  size="small"
                  sx={{ ml: 1 }}
                />
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/usuarios/${usuario.id}`)}
                >
                  Ver Detalles
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Usuarios; 