import { createSlice } from "@reduxjs/toolkit";

const questionsSlice = createSlice({
    name: 'questions',
    initialState:{},
    reducers: {
        saveNewQuestions: (state, action) => {
            return action.payload
        },
        clearQuestions: (state) => {
            return {}
        },
        updateQuestions: (state, action) => {
            return{
                ...state,
                ...action.payload
            }
        }
    }
})

export const {saveNewQuestions, clearQuestions, updateQuestions} = questionsSlice.actions
export default questionsSlice.reducer