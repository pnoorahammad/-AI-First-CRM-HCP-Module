import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';
import type { Interaction, InteractionCreate } from '../../types/interaction';

interface InteractionState {
  interactions: Interaction[];
  currentInteraction: Interaction | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: InteractionState = {
  interactions: [],
  currentInteraction: null,
  isLoading: false,
  error: null,
};

export const fetchInteractions = createAsyncThunk(
  'interactions/fetchAll',
  async (hcpId?: number) => {
    const params = hcpId ? { hcp_id: hcpId } : {};
    const response = await api.get('/interactions/', { params });
    return response.data;
  }
);

export const createInteraction = createAsyncThunk(
  'interactions/create',
  async (data: InteractionCreate, { rejectWithValue }) => {
    try {
      const response = await api.post('/interactions/', data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create interaction');
    }
  }
);

const interactionSlice = createSlice({
  name: 'interactions',
  initialState,
  reducers: {
    setCurrentInteraction: (state, action) => {
      state.currentInteraction = action.payload;
    },
    clearInteractionError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.isLoading = false;
        state.interactions = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch interactions';
      })
      .addCase(createInteraction.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.isLoading = false;
        state.interactions.unshift(action.payload); // Add to beginning
      })
      .addCase(createInteraction.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setCurrentInteraction, clearInteractionError } = interactionSlice.actions;
export default interactionSlice.reducer;
