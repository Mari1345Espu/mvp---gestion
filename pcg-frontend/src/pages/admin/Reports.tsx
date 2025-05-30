import React from 'react';
import { Container, Typography } from '@mui/material';

const Reports = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Gestión de Reportes
      </Typography>
      <Typography variant="body1">
        Esta sección está en desarrollo. Próximamente podrás generar reportes del sistema.
      </Typography>
    </Container>
  );
};

export default Reports; 