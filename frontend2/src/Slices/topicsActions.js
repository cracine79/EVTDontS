import { csrfFetch } from "../csrf"
import { updateTopics } from "./topicsSlice"

export const getAllTopics = () => async(dispatch) => {
    try{
        const response = await csrfFetch('api/topics')

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response status:', response.status);
            console.error('Error response body: ', errorText);
            throw new Error(`Error ${response.status}: ${errorText}`);
            }
        
        const results = await response.json()

        dispatch(updateTopics(results.topics))

    } catch(error){
        console.error(error)
    }
}