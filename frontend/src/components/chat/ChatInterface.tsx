import React, { useState, useRef, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { 
  Box, 
  TextField, 
  IconButton, 
  CircularProgress,
  Paper
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import { MessageBubble } from './MessageBubble';
import { EditablePreview } from './EditablePreview';
import { AppDispatch, RootState } from '../../store/store';
import { sendMessage, addUserMessage, setExtractedData } from '../../store/slices/chatSlice';

export const ChatInterface: React.FC = () => {
  const [inputValue, setInputValue] = useState('');
  const dispatch = useDispatch<AppDispatch>();
  const { messages, isLoading, extractedData } = useSelector((state: RootState) => state.chat);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, extractedData]);

  const handleSend = () => {
    if (inputValue.trim()) {
      dispatch(addUserMessage(inputValue));
      dispatch(sendMessage(inputValue));
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleConfirmPreview = (data: any) => {
    // We send a specific command to the agent to confirm the data
    const message = `Please confirm and save the interaction with this data: ${JSON.stringify(data)}`;
    dispatch(addUserMessage("I confirm the details. Please save."));
    dispatch(sendMessage(message));
    dispatch(setExtractedData(null));
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '600px', bgcolor: 'grey.50', borderRadius: 2 }}>
      
      {/* Chat Messages Area */}
      <Box sx={{ flexGrow: 1, overflow: 'auto', p: 3 }}>
        {messages.map((msg, idx) => (
          <MessageBubble key={idx} message={msg} />
        ))}
        
        {extractedData && (
          <EditablePreview 
            data={extractedData} 
            onConfirm={handleConfirmPreview} 
            onCancel={() => dispatch(setExtractedData(null))} 
          />
        )}
        
        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
            <Paper elevation={0} sx={{ p: 2, borderRadius: 3, bgcolor: 'background.paper' }}>
              <CircularProgress size={20} />
            </Paper>
          </Box>
        )}
        <div ref={messagesEndRef} />
      </Box>
      
      {/* Input Area */}
      <Box sx={{ p: 2, bgcolor: 'background.paper', borderTop: '1px solid #eee', borderRadius: '0 0 8px 8px' }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="e.g. I met Dr. Raj yesterday in Apollo Hospital. Discussed Product X..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyPress}
          disabled={isLoading || !!extractedData}
          InputProps={{
            endAdornment: (
              <IconButton 
                color="primary" 
                onClick={handleSend}
                disabled={!inputValue.trim() || isLoading || !!extractedData}
              >
                <SendIcon />
              </IconButton>
            ),
            sx: { borderRadius: 3, bgcolor: 'grey.100' }
          }}
        />
      </Box>
    </Box>
  );
};
