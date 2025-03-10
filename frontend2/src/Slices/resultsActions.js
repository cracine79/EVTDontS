import { csrfFetch } from "../csrf";
import { updateUserResults } from "./resultsSlice";
import { updateUserChapters } from "./userChaptersSlice";
import { updateUser, login } from "./userSlice";
import { useNavigate } from "react-router-dom";
import { updateTopicProg } from "./topicProgSlice";
import { updateTopics } from "./topicsSlice";


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
        dispatch(updateUserChapters(data.chapters))
        dispatch(login(data.user))  //to update newest chapter
        dispatch(updateUserResults(data.answers))  //Kept in frontend temporarily to show results
        dispatch(updateTopicProg(data.topic_progress))
        dispatch(updateTopics(data.topics))
        return (data.last_chapter)

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
    try{
        const response = await csrfFetch('/api/progress/chapter', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
             
            },
            body: JSON.stringify(chapterData)
        })
        const data = await response.json()
        dispatch(updateUser(data))
        return data
        
    } catch(error){
        console.log('error during data submission:', error);
        return Promise.reject(error)
    }
}