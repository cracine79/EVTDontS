import { configureStore } from '@reduxjs/toolkit';
import userReducer from './Slices/userSlice';
import modalReducer from './Slices/modalSlice.js'
import unitsReducer from './Slices/unitsSlice.js'
import chaptersReducer from './Slices/chaptersSlice.js'
import questionsReducer from './Slices/questionsSlice.js'

export const store = configureStore({
  reducer: {
    user: userReducer,
    modal: modalReducer,
    units: unitsReducer,
    chapters: chaptersReducer,
    questions: questionsReducer
  },
});