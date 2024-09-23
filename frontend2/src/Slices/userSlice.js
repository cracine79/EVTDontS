import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    username: null, // This will store user details when logged in
    email: null,
    currentChapter: null
  },
  reducers: {
    login: (state, action) => {
      state.username = action.payload.username;
      state.email = action.payload.email;
      state.currentChapter = action.payload.current_chapter;
    },
    logout: (state) => {
      state.username = null;
      state.email = null;
      state.currentChapter = null;
    },
    updateUser: (state, action) => {
      state.currentChapter = action.payload.current_chapter
    }
  },
});

export const { login, logout, updateUser } = userSlice.actions;

export default userSlice.reducer;