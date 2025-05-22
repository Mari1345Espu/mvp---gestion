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
} from '@mui/material';
import { getProyectos } from '../../services/proyectoService';
import { Proyecto } from '../../types';

const Proyectos: React.FC = () => {
  const navigate = useNavigate();
  const [proyectos, setProyectos] = useState<Proyecto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProyectos = async () => {
      try {
        const response = await getProyectos();
        setProyectos(response.content);
      } catch (err) {
        setError('Error al cargar los proyectos');
      } finally {
        setLoading(false);
      }
    };

    fetchProyectos();
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
            Proyectos
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/proyectos/nuevo')}
            sx={{ mb: 3 }}
          >
            Nuevo Proyecto
          </Button>
        </Grid>
        {proyectos.map((proyecto) => (
          <Grid item xs={12} sm={6} md={4} key={proyecto.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {proyecto.nombre}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Estado: {proyecto.estado}
                </Typography>
                <Typography variant="body2">
                  {proyecto.descripcion}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/proyectos/${proyecto.id}`)}
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

export default Proyectos; 