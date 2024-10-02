import { createSlice } from "@reduxjs/toolkit";


const topicProgSlice = createSlice({
    name: 'topicProg',
    initialState: {},
    reducers: {
        storeTopicProg: (state, action) => {
            return action.payload
        },
        updateTopicProg: (state, action) => {
            return {
                ...state,
                ...action.payload
            }
        },
        clearTopicProg: (state) => {
            return{}
        }
    }

})

export const { storeTopicProg, updateTopicProg, clearTopicProg } = topicProgSlice.actions
export default topicProgSlice.reducer