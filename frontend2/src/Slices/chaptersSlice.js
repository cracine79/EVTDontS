import { createSlice } from "@reduxjs/toolkit";

// const updateChapterProgress = async(chapterId, userId)

const chaptersSlice = createSlice({
    name: 'chapters',
    initialState: {},
    reducers: {
        storeChapters: (state, action) => {
            return action.payload
        },
        updateChapters: (state, action) => {
            return {
                ...state,
                ...action.payload
            }

        }, 
        clearChapters: (state) => {
            return {}
        }
     }
})

export const {storeChapters, updateChapters, clearChapters} = chaptersSlice.actions
export default chaptersSlice.reducer 