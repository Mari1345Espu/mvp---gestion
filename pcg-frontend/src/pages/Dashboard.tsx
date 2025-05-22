import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import {
  Assessment as AssessmentIcon,
  School as SchoolIcon,
  Group as GroupIcon,
  Assignment as AssignmentIcon,
  Event as EventIcon,
  Description as DescriptionIcon,
  People as PeopleIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { getProyectos } from '../services/proyectoService';
import { getProgramas } from '../services/programaService';
import { getReportes } from '../services/reporteService';
import { Proyecto, Programa, Reporte } from '../types';

interface Stats {
  proyectos: number;
  programas: number;
  reportes: number;
  participantes: number;
}

const getEstadoColor = (estadoId: number) => {
  switch (estadoId) {
    case 1:
      return 'success';
    case 2:
      return 'warning';
    case 3:
      return 'error';
    default:
      return 'default';
  }
};

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<Stats>({
    proyectos: 0,
    programas: 0,
    reportes: 0,
    participantes: 0,
  });
  const [recentProyectos, setRecentProyectos] = useState<Proyecto[]>([]);
  const [recentProgramas, setRecentProgramas] = useState<Programa[]>([]);
  const [recentReportes, setRecentReportes] = useState<Reporte[]>([]);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        const [proyectosRes, programasRes, reportesRes] = await Promise.all([
          getProyectos(),
          getProgramas(),
          getReportes(),
        ]);

        setStats({
          proyectos: proyectosRes.totalElements,
          programas: programasRes.totalElements,
          reportes: reportesRes.totalElements,
          participantes: 0, // TODO: Implementar cuando tengamos el servicio de participantes
        });

        // Actualizar listas recientes
        setRecentProyectos(proyectosRes.content);
        setRecentProgramas(programasRes.content);
        setRecentReportes(reportesRes.content);
      } catch (err) {
        setError('Error al cargar las estadísticas');
        console.error('Error:', err);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Bienvenido, {user?.nombre}
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              Proyectos
            </Typography>
            <Typography variant="h4">{stats.proyectos}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              Programas
            </Typography>
            <Typography variant="h4">{stats.programas}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              Reportes
            </Typography>
            <Typography variant="h4">{stats.reportes}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              Participantes
            </Typography>
            <Typography variant="h4">{stats.participantes}</Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Proyectos Recientes */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Proyectos Recientes</Typography>
          <Button onClick={() => navigate('/proyectos')}>Ver todos</Button>
        </Box>
        <Grid container spacing={2}>
          {recentProyectos.map((proyecto) => (
            <Grid item xs={12} sm={6} md={4} key={proyecto.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" noWrap>
                    {proyecto.nombre}
                  </Typography>
                  <Chip
                    label={proyecto.estado_id === 1 ? 'Activo' : 'Inactivo'}
                    color={getEstadoColor(proyecto.estado_id)}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => navigate(`/proyectos/${proyecto.id}`)}>
                    Ver detalles
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Programas Recientes */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Programas Recientes</Typography>
          <Button onClick={() => navigate('/programas')}>Ver todos</Button>
        </Box>
        <Grid container spacing={2}>
          {recentProgramas.map((programa) => (
            <Grid item xs={12} sm={6} md={4} key={programa.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" noWrap>
                    {programa.nombre}
                  </Typography>
                  <Chip
                    label={programa.estado_id === 1 ? 'Activo' : 'Inactivo'}
                    color={getEstadoColor(programa.estado_id)}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => navigate(`/programas/${programa.id}`)}>
                    Ver detalles
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Reportes Recientes */}
      <Paper sx={{ p: 2 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Reportes Recientes</Typography>
          <Button onClick={() => navigate('/reportes')}>Ver todos</Button>
        </Box>
        <Grid container spacing={2}>
          {recentReportes.map((reporte) => (
            <Grid item xs={12} sm={6} md={4} key={reporte.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" noWrap>
                    {reporte.titulo}
                  </Typography>
                  <Chip
                    label={reporte.estado_id === 1 ? 'Activo' : 'Inactivo'}
                    color={getEstadoColor(reporte.estado_id)}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => navigate(`/reportes/${reporte.id}`)}>
                    Ver detalles
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Paper>
    </Container>
  );
};

export default Dashboard; 