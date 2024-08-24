import { configureStore } from '@reduxjs/toolkit';
import userReducer from './Slices/userSlice';
import modalReducer from './Slices/modalSlice'

export const store = configureStore({
  reducer: {
    user: userReducer,
    modal: modalReducer
  },
});