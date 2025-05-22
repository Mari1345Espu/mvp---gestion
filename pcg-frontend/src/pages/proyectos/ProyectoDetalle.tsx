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
} from '@mui/material';
import { getProyecto } from '../../services/proyectoService';
import { Proyecto } from '../../types';

const ProyectoDetalle: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [proyecto, setProyecto] = useState<Proyecto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProyecto = async () => {
      try {
        if (!id) return;
        const data = await getProyecto(parseInt(id));
        setProyecto(data);
      } catch (err) {
        setError('Error al cargar el proyecto');
      } finally {
        setLoading(false);
      }
    };

    fetchProyecto();
  }, [id]);

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error || !proyecto) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Proyecto no encontrado'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Button
          variant="outlined"
          onClick={() => navigate('/proyectos')}
          sx={{ mb: 2 }}
        >
          Volver a Proyectos
        </Button>
        <Typography variant="h4" component="h1" gutterBottom>
          {proyecto.nombre}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Descripción
            </Typography>
            <Typography paragraph>{proyecto.descripcion}</Typography>

            <Typography variant="h6" gutterBottom>
              Detalles
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Estado
                </Typography>
                <Typography>{proyecto.estado}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Responsable
                </Typography>
                <Typography>
                  {proyecto.responsable?.nombre || 'No asignado'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Fecha de Inicio
                </Typography>
                <Typography>
                  {new Date(proyecto.fechaInicio).toLocaleDateString()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Fecha de Fin
                </Typography>
                <Typography>
                  {new Date(proyecto.fechaFin).toLocaleDateString()}
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
                onClick={() => navigate(`/proyectos/${id}/editar`)}
              >
                Editar Proyecto
              </Button>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => navigate(`/proyectos/${id}/reportes`)}
              >
                Ver Reportes
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ProyectoDetalle; 