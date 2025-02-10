import { csrfFetch } from "../csrf";
import { updateUserChapters } from "./userChaptersSlice";
import { useDispatch } from "react-redux";

export const updateVideoProgress = (chapterId) => async(dispatch) => {
        try {
            const response = await csrfFetch('/api/progress/' , {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                  },
                body: JSON.stringify({ chapter_id: chapterId }),
            });

        const data = await response.json()

        dispatch(updateUserChapters(data))
        } catch (error) {
            console.error("error finding", error)
        }
    }
