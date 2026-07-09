import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import hcpReducer from './slices/hcpSlice';
import interactionReducer from './slices/interactionSlice';
import chatReducer from './slices/chatSlice';
// Future slices: notificationReducer

export const store = configureStore({
  reducer: {
    auth: authReducer,
    hcp: hcpReducer,
    interactions: interactionReducer,
    chat: chatReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
