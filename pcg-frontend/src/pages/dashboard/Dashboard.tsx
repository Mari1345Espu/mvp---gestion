import React from 'react';
import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';
import AdminDashboard from '../admin/Dashboard';
import GroupLeaderDashboard from '../group-leader/GroupLeaderDashboard';
import ResearcherDashboard from '../researcher/ResearcherDashboard';
import InternalEvaluatorDashboard from '../internal-evaluator/InternalEvaluatorDashboard';
import ExternalEvaluatorDashboard from '../external-evaluator/ExternalEvaluatorDashboard';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const renderDashboard = () => {
    switch (user?.rol) {
      case 'admin':
        return <AdminDashboard />;
      case 'lider':
        return <GroupLeaderDashboard />;
      case 'investigador':
        return <ResearcherDashboard />;
      case 'evaluador_interno':
        return <InternalEvaluatorDashboard />;
      case 'evaluador_externo':
        return <ExternalEvaluatorDashboard />;
      default:
        return (
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom>
              Bienvenido, {user?.nombre}
            </Typography>
            <Box sx={{ mt: 4 }}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Paper sx={{ p: 3 }}>
                    <Typography variant="h6" gutterBottom>
                      No tienes un rol asignado
                    </Typography>
                    <Typography variant="body1">
                      Por favor, contacta al administrador para que te asigne un rol.
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          </Container>
        );
    }
  };

  return renderDashboard();
};

export default Dashboard; 