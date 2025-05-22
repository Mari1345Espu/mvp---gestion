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
} from '@mui/material';
import {
  People as PeopleIcon,
  Group as GroupIcon,
  Assignment as AssignmentIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

const features = [
  {
    title: 'Gestión de Usuarios',
    description: 'Administra usuarios, roles y permisos del sistema.',
    icon: <PeopleIcon sx={{ fontSize: 40 }} />,
    path: '/admin/users',
  },
  {
    title: 'Grupos de Investigación',
    description: 'Gestiona los grupos de investigación y sus miembros.',
    icon: <GroupIcon sx={{ fontSize: 40 }} />,
    path: '/admin/research-groups',
  },
  {
    title: 'Proyectos',
    description: 'Administra proyectos de investigación y sus estados.',
    icon: <AssignmentIcon sx={{ fontSize: 40 }} />,
    path: '/admin/projects',
  },
  {
    title: 'Reportes',
    description: 'Genera reportes y estadísticas del sistema.',
    icon: <AssessmentIcon sx={{ fontSize: 40 }} />,
    path: '/admin/reports',
  },
];

const AdminDashboard = () => {
  const { user } = useAuth();

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Panel de Administración
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

      <Paper sx={{ p: 3, mt: 4 }}>
        <Typography variant="h6" gutterBottom>
          Resumen del Sistema
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary">
                150
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Usuarios Activos
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary">
                25
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Grupos de Investigación
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary">
                75
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Proyectos Activos
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary">
                45
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Publicaciones
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default AdminDashboard; 