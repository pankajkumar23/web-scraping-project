import React, { useEffect } from 'react'
import {jwtDecode} from "jwt-decode"
import Navbar from './Navbar'
import { useNavigate } from 'react-router-dom'
const ProfilePage = () => {
  let navigate = useNavigate()

  useEffect(()=>{
    if (! localStorage.getItem("token")){
      navigate('/login')
    }
  },[navigate])

let token= localStorage.getItem("token")
let user=jwtDecode(token)
console.log(user);
  return (
 <>
 <div className=' h-screen flex justify-center items-center text-2xl'>

    welcome, {user.sub.username}
 </div>
 </>
  )
}

export default ProfilePage