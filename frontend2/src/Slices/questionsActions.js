import { updateQuestions } from "./questionsSlice";
import { csrfFetch } from "../csrf";

export const getQuestions = (chapter_id) => async(dispatch) => {
    try {
        const response = await csrfFetch(`/api/quiz/${chapter_id}`)
    
    if (!response.ok) {
        // Log the status and response text for debugging
        const errorText = await response.text();
        console.error('Error response status:', response.status);
        console.error('Error response body: ', errorText);
        // Optionally, throw an error to handle it later in the catch block
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const data = await response.json()
      dispatch(updateQuestions(data))
    } catch (error) {
        console.error(error)
    }
}