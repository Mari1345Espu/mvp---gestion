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
import { getProgramas } from '../../services/programaService';
import { Programa } from '../../types';

const Programas: React.FC = () => {
  const navigate = useNavigate();
  const [programas, setProgramas] = useState<Programa[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProgramas = async () => {
      try {
        const response = await getProgramas();
        setProgramas(response.content);
      } catch (err) {
        setError('Error al cargar los programas');
      } finally {
        setLoading(false);
      }
    };

    fetchProgramas();
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
            Programas
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => navigate('/programas/nuevo')}
            sx={{ mb: 3 }}
          >
            Nuevo Programa
          </Button>
        </Grid>
        {programas.map((programa) => (
          <Grid item xs={12} sm={6} md={4} key={programa.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {programa.nombre}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                  Estado: {programa.estado}
                </Typography>
                <Typography variant="body2">
                  {programa.descripcion}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => navigate(`/programas/${programa.id}`)}
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

export default Programas; 