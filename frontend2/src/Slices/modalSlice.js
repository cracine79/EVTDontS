import {createSlice} from '@reduxjs/toolkit'


const modalSlice = createSlice({
    name: 'modal',
    initialState: {
        isLoginOpen: false,
        isSignupOpen: false
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
        }
    }
})

export const {openLoginModal, closeLoginModal, openSignupModal, closeSignupModal} = modalSlice.actions
export default modalSlice.reducer;