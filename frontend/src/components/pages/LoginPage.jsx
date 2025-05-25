import { Link } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useForm } from 'react-hook-form';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome"
import {faEye,faEyeSlash} from "@fortawesome/free-solid-svg-icons"
import { useState } from "react";

const LoginPage = () => {


  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm({mode:"onChange"});



  const [visiblePassword,setVisiblePassword] = useState(false)



  const passwordVisibilityToggle =()=>{
    setVisiblePassword(!visiblePassword)
  }
  

const navigate = useNavigate()
  

  const loginHandler = async (data) => {
    const loginData = {
      ...data,
      email: data.email.trim().toLowerCase(),
      password: data.password.trim(),
      
    };
  
    console.log("loginData", loginData);
      try {
        let response = await axios.post("http://127.0.0.1:8000/login", loginData)
        if (response.data) {
          
          toast.success("Successfully login");
          reset()
          let token = response.data.message["access_token"]
          
          if (token) {
            console.log(token);
            localStorage.setItem("token",token)
            localStorage.setItem("user",response.data.message["email"])
            navigate("/profile")
          }
          else{
            console.log("token not found");
            
          }
        }
        else{
          console.log("failed to response from backend");
          toast.error("failed login");
        }
    
      } catch (error) {
        console.log("error at login api", error);
        if (error.response) {
      
          const msg = error.response.data?.message || "login failed";
          toast.error(msg);
          console.log("backend error message", msg);
        } else if (error.request) {
          
          toast.error("no response from server");
          console.log("no response received", error.request);
        } else {
          
          toast.error("Something went wrong");
          console.log("error", error.message);
        }
      }
    }

  return (
    <form onSubmit={handleSubmit(loginHandler)}>
      <Toaster/>
    <div className=" h-210  bg-gray-100 flex flex-col items-center justify-center">
      
      <span className="w-full font-bold text-center text-xl  text-purple-800">
        Scrapy
      </span>
      <div className="rounded-md shadow-2xl w-110 h-130 pl-10 pt-30  ">
        <div>
        <label htmlFor="email">Email address<sup className="text-red-500">*</sup></label>
        <br />
        <input {...register("email",{
          required:"email must required!!",
          pattern:{ 
            value:/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
            message :"enter valid email!!",
          }
        })}
          type="email"
          placeholder="your@email.address"
          className= {`bg-white rounded-md w-90 px-5  h-9 ${errors.email ? "border border-red-500 " : "border border-gray-500"}`}
          name="email"
        />
        <span className="text-red-500 text-sm block h-5"> {errors.email?.message||""}</span>
          </div>
        <br />
      <div>
        <label htmlFor="password">Password<sup className="text-red-500">*</sup> </label>
        <br />
        <input  {...register("password",{
          required:"password must required!!",
        })}
        type ={visiblePassword?"text":"password"}
          placeholder="Your secret Password "
          className= {`bg-white rounded-md w-90 px-5 h-9 ${errors.password ? "border border-red-500" : "border border-gray-500"}`}
          name="password"
        />
        <span className="flex justify-end items-end" onClick={passwordVisibilityToggle}><FontAwesomeIcon icon={visiblePassword ? faEye:faEyeSlash} className="absolute mr-15  mb-2 text-sm"/></span>
      <span className="text-red-500 text-sm block h-5"> {errors.password?.message||""}</span>
        </div>
        <br />
        
        <input type="submit" value="Login"
          className="rounded-md w-90 bg-purple-800 text-white h-10   cursor-pointer "
        />
       
        <p>
          Don't have account?{" "}
          <Link to="/signup" className="text-purple-800">
            Sign up
          </Link>
        </p>
      </div>
    </div>
    </form>
  );
};

export default LoginPage;
