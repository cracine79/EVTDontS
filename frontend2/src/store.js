import { configureStore } from '@reduxjs/toolkit';
import userReducer from './Slices/userSlice';
import modalReducer from './Slices/modalSlice.js'

export const store = configureStore({
  reducer: {
    user: userReducer,
    modal: modalReducer
  },
});