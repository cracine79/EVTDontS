import { createSlice } from "@reduxjs/toolkit";

// const updateChapterProgress = async(chapterId, userId)

const chaptersSlice = createSlice({
    name: 'chapters',
    initialState: {},
    reducers: {
        storeChapters: (state, action) => {
            return action.payload
        },
        // Merge field by field, so loading every chapter doesn't drop what we know about plan chapters (in_plan etc.)
        updateChapters: (state, action) => {
            const merged = { ...state }
            Object.entries(action.payload || {}).forEach(([id, chapter]) => {
                merged[id] = { ...(state[id] || {}), ...chapter }
            })
            return merged
        },
        clearChapters: (state) => {
            return {}
        }
     }
})

export const {storeChapters, updateChapters, clearChapters} = chaptersSlice.actions
export default chaptersSlice.reducer 