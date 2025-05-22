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
import { getReportes } from '../../services/reporteService';
import { Reporte } from '../../types';

const Reportes: React.FC = () => {
  const navigate = useNavigate();
  const [reportes, setReportes] = useState<Reporte[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReportes = async () => {
      try {
        const response = await getReportes();
        setReportes(response.content);
      } catch (err) {
        setError('Error al cargar los reportes');
      } finally {
        setLoading(false);
      }
    };

    fetchReportes();
  }, []);

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
            Reportes
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/reportes/nuevo')}
            sx={{ mb: 3 }}
          >
            Nuevo Reporte
          </Button>
        </Grid>
        {reportes.map((reporte) => (
          <Grid item xs={12} sm={6} md={4} key={reporte.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {reporte.titulo}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Tipo: {reporte.tipo}
                </Typography>
                <Chip
                  label={reporte.estado || 'Sin estado'}
                  color={getEstadoColor(reporte.estado || '')}
                  size="small"
                  sx={{ mb: 2 }}
                />
                <Typography variant="body2">
                  {reporte.descripcion}
                </Typography>
                <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                  Autor: {reporte.usuario?.nombre || 'No asignado'}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/reportes/${reporte.id}`)}
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

export default Reportes; 