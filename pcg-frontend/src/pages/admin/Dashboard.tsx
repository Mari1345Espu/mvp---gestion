import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Container,
  Box,
  Paper,
} from '@mui/material';
import {
  People as PeopleIcon,
  Assignment as ProjectIcon,
  LocationOn as LocationIcon,
  Campaign as ConvocatoriaIcon,
  RateReview as EvaluatorIcon,
  Assessment as ReportIcon,
  CheckCircle as CloseIcon,
} from '@mui/icons-material';

const AdminDashboard = () => {
  const navigate = useNavigate();

  const dashboardItems = [
    {
      title: 'Gestión de Usuarios',
      description: 'Administrar usuarios, activar/desactivar y CRUD completo',
      icon: <PeopleIcon sx={{ fontSize: 40 }} />,
      path: '/admin/users',
      color: '#1976d2',
    },
    {
      title: 'Gestión de Proyectos',
      description: 'Administrar proyectos, CRUD completo',
      icon: <ProjectIcon sx={{ fontSize: 40 }} />,
      path: '/admin/projects',
      color: '#2e7d32',
    },
    {
      title: 'Gestión de Lugares',
      description: 'Administrar extensiones, programas y facultades',
      icon: <LocationIcon sx={{ fontSize: 40 }} />,
      path: '/admin/locations',
      color: '#ed6c02',
    },
    {
      title: 'Gestión de Convocatorias',
      description: 'Administrar convocatorias, activar/desactivar',
      icon: <ConvocatoriaIcon sx={{ fontSize: 40 }} />,
      path: '/admin/convocatorias',
      color: '#9c27b0',
    },
    {
      title: 'Asignación de Evaluadores',
      description: 'Asignar evaluadores externos e internos',
      icon: <EvaluatorIcon sx={{ fontSize: 40 }} />,
      path: '/admin/evaluators',
      color: '#d32f2f',
    },
    {
      title: 'Reportes',
      description: 'Generar reportes del sistema',
      icon: <ReportIcon sx={{ fontSize: 40 }} />,
      path: '/admin/reports',
      color: '#0288d1',
    },
    {
      title: 'Gestión de Cierre',
      description: 'Administrar cierre de proyectos',
      icon: <CloseIcon sx={{ fontSize: 40 }} />,
      path: '/admin/closure',
      color: '#7b1fa2',
    },
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Panel de Administración
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Bienvenido al panel de control administrativo
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {dashboardItems.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.title}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                  boxShadow: 3,
                },
              }}
              onClick={() => navigate(item.path)}
            >
              <CardContent>
                <Box
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    mb: 2,
                  }}
                >
                  <Box
                    sx={{
                      backgroundColor: `${item.color}15`,
                      borderRadius: '50%',
                      p: 1,
                      mr: 2,
                    }}
                  >
                    {React.cloneElement(item.icon, {
                      sx: { color: item.color },
                    })}
                  </Box>
                  <Typography variant="h6" component="h2">
                    {item.title}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary">
                  {item.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default AdminDashboard; 