import React from 'react';
import { Container, Typography, Grid, Paper } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';

const AdminDashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard del Administrador
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Bienvenido, {user?.nombre}
            </Typography>
            <Typography variant="body1">
              Aquí podrás gestionar usuarios, roles y permisos del sistema.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default AdminDashboard; 