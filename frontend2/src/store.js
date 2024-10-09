import { configureStore } from '@reduxjs/toolkit';
import userReducer from './Slices/userSlice';
import modalReducer from './Slices/modalSlice.js'
import unitsReducer from './Slices/unitsSlice.js'
import chaptersReducer from './Slices/chaptersSlice.js'
import questionsReducer from './Slices/questionsSlice.js'
import resultsReducer from './Slices/resultsSlice.js'
import topicProgReducer from './Slices/topicProgSlice.js'
import userChaptersReducer from './Slices/userChaptersSlice.js'

export const store = configureStore({
  reducer: {
    user: userReducer,
    modal: modalReducer,
    units: unitsReducer,
    chapters: chaptersReducer,
    questions: questionsReducer,
    results: resultsReducer,
    topicProg: topicProgReducer,
    userChapters: userChaptersReducer
  },
});