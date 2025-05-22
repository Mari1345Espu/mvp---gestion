import React from 'react';
import { Container, Box, Paper, Typography } from '@mui/material';
import logo from '../assets/logo.png';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title }) => {
  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Box sx={{ mb: 3, display: 'flex', justifyContent: 'center', width: '100%' }}>
          <img src={logo} alt="Logo" style={{ height: 100, maxWidth: '100%' }} />
        </Box>
        <Paper
          elevation={3}
          sx={{
            p: 4,
            width: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5" sx={{ mb: 3, fontWeight: 600 }}>
            {title}
          </Typography>
          {children}
        </Paper>
      </Box>
    </Container>
  );
};

export default AuthLayout; 