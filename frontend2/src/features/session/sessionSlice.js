import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { useEffect } from "react";
import csrfFetch from "./csrf";
const SESSION_LOGIN_USER = 'session/loginUser'


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
    email: "dude@dude.com",
    loggedIn: true,
    error: null
  };

  export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
      loginUser(state, action) {
        state.user = action.payload.username;
        state.email = action.payload.email;
        state.loggedIn = true;
      },
      logoutUser(state) {
        state.user = null;
        state.email = null;
        state.loggedIn = true;
      },
      setError(state, action) {
        state.error = action.payload;
      },
    },
  });

  export const storeCSRFToken = response => {

    const csrfToken = response.headers.get("X-CSRF-Token");
    if (csrfToken) sessionStorage.setItem("X-CSRF-Token", csrfToken);
  };

  export const restoreSession = () => async dispatch => {
    let res = await csrfFetch('/api/csrf');
    storeCSRFToken(res);
    return res;
  }


export const { loginUser, logoutUser, setError } = userSlice.actions;

export default userSlice.reducer;