import { updateQuestions } from "./questionsSlice";
import { csrfFetch } from "../csrf";

export const getQuestions = (data) => async(dispatch) => {
    try {
        const { chapter, type, topics } = data;

        const topicsParam = encodeURIComponent(JSON.stringify(topics))
        const response = await csrfFetch(`/api/quiz/questions?chapter=${chapter}&type=${type}&topics=${encodeURIComponent(topicsParam)}`);

    
    if (!response.ok) {
        // Log the status and response text for debugging
        const errorText = await response.text();
        console.error('Error response status:', response.status);
        console.error('Error response body: ', errorText);
        // Optionally, throw an error to handle it later in the catch block
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const results = await response.json()
      dispatch(updateQuestions(results))
    } catch (error) {
        console.error(error)
    }
}