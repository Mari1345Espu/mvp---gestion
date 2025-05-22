import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Button,
  Chip,
  Divider,
  Alert,
  CircularProgress,
} from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';
import { proyectoService } from '../../services/proyectoService';
import { Proyecto } from '../../types';

const ProyectoDetalle: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [proyecto, setProyecto] = useState<Proyecto | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadProyecto();
  }, [id]);

  const loadProyecto = async () => {
    try {
      setLoading(true);
      const data = await proyectoService.getProyecto(id!);
      setProyecto(data);
    } catch (err) {
      setError('Error al cargar el proyecto');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('¿Está seguro de eliminar este proyecto?')) {
      try {
        await proyectoService.deleteProyecto(id!);
        navigate('/dashboard');
      } catch (err) {
        setError('Error al eliminar el proyecto');
      }
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!proyecto) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">Proyecto no encontrado</Alert>
      </Container>
    );
  }

  const canEdit = user?.rol === 'admin' || 
                 (user?.rol === 'lider' && proyecto.lider_id === user.id);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4" component="h1">
          {proyecto.titulo}
        </Typography>
        {canEdit && (
          <Box>
            <Button
              variant="contained"
              color="primary"
              onClick={() => navigate(`/proyectos/editar/${id}`)}
              sx={{ mr: 1 }}
            >
              Editar
            </Button>
            <Button
              variant="outlined"
              color="error"
              onClick={handleDelete}
            >
              Eliminar
            </Button>
          </Box>
        )}
      </Box>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="h6" gutterBottom>
              Información General
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Chip
                label={proyecto.estado.toUpperCase()}
                color={
                  proyecto.estado === 'aprobado' ? 'success' :
                  proyecto.estado === 'rechazado' ? 'error' :
                  proyecto.estado === 'en_progreso' ? 'primary' :
                  'default'
                }
                sx={{ mr: 1 }}
              />
              <Chip
                label={proyecto.tipo_proyecto.toUpperCase()}
                color="secondary"
              />
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Descripción
            </Typography>
            <Typography variant="body1" paragraph>
              {proyecto.descripcion}
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Objetivo
            </Typography>
            <Typography variant="body1" paragraph>
              {proyecto.objetivo}
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Metodología
            </Typography>
            <Typography variant="body1" paragraph>
              {proyecto.metodologia}
            </Typography>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography variant="subtitle1" gutterBottom>
              Resultados Esperados
            </Typography>
            <Typography variant="body1" paragraph>
              {proyecto.resultados_esperados}
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
          </Grid>

          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" gutterBottom>
              Presupuesto
            </Typography>
            <Typography variant="body1">
              ${proyecto.presupuesto}
            </Typography>
          </Grid>

          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" gutterBottom>
              Duración
            </Typography>
            <Typography variant="body1">
              {proyecto.duracion} meses
            </Typography>
          </Grid>

          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" gutterBottom>
              Área de Conocimiento
            </Typography>
            <Typography variant="body1">
              {proyecto.area_conocimiento}
            </Typography>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle1" gutterBottom>
              Palabras Clave
            </Typography>
            <Box>
              {proyecto.palabras_clave.split(',').map((keyword: string, index: number) => (
                <Chip
                  key={index}
                  label={keyword.trim()}
                  size="small"
                  sx={{ mr: 1, mb: 1 }}
                />
              ))}
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default ProyectoDetalle; 