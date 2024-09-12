import { createSlice } from "@reduxjs/toolkit";


const resultsSlice = createSlice({
    name: 'results',
    initialState: {},
    reducers: {
        storeUserResults: (state, action) => {
            return action.payload
        },
        updateUserResults: (state, action)=>{
            return {
                ...state,
                ...action.payload
            }
        },
        clearUserResults: (state, action)=>{
            return {}
        }
    }
})

export const {storeUserResults, updateUserResults, clearUserResults} = resultsSlice.actions
export default resultsSlice.reducer