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
} from '@mui/material';
import { getExtensiones } from '../../services/extensionService';
import { Extension } from '../../types';

const Extensiones: React.FC = () => {
  const navigate = useNavigate();
  const [extensiones, setExtensiones] = useState<Extension[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchExtensiones = async () => {
      try {
        const response = await getExtensiones();
        setExtensiones(response.content);
      } catch (err) {
        setError('Error al cargar las extensiones');
      } finally {
        setLoading(false);
      }
    };

    fetchExtensiones();
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
            Extensiones
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/extensiones/nueva')}
            sx={{ mb: 3 }}
          >
            Nueva Extensión
          </Button>
        </Grid>
        {extensiones.map((extension) => (
          <Grid item xs={12} sm={6} md={4} key={extension.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {extension.nombre}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Tipo: {extension.tipo}
                </Typography>
                <Chip
                  label={extension.activo ? 'Activo' : 'Inactivo'}
                  color={extension.activo ? 'success' : 'default'}
                  size="small"
                  sx={{ mb: 2 }}
                />
                <Typography variant="body2">
                  {extension.descripcion}
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Duración: {extension.duracion} horas
                </Typography>
                <Typography variant="caption" display="block">
                  Modalidad: {extension.modalidad}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/extensiones/${extension.id}`)}
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

export default Extensiones; 