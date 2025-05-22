import React from 'react';
import {
  Container,
  Typography,
  Paper,
  Grid,
  Box,
  Divider,
} from '@mui/material';

const Configuracion: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Configuración
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Configuración General
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Nombre de la Institución
              </Typography>
              <Typography>Universidad Nacional de Colombia</Typography>
            </Box>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Año Académico
              </Typography>
              <Typography>2024</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Configuración del Sistema
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Versión del Sistema
              </Typography>
              <Typography>1.0.0</Typography>
            </Box>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Última Actualización
              </Typography>
              <Typography>01/03/2024</Typography>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Configuración de Notificaciones
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Notificaciones por Correo
              </Typography>
              <Typography>Activadas</Typography>
            </Box>
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" color="textSecondary" gutterBottom>
                Notificaciones en Sistema
              </Typography>
              <Typography>Activadas</Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Configuracion; 