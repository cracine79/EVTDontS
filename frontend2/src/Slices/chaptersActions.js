import { csrfFetch } from "../csrf"
import { updateChapters } from "./chaptersSlice";

export const getAllChapters = () => async(dispatch) => {
    try {
        const response = await csrfFetch('api/chapters')
    
        if (!response.ok) {
            // Log the status and response text for debugging
            const errorText = await response.text();
            console.error('Error response status:', response.status);
            console.error('Error response body: ', errorText);
            // Optionally, throw an error to handle it later in the catch block
            throw new Error(`Error ${response.status}: ${errorText}`);
          }
        
          const results = await response.json()
          dispatch(updateChapters(results.chapters))

    } catch(error){
        console.error(error)
    }
}


export const getChapterBlurb = async(chapterId) => {
    try {
        console.log('next')
        console.log(chapterId)
        const response = await csrfFetch(`/api/chapters/blurb/${chapterId}`)
    
    if (!response.ok) {
        const errorText = await response.text();
        console.error('Error response status:', response.status);
        console.error('Error response body: ', errorText);
        throw new Error(`Error ${response.status}: ${errorText}`);
        }
    
        const results = await response.json()

        return results.video_blurb
        
    } catch(error){
        console.error(error)
    }
}