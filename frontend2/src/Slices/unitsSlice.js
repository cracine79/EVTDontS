import { createSlice } from "@reduxjs/toolkit";



const unitsSlice = createSlice({
    name: 'units',
    initialState:{},
    reducers: {
        storeUserUnits: (state, action) => {
            return action.payload
        }
    }
})

export const {storeUserUnits} = unitsSlice.actions;
export default unitsSlice.reducer