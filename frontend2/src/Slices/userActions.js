import { login, logout } from "./userSlice";
import { csrfFetch } from "../csrf";
import { useDispatch } from "react-redux";



export const restoreUser = () => async(dispatch) => {

    try {

      const response = await csrfFetch('/api/auth/refreshuser');
      if (response.ok) {
        const data = await response.json();
     
  
        // Dispatch the login action from userSlice
        dispatch(login({
          username: data.username,
          email: data.email
        }));
      } else {
        dispatch(logout());
      }
    } catch (error) {
      console.error('Failed to restore user:', error);
      dispatch(logout());
    }
  };