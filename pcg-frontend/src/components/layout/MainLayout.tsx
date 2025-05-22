import React, { useState } from 'react';
import { Box, CssBaseline } from '@mui/material';
import { Navbar } from '../Navbar';
import Sidebar from '../navigation/Sidebar';

const drawerWidth = 240;

interface MainLayoutProps {
  children: React.ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <Navbar onMenuClick={toggleSidebar} />
      <Sidebar open={sidebarOpen} onClose={toggleSidebar} />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout; 