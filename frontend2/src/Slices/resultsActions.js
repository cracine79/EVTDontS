import { csrfFetch } from "../csrf";
import { updateUserResults } from "./resultsSlice";

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
      
    } catch(error) {
        console.error('Error during answer submission:', error);
    }
}

export const finishQuiz = (quizData) => async(dispatch) => {
    console.log(quizData)
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
    } catch(error){
        Console.log('Error during data submission:', error)
    }
}