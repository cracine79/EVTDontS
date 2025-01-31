import { login, logout } from "./userSlice";
import { csrfFetch } from "../csrf";
import { useDispatch } from "react-redux";
import { storeUserUnits } from "./unitsSlice";
import { storeUserChapters } from "./userChaptersSlice";
import { storeTopicProg } from "./topicProgSlice";
import { storeChapters } from "./chaptersSlice";
import { updateChapters } from "./chaptersSlice";
import { storeTopics } from "./topicsSlice";



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


export const loginUser = (username, password) => async(dispatch) => {
  try {
    const response = await csrfFetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      // Log the status and response text for debugging
      const errorText = await response.text();
      console.error('Error response status:', response.status);
      console.error('Error response body: ', errorText);
      // Optionally, throw an error to handle it later in the catch block
      throw new Error(`Error ${response.status}: ${errorText}`);
    }
   
    const data = await response.json();
    localStorage.setItem('access_token', data.user.access_token);
    dispatch(login(data.user));
    dispatch(storeUserUnits(data.units))
    dispatch(updateChapters(data.chapters))
    dispatch(storeTopicProg(data.topic_progress))
    dispatch(storeUserChapters(data.user_chapters))
    dispatch(storeTopics(data.topics))

    return {success: true}
 
  } catch (error) {
    // Log any errors that occur during fetch or processing
    console.error('Error during login:', error);
    return {error: error.message }
  }
  };

  export const signupUser = (username, email, password, quizData) => async(dispatch)  => {
    try{
      const response = await csrfFetch('/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password, quizData }),
      });
      const data = await response.json();
      localStorage.setItem('access_token', data.user.access_token);
      dispatch(login(data.user));
      return {success: true}
    } catch (error) {
      return {error: error.message}
    }
  }