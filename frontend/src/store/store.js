import {configureStore, combineSlices} from "@reduxjs/toolkit"
import userSlice from "./userSlice"
import thunk from "redux-thunk";


const rootReducer = combineSlices(userSlice)
const store = configureStore({
    reducer: rootReducer,
    middleware: [thunk],
    devTools: process.env.NODE_ENV !== 'production',
})

export default store