import React from 'react';
import { 
  Box, 
  Drawer, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText,
  Typography,
  Divider,
  useTheme
} from '@mui/material';
import { 
  Dashboard as DashboardIcon, 
  AddCircleOutline as LogIcon, 
  History as HistoryIcon,
  PeopleAlt as HCPIcon,
  Analytics as AnalyticsIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';
import { useLocation, useNavigate } from 'react-router-dom';

interface SidebarProps {
  drawerWidth: number;
  mobileOpen: boolean;
  handleDrawerToggle: () => void;
}

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Log Interaction', icon: <LogIcon />, path: '/log-interaction' },
  { text: 'Interaction History', icon: <HistoryIcon />, path: '/history' },
  { text: 'HCP Profiles', icon: <HCPIcon />, path: '/hcps' },
  { text: 'Analytics', icon: <AnalyticsIcon />, path: '/analytics' },
  { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
];

const Sidebar: React.FC<SidebarProps> = ({ drawerWidth, mobileOpen, handleDrawerToggle }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const theme = useTheme();

  const drawer = (
    <div>
      <Box sx={{ p: 2.5, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Typography variant="h6"  color="primary.main" sx={{ fontWeight: "bold" }}>
          AI-First CRM
        </Typography>
      </Box>
      <Divider />
      <List sx={{ px: 2, pt: 2 }}>
        {menuItems.map((item) => {
          const isSelected = location.pathname === item.path;
          return (
            <ListItem key={item.text} disablePadding sx={{ mb: 1 }}>
              <ListItemButton
                selected={isSelected}
                onClick={() => {
                  navigate(item.path);
                  if (mobileOpen) handleDrawerToggle();
                }}
                sx={{
                  borderRadius: 2,
                  '&.Mui-selected': {
                    bgcolor: 'primary.main',
                    color: 'primary.contrastText',
                    '&:hover': {
                      bgcolor: 'primary.dark',
                    },
                    '& .MuiListItemIcon-root': {
                      color: 'primary.contrastText',
                    }
                  }
                }}
              >
                <ListItemIcon sx={{ minWidth: 40, color: isSelected ? 'inherit' : 'text.secondary' }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText primary={item.text} primaryTypographyProps={{ fontWeight: isSelected ? 600 : 400 }} />
              </ListItemButton>
            </ListItem>
          );
        })}
      </List>
    </div>
  );

  return (
    <Box
      component="nav"
      sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
    >
      {/* Mobile drawer */}
      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{ keepMounted: true }}
        sx={{
          display: { xs: 'block', sm: 'none' },
          '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
        }}
      >
        {drawer}
      </Drawer>
      
      {/* Desktop drawer */}
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: 'none', sm: 'block' },
          '& .MuiDrawer-paper': { 
            boxSizing: 'border-box', 
            width: drawerWidth,
            borderRight: `1px solid ${theme.palette.divider}`
          },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
};

export default Sidebar;
