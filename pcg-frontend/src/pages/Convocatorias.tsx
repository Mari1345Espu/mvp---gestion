import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  Chip,
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface Convocatoria {
  id: number;
  titulo: string;
  descripcion: string;
  fecha_inicio: string;
  fecha_fin: string;
  estado: string;
}

const Convocatorias: React.FC = () => {
  const [convocatorias, setConvocatorias] = useState<Convocatoria[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchConvocatorias();
  }, []);

  const fetchConvocatorias = async () => {
    try {
      const response = await fetch('/api/v1/convocatorias');
      const data = await response.json();
      setConvocatorias(data);
    } catch (error) {
      console.error('Error al cargar convocatorias:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerDetalles = (id: number) => {
    navigate(`/convocatorias/${id}`);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Convocatorias
      </Typography>
      <Grid container spacing={3}>
        {convocatorias.map((convocatoria) => (
          <Grid item xs={12} md={6} lg={4} key={convocatoria.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" component="h2" gutterBottom>
                  {convocatoria.titulo}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {convocatoria.descripcion}
                </Typography>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Chip
                    label={convocatoria.estado}
                    color={convocatoria.estado === 'Activa' ? 'success' : 'default'}
                  />
                  <Typography variant="caption" color="text.secondary">
                    {new Date(convocatoria.fecha_fin).toLocaleDateString()}
                  </Typography>
                </Box>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  color="primary"
                  onClick={() => handleVerDetalles(convocatoria.id)}
                >
                  Ver detalles
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Convocatorias; 