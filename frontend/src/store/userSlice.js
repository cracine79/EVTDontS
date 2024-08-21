import { createSlice } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    user: null,
    csrfToken: null, // To store CSRF token
  },
  reducers: {
    setUser(state, action) {
      state.user = action.payload;
    },
    setCsrfToken(state, action) {
      state.csrfToken = action.payload;
    },
    clearUser(state) {
      state.user = null;
    },
  },
});

export const { setUser, setCsrfToken, clearUser } = userSlice.actions;
export default userSlice.reducer;