import {createSlice} from '@reduxjs/toolkit'


const modalSlice = createSlice({
    name: 'modal',
    initialState: {
        isLoginOpen: false,
        isSignupOpen: false,
        isQuizOpen: false
    },
    reducers: {
        openLoginModal: (state) => {
            state.isLoginOpen = true
        },
        closeLoginModal: (state)=> {
            state.isLoginOpen = false
        },
        openSignupModal: (state) => {
            state.isSignupOpen = true
        },
        closeSignupModal: (state)=> {
            state.isSignupOpen = false
        },
        openQuizModal: (state) => {
            state.isQuizOpen = true
        },
        closeQuizModal: (state) => {
            state.isQuizOpen = false
        },
    }
})

export const {openLoginModal, closeLoginModal, openSignupModal, closeSignupModal} = modalSlice.actions
export default modalSlice.reducer;