import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import csrfFetch from "./csrf";  // Assuming you have csrfFetch properly set up

const SESSION_LOGIN_USER = 'session/loginUser';

const initialState = {
  user: null,
  email: null,
  loggedIn: false,
  loading: false,
  error: null
};

// Async thunk for login
export const loginUser = createAsyncThunk(
  SESSION_LOGIN_USER,
  async ({ username, password }, { rejectWithValue }) => {
    try {
      const res = await csrfFetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        headers: { 'Content-Type': 'application/json' }
      });

      const data = await res.json();
      console.log('Login success data:', data);  // Log the data for debugging

      if (res.status >= 400) {
        return rejectWithValue(data);
      }

      return data;  // Success case
    } catch (err) {
      console.error('Login error mofo:', err);  // Log the error
      return rejectWithValue(err.message);
    }
  }
);

// Create the user slice
export const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    logoutUser(state) {
      state.user = null;
      state.email = null;
      state.loggedIn = false;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.user = action.payload.username;
        state.email = action.payload.email;
        state.loggedIn = true;
        localStorage.setItem('token', action.payload.access_token); // Assuming a token is returned
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

// Export the actions and reducer
export const { logoutUser } = userSlice.actions;
export default userSlice.reducer;

// Restore session function
export const restoreSession = () => async (dispatch) => {
  const res = await csrfFetch('/api/csrf/');
  const data = await res.json();
  sessionStorage.setItem('X-CSRF-Token', data.csrf_token);
};
