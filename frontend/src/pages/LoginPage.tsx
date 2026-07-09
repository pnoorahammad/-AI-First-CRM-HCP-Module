import React, { useEffect } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { useDispatch, useSelector } from 'react-redux';
import { 
  Box, 
  Button, 
  TextField, 
  Typography, 
  Paper, 
  Link,
  Alert,
  CircularProgress
} from '@mui/material';
import { login, clearError } from '../store/slices/authSlice';
import type { AppDispatch, RootState } from '../store/store';
import type { LoginData } from '../types/auth';

const LoginPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();
  const { isLoading, error, isAuthenticated } = useSelector((state: RootState) => state.auth);

  const { control, handleSubmit, formState: { errors } } = useForm<LoginData>({
    defaultValues: { email: '', password: '' }
  });

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/');
    }
    return () => {
      dispatch(clearError());
    };
  }, [isAuthenticated, navigate, dispatch]);

  const onSubmit = (data: LoginData) => {
    dispatch(login(data));
  };

  return (
    <Box 
      sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        bgcolor: 'grey.100' 
      }}
    >
      <Paper elevation={3} sx={{ p: 4, width: '100%', maxWidth: 400, borderRadius: 2 }}>
        <Typography variant="h5" component="h1" gutterBottom align="center" sx={{ fontWeight: 'bold' }}>
          AI-First CRM
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" align="center" sx={{ mb: 3 }}>
          Log in to your account
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        <form onSubmit={handleSubmit(onSubmit)}>
          <Controller
            name="email"
            control={control}
            rules={{ 
              required: 'Email is required',
              pattern: { value: /^\S+@\S+$/i, message: 'Invalid email' }
            }}
            render={({ field }) => (
              <TextField
                {...field}
                label="Email"
                variant="outlined"
                fullWidth
                margin="normal"
                error={!!errors.email}
                helperText={errors.email?.message}
              />
            )}
          />
          
          <Controller
            name="password"
            control={control}
            rules={{ required: 'Password is required' }}
            render={({ field }) => (
              <TextField
                {...field}
                label="Password"
                type="password"
                variant="outlined"
                fullWidth
                margin="normal"
                error={!!errors.password}
                helperText={errors.password?.message}
              />
            )}
          />

          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            fullWidth 
            size="large"
            sx={{ mt: 3, mb: 2 }}
            disabled={isLoading}
          >
            {isLoading ? <CircularProgress size={24} /> : 'Login'}
          </Button>

          <Typography align="center" variant="body2">
            Don't have an account?{' '}
            <Link component={RouterLink} to="/register" color="primary">
              Register here
            </Link>
          </Typography>
        </form>
      </Paper>
    </Box>
  );
};

export default LoginPage;
