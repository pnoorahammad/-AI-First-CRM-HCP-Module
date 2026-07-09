import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Box } from '@mui/material';
import Sidebar from '../components/Sidebar';
import TopNavbar from '../components/TopNavbar';

const drawerWidth = 260;

const MainLayout: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <TopNavbar handleDrawerToggle={handleDrawerToggle} drawerWidth={drawerWidth} />
      
      <Sidebar 
        drawerWidth={drawerWidth} 
        mobileOpen={mobileOpen} 
        handleDrawerToggle={handleDrawerToggle} 
      />
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          mt: 8 // Space for AppBar
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default MainLayout;
