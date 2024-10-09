import { csrfFetch } from "../csrf";
import { storeUserUnits } from "./unitsSlice";
import { storeUserChapters } from "./userChaptersSlice";
import { storeChapters } from "./chaptersSlice";
import { updateUser } from "./userSlice";


export const addUserUnits = (units) => async(dispatch) => {
    try{
        const response = await csrfFetch('/api/units/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(units)
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
      console.log(data)
      dispatch(storeUserUnits(data.units))
      dispatch(updateUser(data.user))
      dispatch(storeUserChapters(data.user_chapters))
      dispatch(storeChapters(data.chapters))
      

      
    } catch(error) {
        console.error('Error during answer submission:', error);
    }
}