import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    username: null, // This will store user details when logged in
    email: null
  },
  reducers: {
    login: (state, action) => {
      state.username = action.payload.username;
      state.email = action.payload.email;
    },
    logout: (state) => {
      state.username = null;
      state.email = null;
    },
  },
});

export const { login, logout } = userSlice.actions;

export default userSlice.reducer;