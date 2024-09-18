import { csrfFetch } from "../csrf";
import { updateUserResults } from "./resultsSlice";
import { updateUserChapters } from "./chaptersSlice";
import { updateUser, login } from "./userSlice";
import { useNavigate } from "react-router-dom";


export const addResults = (results) => async(dispatch) => {
    try{
        const response = await csrfFetch('/api/results/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(results)
        })
    
    if (!response.ok) {
        // Log the status and response text for debugging
        const errorText = await response.text();
        console.error('Error response status:', response.status);
        console.error('Error response body: ', errorText);
        // Optionally, throw an error to handle it later in the catch block
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const data = await response.json()
      dispatch(updateUserResults(data))
      dispatch(updateUser(user))

      
    } catch(error) {
        console.error('Error during answer submission:', error);
    }
}

export const finishQuiz = (quizData) => async(dispatch) => {

    try{
        const response = await csrfFetch('/api/progress/finishquiz', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(quizData)
        })

        const data = await response.json()
        console.log(data.user)
        dispatch(updateUserChapters(data.chapters))
        dispatch(login(data.user))

        


    } catch(error){
        console.log('Error during data submission:', error)
    }
}