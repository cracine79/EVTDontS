import { createSlice } from "@reduxjs/toolkit";

export const startChapterProgress = async(chapterId, userId) => {
    try{
        const response = await csrfFetch('/api/progress/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
              },
            body: JSON.stringify({ chapter_id: chapterId, user_id: userId }),
        });

    const data = await response.json()
    
    dispatchEvent(createSlice())

    } catch (error) {
        console.error('Error finding', error)
    }
}

const chaptersSlice = createSlice({
    name: 'chapters',
    initialState: {},
    reducers: {
        storeUserChapters: (state, action) => {
            return action.payload
        },
        updateUserChapters: (state, action) => {
            const {chapterId, updates} = action.payload;

            if(state[chapterId]){
                state[chapterId] = {
                    ...state[chapterId],
                    ...updates
                }
            }
        }
    }
})

export const {storeUserChapters, updateUserChapters} = chaptersSlice.actions
export default chaptersSlice.reducer