import { login, logout } from "./userSlice";
import { csrfFetch } from "../csrf";
import { useDispatch } from "react-redux";
import { storeUserUnits } from "./unitsSlice";



export const restoreUser = () => async(dispatch) => {

    try {

      const response = await csrfFetch('/api/auth/refreshuser');
      if (response.ok) {
        const data = await response.json();
     
  
        // Dispatch the login action from userSlice
        dispatch(login({
          username: data.user.username,
          email: data.user.email
        }));
        dispatch(storeUserUnits(data.units))
      } else {
        dispatch(logout());
      }
    } catch (error) {
      console.error('Failed to restore user:', error);
      dispatch(logout());
    }
  };