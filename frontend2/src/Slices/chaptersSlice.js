import { createSlice } from "@reduxjs/toolkit";

const chaptersSlice = createSlice({
    name: 'chapters',
    initialState: {},
    reducers: {
        storeUserChapters: (state, action) => {
            return action.payload
        }
    }
})

export const {storeUserChapters} = chaptersSlice.actions
export default chaptersSlice.reducer