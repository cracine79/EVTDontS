import { csrfFetch } from "../csrf";
import { updateUserResults } from "./resultsSlice";
import { updateUserChapters } from "./chaptersSlice";
import { updateUser, login } from "./userSlice";
import { useNavigate } from "react-router-dom";
import { updateTopicProg } from "./topicProgSlice";


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
    //   dispatch(updateUser(user))

      
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
        console.log(data)
        dispatch(updateUserChapters(data.chapters))
        dispatch(login(data.user))
        console.log(data.answers)
        dispatch(updateUserResults(data.answers))
        dispatch(updateTopicProg(data.topic_progress))

    } catch(error){
        console.log('Error during data submission:', error)
    }
}

export const finishReviewQuiz = (quizData) => async(dispatch) => {
    try{
        const response = await csrfFetch('/api/progress/finishreviewquiz', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(quizData)
        })
        const data = await response.json()
        dispatch(updateUserResults(data.answers))
        dispatch(updateTopicProg(data.topic_progress))
    } catch(error){
        console.log('Error during data submission:', error)
    }
}
 

export const finishChapter = (chapterData)  => async(dispatch) => {
    console.log('Chapter DATA!!', chapterData)
    try{
        const response = await csrfFetch('/api/progress/chapter', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
             
            },
            body: JSON.stringify(chapterData)
        })
        const data = await response.json()
        console.log('Data received from API:', data); // Ensure this logs correctly
        dispatch(updateUser(data))
        console.log(data)
        
    } catch(error){
        console.log('error during data submission:', error)
    }
}