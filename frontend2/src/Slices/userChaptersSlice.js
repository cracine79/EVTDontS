import { createSlice } from "@reduxjs/toolkit";

const userChaptersSlice = createSlice({
    name: 'userChapters',
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
            return{}
        }
    }
})

export const { storeUserChapters, updateUserChapters, clearUserChapters } = userChaptersSlice.actions
export default userChaptersSlice.reducer