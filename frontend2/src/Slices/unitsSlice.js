import { createSlice } from "@reduxjs/toolkit";



const unitsSlice = createSlice({
    name: 'units',
    initialState:{},
    reducers: {
        storeUserUnits: (state, action) => {
            return action.payload
        },
        clearUserUnits: (state, action) => {
            return {}
        }
    }
})

export const {storeUserUnits, clearUserUnits} = unitsSlice.actions;
export default unitsSlice.reducer