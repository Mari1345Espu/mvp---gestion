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
  School as SchoolIcon,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

const features = [
  {
    title: 'Mis Proyectos',
    description: 'Gestiona tus proyectos de investigación activos.',
    icon: <AssignmentIcon sx={{ fontSize: 40 }} />,
    path: '/researcher/projects',
  },
  {
    title: 'Publicaciones',
    description: 'Administra tus publicaciones y productos de investigación.',
    icon: <DescriptionIcon sx={{ fontSize: 40 }} />,
    path: '/researcher/publications',
  },
  {
    title: 'Evaluaciones',
    description: 'Revisa las evaluaciones de tus trabajos.',
    icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
    path: '/researcher/evaluations',
  },
  {
    title: 'Formación',
    description: 'Accede a recursos y materiales de formación.',
    icon: <SchoolIcon sx={{ fontSize: 40 }} />,
    path: '/researcher/training',
  },
];

const mockProjects = [
  {
    id: 1,
    title: 'Proyecto de Investigación 1',
    status: 'En Progreso',
    deadline: '2024-12-31',
  },
  {
    id: 2,
    title: 'Proyecto de Investigación 2',
    status: 'Pendiente',
    deadline: '2024-10-15',
  },
];

const ResearcherDashboard = () => {
  const { user } = useAuth();

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'en progreso':
        return 'primary';
      case 'pendiente':
        return 'warning';
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
          Panel de Investigador
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
              Mis Proyectos Activos
            </Typography>
            <List>
              {mockProjects.map((project) => (
                <ListItem key={project.id}>
                  <ListItemText
                    primary={project.title}
                    secondary={`Fecha límite: ${project.deadline}`}
                  />
                  <ListItemSecondaryAction>
                    <Chip
                      label={project.status}
                      color={getStatusColor(project.status)}
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Button
                      component={RouterLink}
                      to={`/researcher/projects/${project.id}`}
                      size="small"
                    >
                      Ver Detalles
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
              Resumen de Actividad
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1" gutterBottom>
                Proyectos Activos: 2
              </Typography>
              <Typography variant="body1" gutterBottom>
                Publicaciones: 3
              </Typography>
              <Typography variant="body1" gutterBottom>
                Evaluaciones Pendientes: 1
              </Typography>
              <Typography variant="body1" gutterBottom>
                Productos: 5
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ResearcherDashboard; 