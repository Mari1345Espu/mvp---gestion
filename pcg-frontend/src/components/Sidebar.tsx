import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Box,
  useTheme,
  useMediaQuery
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Assignment as AssignmentIcon,
  People as PeopleIcon,
  Settings as SettingsIcon,
  Menu as MenuIcon
} from '@mui/icons-material';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Proyectos', icon: <AssignmentIcon />, path: '/projects' },
  { text: 'Usuarios', icon: <PeopleIcon />, path: '/users' },
  { text: 'Configuración', icon: <SettingsIcon />, path: '/settings' }
];

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const handleNavigation = (path: string) => {
    navigate(path);
    if (isMobile) {
      onClose();
    }
  };

  return (
    <Drawer
      variant={isMobile ? 'temporary' : 'permanent'}
      open={open}
      onClose={onClose}
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
          backgroundColor: theme.palette.background.default,
          borderRight: `1px solid ${theme.palette.divider}`
        }
      }}
    >
      <Box sx={{ p: 2 }}>
        <MenuIcon sx={{ fontSize: 40, color: theme.palette.primary.main }} />
      </Box>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            onClick={() => handleNavigation(item.path)}
            selected={location.pathname === item.path}
            sx={{
              '&.Mui-selected': {
                backgroundColor: theme.palette.primary.light,
                '&:hover': {
                  backgroundColor: theme.palette.primary.light,
                }
              }
            }}
          >
            <ListItemIcon sx={{ color: location.pathname === item.path ? theme.palette.primary.main : 'inherit' }}>
              {item.icon}
            </ListItemIcon>
            <ListItemText 
              primary={item.text}
              sx={{
                color: location.pathname === item.path ? theme.palette.primary.main : 'inherit'
              }}
            />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;
