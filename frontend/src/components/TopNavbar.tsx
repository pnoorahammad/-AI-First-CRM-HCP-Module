import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  IconButton, 
  Typography, 
  Box, 
  Avatar, 
  Menu, 
  MenuItem,
  useTheme
} from '@mui/material';
import { Menu as MenuIcon, Notifications as NotificationsIcon } from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../store/slices/authSlice';
import { RootState, AppDispatch } from '../store/store';
import { useNavigate } from 'react-router-dom';

interface TopNavbarProps {
  handleDrawerToggle: () => void;
  drawerWidth: number;
}

const TopNavbar: React.FC<TopNavbarProps> = ({ handleDrawerToggle, drawerWidth }) => {
  const theme = useTheme();
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { user } = useSelector((state: RootState) => state.auth);
  
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  
  const handleLogout = () => {
    handleClose();
    dispatch(logout());
    navigate('/login');
  };

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        width: { sm: `calc(100% - ${drawerWidth}px)` },
        ml: { sm: `${drawerWidth}px` },
        bgcolor: 'background.paper',
        color: 'text.primary',
        borderBottom: `1px solid ${theme.palette.divider}`
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{ mr: 2, display: { sm: 'none' } }}
        >
          <MenuIcon />
        </IconButton>
        
        <Box sx={{ flexGrow: 1 }} />
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton color="inherit">
            <NotificationsIcon />
          </IconButton>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, cursor: 'pointer' }} onClick={handleMenu}>
            <Box sx={{ textAlign: 'right', display: { xs: 'none', md: 'block' } }}>
              <Typography variant="body2"  sx={{ fontWeight: "bold" }}>
                {user?.full_name || 'User'}
              </Typography>
              <Typography variant="caption" color="text.secondary" sx={{ textTransform: 'capitalize' }}>
                {user?.role || 'Rep'}
              </Typography>
            </Box>
            <Avatar sx={{ bgcolor: 'primary.main', width: 35, height: 35 }}>
              {user?.full_name?.charAt(0) || 'U'}
            </Avatar>
          </Box>
          
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            keepMounted
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
          >
            <MenuItem onClick={() => { handleClose(); navigate('/settings'); }}>Profile Settings</MenuItem>
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default TopNavbar;
