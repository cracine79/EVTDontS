import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { useEffect } from "react";
import csrfFetch from "./csrf";
const SESSION_LOGIN_USER = 'session/loginUser'
import axios from 'axios'


// export const loginUser = createAsyncThunk(
//   SESSION_LOGIN_USER,
//   async({username, password}, {rejectWithValue})=>{
//     try{
//       const response = await fetch('api/session/login', {username, password});
//     }
//   })

// )
const initialState = {
    user: null,
    email: null,
    loggedIn: false,
    error: null
  };

  export const loginUser = createAsyncThunk(
    'auth/loginUser',
    async ({ username, password }, { rejectWithValue }) => {
      try {
        const response = await axios.post('/api/auth/login', { username, password });
        return response.data;
      } catch (error) {
        return rejectWithValue(error.response.data);
      }
    }
  );

  export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
      logoutUser(state) {
        state.user = null;
        state.email = null;
        state.loggedIn = true;
      },
      extraReducers: (builder) => {
        // Handle login
        builder
          .addCase(loginUser.pending, (state) => {
            state.loading = true;
            state.error = null;
          })
          .addCase(loginUser.fulfilled, (state, action) => {
            state.loading = false;
            state.user = action.payload.user;
            state.email=action.payload.email
            state.loggedIn = true;
            localStorage.setItem('token', action.payload.access_token); // Assuming a token is returned
          })
          .addCase(loginUser.rejected, (state, action) => {
            state.loading = false;
            state.error = action.payload;
          })
      }
    },
  });

  export const storeCSRFToken = response => {

    const csrfToken = response['csrf_token'];
    if (csrfToken) sessionStorage.setItem("X-CSRF-Token", csrfToken);
  };

  export const restoreSession = () => async dispatch => {
    let res = await csrfFetch('/api/csrf/');
    let outcome = await res.json()
    storeCSRFToken(outcome);
  }

  export const login = user => async dispatch => {
    let res = await csrfFetch('/api/auth/login')
  }


export const { logoutUser } = userSlice.actions;

export default userSlice.reducer;