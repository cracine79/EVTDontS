import {createSlice} from '@reduxjs/toolkit'


const modalSlice = createSlice({
    name: 'modal',
    initialState: {
        isLoginOpen: false,
        isSignupOpen: false,
        isQuizOpen: false,
        isResultsOpen: false,
        sourceData: null
    },
    reducers: {
        openLoginModal: (state) => {
            state.isLoginOpen = true
        },
        closeLoginModal: (state)=> {
            state.isLoginOpen = false;
        },
        openSignupModal: (state, action) => {
            state.isSignupOpen = true;
            state.sourceData = action.payload || null;
        },
        closeSignupModal: (state)=> {
            state.isSignupOpen = false;
            state.sourceData = null;
        },
        openQuizModal: (state) => {
            state.isQuizOpen = true
        },
        closeQuizModal: (state) => {
            state.isQuizOpen = false
        },
        openResultsModal: (state) => {
            state.isResultsOpen = true
        },
        closeResultsModal: (state) => {
            state.isResultsOpen = false
        }
    }
})

export const {openLoginModal, closeLoginModal, openSignupModal, closeSignupModal, openQuizModal, closeQuizModal, openResultsModal, closeResultsModal} = modalSlice.actions
export default modalSlice.reducer;