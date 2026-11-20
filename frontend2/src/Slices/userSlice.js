import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    username: null, // This will store user details when logged in
    email: null,
    currentChapter: null,
    authChecked: false // becomes true once we know whether the user is logged in
  },
  reducers: {
    login: (state, action) => {
      state.username = action.payload.username;
      state.email = action.payload.email;
      state.currentChapter = action.payload.current_chapter;
      state.authChecked = true;
    },
    logout: (state) => {
      state.username = null;
      state.email = null;
      state.currentChapter = null;
      state.authChecked = true;
    },
    updateUser: (state, action) => {
      state.currentChapter = action.payload.current_chapter
    }
  },
});

export const { login, logout, updateUser } = userSlice.actions;

export default userSlice.reducer;