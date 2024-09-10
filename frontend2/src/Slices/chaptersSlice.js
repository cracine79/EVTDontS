import { createSlice } from "@reduxjs/toolkit";

// const updateChapterProgress = async(chapterId, userId)

const chaptersSlice = createSlice({
    name: 'chapters',
    initialState: {},
    reducers: {
        storeUserChapters: (state, action) => {
            return action.payload
        },
        updateUserChapters: (state, action) => {
            return {
                ...state,
                ...action.payload
            }

        }, 
        clearUserChapters: (state) => {
            return {}
        }
     }
})

export const {storeUserChapters, updateUserChapters, clearUserChapters} = chaptersSlice.actions
export default chaptersSlice.reducer