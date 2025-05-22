import React from 'react';
import { Container, Typography, Grid, Paper } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';

const LiderDashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard del Líder de Grupo
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Bienvenido, {user?.nombre}
            </Typography>
            <Typography variant="body1">
              Aquí podrás gestionar tu grupo de investigación y sus proyectos.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LiderDashboard; 