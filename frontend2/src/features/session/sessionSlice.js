import { createSlice } from "@reduxjs/toolkit";


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



export const { loginUser, logoutUser, setError } = userSlice.actions;

export default userSlice.reducer;