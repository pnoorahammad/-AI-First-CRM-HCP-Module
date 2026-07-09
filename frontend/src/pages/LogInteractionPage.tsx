import React, { useState } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  Tabs, 
  Tab, 
  Paper,
  useTheme
} from '@mui/material';
import { StructuredForm } from '../components/interactions/StructuredForm';
import { ChatInterface } from '../components/chat/ChatInterface';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`interaction-tabpanel-${index}`}
      aria-labelledby={`interaction-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const LogInteractionPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const theme = useTheme();

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom color="primary.main" sx={{ fontWeight: 'bold' }}>
        Log Interaction
      </Typography>
      
      <Paper elevation={0} sx={{ border: `1px solid ${theme.palette.divider}`, borderRadius: 2 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'background.paper', borderRadius: '8px 8px 0 0' }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            aria-label="log interaction tabs"
            indicatorColor="primary"
            textColor="primary"
            variant="fullWidth"
          >
            <Tab label="Structured Form" id="interaction-tab-0" aria-controls="interaction-tabpanel-0" />
            <Tab label="AI Conversation" id="interaction-tab-1" aria-controls="interaction-tabpanel-1" />
          </Tabs>
        </Box>
        
        <TabPanel value={tabValue} index={0}>
          <StructuredForm />
        </TabPanel>
        
        <TabPanel value={tabValue} index={1}>
          <ChatInterface />
        </TabPanel>
      </Paper>
    </Container>
  );
};

export default LogInteractionPage;
