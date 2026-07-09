import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { api } from '../../services/api';
import type { HCP, HCPCreate } from '../../types/hcp';

interface HCPState {
  hcps: HCP[];
  currentHcp: HCP | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: HCPState = {
  hcps: [],
  currentHcp: null,
  isLoading: false,
  error: null,
};

export const fetchHCPs = createAsyncThunk(
  'hcp/fetchAll',
  async (search?: string) => {
    const params = search ? { search } : {};
    const response = await api.get('/hcp/', { params });
    return response.data;
  }
);

export const createHCP = createAsyncThunk(
  'hcp/create',
  async (data: HCPCreate, { rejectWithValue }) => {
    try {
      const response = await api.post('/hcp/', data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create HCP');
    }
  }
);

const hcpSlice = createSlice({
  name: 'hcp',
  initialState,
  reducers: {
    setCurrentHcp: (state, action) => {
      state.currentHcp = action.payload;
    },
    clearHcpError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHCPs.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchHCPs.fulfilled, (state, action) => {
        state.isLoading = false;
        state.hcps = action.payload;
      })
      .addCase(fetchHCPs.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch HCPs';
      })
      .addCase(createHCP.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(createHCP.fulfilled, (state, action) => {
        state.isLoading = false;
        state.hcps.push(action.payload);
      })
      .addCase(createHCP.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setCurrentHcp, clearHcpError } = hcpSlice.actions;
export default hcpSlice.reducer;
