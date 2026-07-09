import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { ChatMessage } from '../../store/slices/chatSlice';

interface MessageBubbleProps {
  message: ChatMessage;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <Box sx={{ 
      display: 'flex', 
      justifyContent: isUser ? 'flex-end' : 'flex-start',
      mb: 2
    }}>
      <Paper 
        elevation={1}
        sx={{
          p: 2,
          maxWidth: '75%',
          borderRadius: 3,
          borderBottomRightRadius: isUser ? 0 : 3,
          borderBottomLeftRadius: isUser ? 3 : 0,
          bgcolor: isUser ? 'primary.main' : 'background.paper',
          color: isUser ? 'primary.contrastText' : 'text.primary',
        }}
      >
        <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
          {message.content}
        </Typography>
      </Paper>
    </Box>
  );
};
