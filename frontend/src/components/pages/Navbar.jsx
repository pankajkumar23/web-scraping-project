import React from 'react'
import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'
import toast,{Toaster} from 'react-hot-toast'
import 'core-js/stable/atob';
const Navbar = () => {

let navigate = useNavigate()
let isLoggedIn = localStorage.getItem("token")

const LogoutPage = () => {
  localStorage.removeItem("token","")
  toast.success("logout sucessfully!!")
  navigate("/")
}
return (
   <>
        <div className='w-full bg-gray-100  '>
          <Toaster/>
            <ul className='  h-20 flex justify-evenly items-center text-xl '>
              <Link to='/'><li className='rounded-md w-20 bg-purple-800 text-white cursor-pointer text-center p-1'>Home</li></Link> 
              { isLoggedIn ? <Link  onClick={LogoutPage}> <li className='rounded-md w-20 bg-purple-800 text-white cursor-pointer text-center p-1' >Logout</li></Link> 
              :<Link to='/login'> <li className='rounded-md w-20 bg-purple-800 text-white cursor-pointer text-center p-1'>Login</li></Link>}
             { isLoggedIn? <Link to='/profile'><li className='rounded-md w-20 bg-purple-800 text-white cursor-pointer text-center p-1'>Profile</li></Link>:null}
            </ul> 
        </div>
</>
  )
}

export default Navbar