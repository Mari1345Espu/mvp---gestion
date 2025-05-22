import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
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
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Chip,
} from '@mui/material';
import {
  Assignment as AssignmentIcon,
  Description as DescriptionIcon,
  Assessment as AssessmentIcon,
  History as HistoryIcon,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

const features = [
  {
    title: 'Evaluaciones Pendientes',
    description: 'Revisa y evalúa los proyectos asignados.',
    icon: <AssignmentIcon sx={{ fontSize: 40 }} />,
    path: '/internal-evaluator/pending',
  },
  {
    title: 'Publicaciones',
    description: 'Evalúa publicaciones y productos de investigación.',
    icon: <DescriptionIcon sx={{ fontSize: 40 }} />,
    path: '/internal-evaluator/publications',
  },
  {
    title: 'Reportes',
    description: 'Genera reportes de evaluación.',
    icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
    path: '/internal-evaluator/reports',
  },
  {
    title: 'Historial',
    description: 'Consulta evaluaciones realizadas anteriormente.',
    icon: <HistoryIcon sx={{ fontSize: 40 }} />,
    path: '/internal-evaluator/history',
  },
];

const mockEvaluations = [
  {
    id: 1,
    title: 'Proyecto de Investigación 1',
    type: 'Proyecto',
    deadline: '2024-12-31',
    status: 'Pendiente',
  },
  {
    id: 2,
    title: 'Publicación Científica 1',
    type: 'Publicación',
    deadline: '2024-10-15',
    status: 'En Revisión',
  },
];

const InternalEvaluatorDashboard = () => {
  const { user } = useAuth();

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pendiente':
        return 'warning';
      case 'en revisión':
        return 'primary';
      case 'completado':
        return 'success';
      default:
        return 'default';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Panel de Evaluador Interno
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Bienvenido, {user?.nombre}
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {features.map((feature) => (
          <Grid item key={feature.title} xs={12} sm={6} md={3}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'center',
                    mb: 2,
                    color: 'primary.main',
                  }}
                >
                  {feature.icon}
                </Box>
                <Typography gutterBottom variant="h6" component="h2" align="center">
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" align="center">
                  {feature.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  component={RouterLink}
                  to={feature.path}
                  size="small"
                  color="primary"
                  fullWidth
                >
                  Acceder
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Evaluaciones Pendientes
            </Typography>
            <List>
              {mockEvaluations.map((evaluation) => (
                <ListItem key={evaluation.id}>
                  <ListItemText
                    primary={evaluation.title}
                    secondary={`Tipo: ${evaluation.type} - Fecha límite: ${evaluation.deadline}`}
                  />
                  <ListItemSecondaryAction>
                    <Chip
                      label={evaluation.status}
                      color={getStatusColor(evaluation.status)}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Button
                      component={RouterLink}
                      to={`/internal-evaluator/evaluate/${evaluation.id}`}
                      size="small"
                    >
                      Evaluar
                    </Button>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Resumen de Evaluaciones
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1" gutterBottom>
                Pendientes: 5
              </Typography>
              <Typography variant="body1" gutterBottom>
                En Revisión: 3
              </Typography>
              <Typography variant="body1" gutterBottom>
                Completadas: 12
              </Typography>
              <Typography variant="body1" gutterBottom>
                Total: 20
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default InternalEvaluatorDashboard; 