import { createSlice } from "@reduxjs/toolkit"


const pageSlice = createSlice({
    name:'page',
    initialState:{
        value : null,
        error :null,
        loading:false
    },
    reducers:{
        setData : (state,action)=>{
            state.value = action.payload
        }

    }
})

export const  {setData} = pageSlice.actions
export default  pageSlice.reducer


