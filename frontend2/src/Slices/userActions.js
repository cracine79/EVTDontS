import { login, logout } from "./userSlice";
import { csrfFetch } from "../csrf";
import { useDispatch } from "react-redux";
import { storeUserUnits } from "./unitsSlice";
import { storeUserChapters } from "./userChaptersSlice";
import { storeTopicProg } from "./topicProgSlice";
import { storeChapters } from "./chaptersSlice";



export const restoreUser = () => async(dispatch) => {

    try {

      const response = await csrfFetch('/api/auth/refreshuser');
      if (response.ok) {
        const data = await response.json();
     
  
        // Dispatch the login action from userSlice
        dispatch(login({
          username: data.user.username,
          email: data.user.email,
          current_chapter: data.user.current_chapter
        }));
        dispatch(storeUserUnits(data.units))
        dispatch(storeChapters(data.chapters))
        dispatch(storeTopicProg(data.topic_progress))
        dispatch(storeUserChapters(data.user_chapters))
      } else {
        dispatch(logout());
      }
    } catch (error) {
      console.error('Failed to restore user:', error);
      dispatch(logout());
    }
  };