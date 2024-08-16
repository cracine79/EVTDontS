import {configureStore, combineSlices} from "@reduxjs/toolkit"
import { userSlice } from "../features/session/sessionSlice"


const rootReducer = combineSlices(userSlice)
const store = configureStore({
    reducer: rootReducer,
})

export default store