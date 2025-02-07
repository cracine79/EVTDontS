import { csrfFetch } from "../csrf";
import { updateUserChapters } from "./userChaptersSlice";


export const updateVideoProgress = async(chapterId) => {
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
