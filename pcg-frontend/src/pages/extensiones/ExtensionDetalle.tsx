import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Button,
  CircularProgress,
  Alert,
  Box,
  Chip,
} from '@mui/material';
import { getExtension } from '../../services/extensionService';
import { Extension } from '../../types';

const ExtensionDetalle: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [extension, setExtension] = useState<Extension | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchExtension = async () => {
      try {
        if (!id) return;
        const data = await getExtension(parseInt(id));
        setExtension(data);
      } catch (err) {
        setError('Error al cargar la extensión');
      } finally {
        setLoading(false);
      }
    };

    fetchExtension();
  }, [id]);

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error || !extension) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Extensión no encontrada'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Button
          variant="outlined"
          onClick={() => navigate('/extensiones')}
          sx={{ mb: 2 }}
        >
          Volver a Extensiones
        </Button>
        <Typography variant="h4" component="h1" gutterBottom>
          {extension.nombre}
        </Typography>
        <Chip
          label={extension.activo ? 'Activo' : 'Inactivo'}
          color={extension.activo ? 'success' : 'default'}
          sx={{ mb: 2 }}
        />
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Descripción
            </Typography>
            <Typography paragraph>{extension.descripcion}</Typography>

            <Typography variant="h6" gutterBottom>
              Detalles
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Tipo
                </Typography>
                <Typography>{extension.tipo}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Duración
                </Typography>
                <Typography>{extension.duracion} horas</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Modalidad
                </Typography>
                <Typography>{extension.modalidad}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Programa
                </Typography>
                <Typography>
                  {extension.programa?.nombre || 'No asignado'}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Acciones
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => navigate(`/extensiones/${id}/editar`)}
              >
                Editar Extensión
              </Button>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => navigate(`/extensiones/${id}/participantes`)}
              >
                Ver Participantes
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ExtensionDetalle; 