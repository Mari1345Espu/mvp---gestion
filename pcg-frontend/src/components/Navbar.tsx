import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Container,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
} from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import logo from '../assets/logo.png';

interface NavbarProps {
  onMenuClick: () => void;
}

const pages = [
  { name: 'Inicio', path: '/' },
  { name: 'Acerca de', path: '/about' },
  { name: 'Contacto', path: '/contact' },
];

export const Navbar: React.FC<NavbarProps> = ({ onMenuClick }) => {
  const [anchorElNav, setAnchorElNav] = useState<null | HTMLElement>(null);
  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Error al cerrar sesión:', error);
    }
  };

  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Logo y nombre institucional */}
          <Box
            component={RouterLink}
            to="/"
            sx={{
              display: 'flex',
              alignItems: 'center',
              textDecoration: 'none',
              mr: 2,
            }}
          >
            <Box
              component="img"
              src={logo}
              alt="Logo Observatorio"
              sx={{ height: 40, width: 40, mr: 1 }}
            />
            <Typography
              variant="h6"
              noWrap
              sx={{
                fontFamily: 'monospace',
                fontWeight: 700,
                letterSpacing: '.3rem',
                color: 'white',
                textDecoration: 'none',
                display: { xs: 'none', md: 'flex' },
              }}
            >
              OBSERVATORIO
            </Typography>
          </Box>

          {/* Menú móvil */}
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="menu de navegación"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              <MenuItem onClick={() => { handleCloseNavMenu(); navigate('/dashboard'); }}>
                Dashboard
              </MenuItem>
              <MenuItem onClick={() => { handleCloseNavMenu(); navigate('/usuarios'); }}>
                Usuarios
              </MenuItem>
              <MenuItem onClick={() => { handleCloseNavMenu(); navigate('/proyectos'); }}>
                Proyectos
              </MenuItem>
            </Menu>
          </Box>

          {/* Logo y nombre para pantallas pequeñas */}
          <Box
            component={RouterLink}
            to="/"
            sx={{
              display: { xs: 'flex', md: 'none' },
              alignItems: 'center',
              flexGrow: 1,
              textDecoration: 'none',
            }}
          >
            <Box
              component="img"
              src={logo}
              alt="Logo Observatorio"
              sx={{ height: 36, width: 36, mr: 1 }}
            />
            <Typography
              variant="h5"
              noWrap
              sx={{
                fontFamily: 'monospace',
                fontWeight: 700,
                letterSpacing: '.3rem',
                color: '#fff',
                textDecoration: 'none',
              }}
            >
              OBSERVATORIO
            </Typography>
          </Box>

          {/* Menú para pantallas grandes */}
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            <Button
              onClick={() => navigate('/dashboard')}
              sx={{ my: 2, color: 'white', display: 'block' }}
            >
              Dashboard
            </Button>
            <Button
              onClick={() => navigate('/usuarios')}
              sx={{ my: 2, color: 'white', display: 'block' }}
            >
              Usuarios
            </Button>
            <Button
              onClick={() => navigate('/proyectos')}
              sx={{ my: 2, color: 'white', display: 'block' }}
            >
              Proyectos
            </Button>
          </Box>

          {/* Menú de usuario */}
          <Box sx={{ flexGrow: 0 }}>
            {isAuthenticated ? (
              <>
                <Tooltip title="Abrir menú">
                  <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                    <Avatar alt={user?.nombre} src={user?.avatar_url} />
                  </IconButton>
                </Tooltip>
                <Menu
                  sx={{ mt: '45px' }}
                  id="menu-appbar"
                  anchorEl={anchorElUser}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorElUser)}
                  onClose={handleCloseUserMenu}
                >
                  <MenuItem onClick={() => { handleCloseUserMenu(); navigate('/perfil'); }}>
                    <Typography textAlign="center">Perfil</Typography>
                  </MenuItem>
                  <MenuItem onClick={() => { handleCloseUserMenu(); handleLogout(); }}>
                    <Typography textAlign="center">Cerrar Sesión</Typography>
                  </MenuItem>
                </Menu>
              </>
            ) : (
              <Button color="inherit" onClick={() => navigate('/login')}>
                Iniciar Sesión
              </Button>
            )}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar; 