import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import { api } from '../../services/api';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatState {
  messages: ChatMessage[];
  sessionId: string | null;
  isLoading: boolean;
  error: string | null;
  extractedData: any | null; // For the preview card
}

const initialState: ChatState = {
  messages: [
    { role: 'assistant', content: 'Hi there! Tell me about your recent interaction with a Healthcare Professional.' }
  ],
  sessionId: null,
  isLoading: false,
  error: null,
  extractedData: null,
};

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async (message: string, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const { sessionId, messages } = state.chat;
      
      const response = await api.post('/chat/', {
        message,
        session_id: sessionId,
        history: messages.filter((m: ChatMessage) => m.content) // Don't send empty messages
      });
      
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to send message');
    }
  }
);

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addUserMessage: (state, action: PayloadAction<string>) => {
      state.messages.push({ role: 'user', content: action.payload });
    },
    setExtractedData: (state, action: PayloadAction<any>) => {
      state.extractedData = action.payload;
    },
    clearChat: (state) => {
      state.messages = initialState.messages;
      state.sessionId = null;
      state.extractedData = null;
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.isLoading = false;
        state.sessionId = action.payload.session_id;
        state.messages.push({ role: 'assistant', content: action.payload.response });
        
        // Very basic heuristic: if response contains "Successfully logged", we can clear
        if (action.payload.response.includes('Successfully logged interaction')) {
           state.extractedData = null;
        }
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
        state.messages.push({ role: 'assistant', content: 'Sorry, I encountered an error processing that.' });
      });
  },
});

export const { addUserMessage, setExtractedData, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
