import { createSlice } from "@reduxjs/toolkit";

const topicsSlice = createSlice({
    name: 'topics',
    initialState: {},
    reducers: {
        storeTopics: (state, action) => {
            return action.payload
        },
        updateTopics: (state, action) => {
            return {
                ...state,
                ...action.payload
            }
        },
        clearTopics: (state) => {
            return {}
        }
    }
})


export const {storeTopics, updateTopics, clearTopics} = topicsSlice.actions
export default topicsSlice.reducer
