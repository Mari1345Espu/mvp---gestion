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
import { getReporte } from '../../services/reporteService';
import { Reporte } from '../../types';

const ReporteDetalle: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [reporte, setReporte] = useState<Reporte | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReporte = async () => {
      try {
        if (!id) return;
        const data = await getReporte(parseInt(id));
        setReporte(data);
      } catch (err) {
        setError('Error al cargar el reporte');
      } finally {
        setLoading(false);
      }
    };

    fetchReporte();
  }, [id]);

  const getEstadoColor = (estado: string) => {
    switch (estado) {
      case 'borrador':
        return 'default';
      case 'en_revision':
        return 'warning';
      case 'aprobado':
        return 'success';
      case 'rechazado':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Container sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error || !reporte) {
    return (
      <Container sx={{ mt: 4 }}>
        <Alert severity="error">{error || 'Reporte no encontrado'}</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Button
          variant="outlined"
          onClick={() => navigate('/reportes')}
          sx={{ mb: 2 }}
        >
          Volver a Reportes
        </Button>
        <Typography variant="h4" component="h1" gutterBottom>
          {reporte.titulo}
        </Typography>
        <Chip
          label={reporte.estado || 'Sin estado'}
          color={getEstadoColor(reporte.estado || '')}
          sx={{ mb: 2 }}
        />
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Descripción
            </Typography>
            <Typography paragraph>{reporte.descripcion}</Typography>

            <Typography variant="h6" gutterBottom>
              Detalles
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Tipo
                </Typography>
                <Typography>{reporte.tipo}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Autor
                </Typography>
                <Typography>
                  {reporte.usuario?.nombre || 'No asignado'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Proyecto
                </Typography>
                <Typography>
                  {reporte.proyecto?.nombre || 'No asignado'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Fecha de Creación
                </Typography>
                <Typography>
                  {new Date(reporte.fecha_creacion).toLocaleDateString()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Última Actualización
                </Typography>
                <Typography>
                  {new Date(reporte.fecha_actualizacion).toLocaleDateString()}
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
                onClick={() => navigate(`/reportes/${id}/editar`)}
              >
                Editar Reporte
              </Button>
              <Button
                variant="outlined"
                color="primary"
                onClick={() => navigate(`/reportes/${id}/anexos`)}
              >
                Ver Anexos
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ReporteDetalle; 