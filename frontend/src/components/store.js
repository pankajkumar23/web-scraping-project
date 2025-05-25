import {configureStore} from "@reduxjs/toolkit";

import pageSlice from "./pageSlice"


const store = configureStore({
    reducer:{
        data:pageSlice
    }
})

export default store