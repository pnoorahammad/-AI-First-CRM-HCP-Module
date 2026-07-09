import React, { useEffect } from 'react';
import { 
  Box, 
  Grid, 
  Paper, 
  Typography, 
  Card, 
  CardContent,
  Avatar
} from '@mui/material';
import { 
  PeopleAlt as HCPIcon, 
  Assignment as InteractionIcon, 
  Event as EventIcon 
} from '@mui/icons-material';
import { useDispatch, useSelector } from 'react-redux';
import { fetchInteractions } from '../store/slices/interactionSlice';
import { fetchHCPs } from '../store/slices/hcpSlice';
import { RootState, AppDispatch } from '../store/store';

const StatCard: React.FC<{ title: string, value: string | number, icon: React.ReactNode, color: string }> = ({ title, value, icon, color }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', p: 3 }}>
      <Box>
        <Typography color="text.secondary" variant="overline"  sx={{ fontWeight: "bold" }}>
          {title}
        </Typography>
        <Typography variant="h4"  sx={{ fontWeight: "bold" }}>
          {value}
        </Typography>
      </Box>
      <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>
        {icon}
      </Avatar>
    </CardContent>
  </Card>
);

const DashboardPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { interactions } = useSelector((state: RootState) => state.interactions);
  const { hcps } = useSelector((state: RootState) => state.hcp);

  useEffect(() => {
    dispatch(fetchInteractions());
    dispatch(fetchHCPs());
  }, [dispatch]);

  const recentInteractions = interactions.slice(0, 5);

  return (
    <Box>
      <Typography variant="h4" gutterBottom  color="text.primary" sx={{ fontWeight: "bold" }}>
        Dashboard
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard 
            title="TOTAL INTERACTIONS" 
            value={interactions.length} 
            icon={<InteractionIcon fontSize="large" />} 
            color="primary.main" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard 
            title="MANAGED HCPs" 
            value={hcps.length} 
            icon={<HCPIcon fontSize="large" />} 
            color="success.main" 
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <StatCard 
            title="UPCOMING FOLLOW-UPS" 
            value={interactions.filter(i => new Date(i.date) >= new Date()).length} 
            icon={<EventIcon fontSize="large" />} 
            color="warning.main" 
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, borderRadius: 2, height: '100%' }}>
            <Typography variant="h6"  gutterBottom sx={{ fontWeight: "bold" }}>
              Recent Interactions
            </Typography>
            {recentInteractions.length === 0 ? (
              <Typography color="text.secondary" sx={{ mt: 2 }}>No interactions logged yet.</Typography>
            ) : (
              <Box sx={{ mt: 2 }}>
                {recentInteractions.map((interaction, index) => {
                  const hcp = hcps.find(h => h.id === interaction.hcp_id);
                  return (
                    <Box key={interaction.id} sx={{ mb: index !== recentInteractions.length -1 ? 2 : 0, pb: index !== recentInteractions.length -1 ? 2 : 0, borderBottom: index !== recentInteractions.length -1 ? '1px solid #eee' : 'none' }}>
                      <Typography variant="subtitle1"  sx={{ fontWeight: "bold" }}>
                        {hcp ? hcp.name : `HCP #${interaction.hcp_id}`}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(interaction.date).toLocaleDateString()} at {interaction.time} • {interaction.visit_type}
                      </Typography>
                      {interaction.products_discussed.length > 0 && (
                        <Typography variant="body2" sx={{ mt: 0.5 }}>
                          <strong>Products:</strong> {interaction.products_discussed.join(', ')}
                        </Typography>
                      )}
                    </Box>
                  );
                })}
              </Box>
            )}
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, borderRadius: 2, height: '100%', bgcolor: 'primary.dark', color: 'white' }}>
            <Typography variant="h6"  gutterBottom sx={{ fontWeight: "bold" }}>
              AI Assistant
            </Typography>
            <Typography variant="body2" sx={{ mb: 2, opacity: 0.9 }}>
              Need to log a meeting quickly? Use the conversational AI assistant to extract details automatically.
            </Typography>
            <Box component="img" src="https://illustrations.popsy.co/amber/communication.svg" alt="AI Assistant" sx={{ width: '100%', maxWidth: 200, display: 'block', margin: 'auto' }} />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;
