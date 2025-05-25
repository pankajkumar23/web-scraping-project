import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast, { Toaster } from "react-hot-toast";
import axios from "axios";
import { useForm } from 'react-hook-form';
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome"
import {faEye,faEyeSlash} from "@fortawesome/free-solid-svg-icons"


const SignUpPage = () => {

  const [visiblePassword,setVisiblePassword] = useState(false)
  const [confirmVisiblePassword,setConfirmVisiblePassword] = useState(false)
  const navigate = useNavigate()

  const {
      register,
      handleSubmit,
      formState: { errors,isSubmitting },
      watch,
      reset
    } = useForm({mode:"onChange"});

    const password = watch("password")



const passwordVisibilityToggle =()=>{
  setVisiblePassword(!visiblePassword)

}


const confirmPasswordVisibilityToggle =()=>{
  setConfirmVisiblePassword(!confirmVisiblePassword)

}


  const signUpHandler = async (data) => {
    const signUpData = {
      ...data,
      email: data.email.trim().toLowerCase(),
      username: data.username.trim().toLowerCase(),
      password: data.password.trim(),
      confirm_password: data.confirm_password.trim()
    };
     console.log(signUpData);
     
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/signup",
          signUpData
        );
        if (response.data) {
          console.log("reponse from backend",response.data);
          toast.success("Successfully Signup");
          reset()
          navigate("/login")
        } 
        else {
          toast.error("failed Signup");
        }
        
      } catch (error) {
        if (error.response) {
          const msg = error.response.data?.message || "signup failed";
          toast.error(msg);
          console.log("backend error message", msg);
        } else if (error.request) {
          
          toast.error("no response from server");
          console.log("no response received", error.request);
        } else {
          
          toast.error("Something went wrong");
          console.log("error message", error.message);
        }
      } 
    }
  return ( 
    <form onSubmit={handleSubmit(signUpHandler)}>
    <div className="h-210  bg-gray-100 flex flex-col items-center justify-center">
      <span className="w-full font-bold text-center text-xl  text-purple-800">
        Scrapy
      </span>
      <div className="rounded-md  shadow-2xl w-110 h-160  pl-10 pt-10 ">
        <div className="">
        <label htmlFor="username">Username<sup className="text-red-500">*</sup></label>
        <br />
        <input {...register("username",{
          required:"username must required!!",
          minLength:{value:3,message:'username must be at least 3 characters'}

        })}

          type="text"
          placeholder="Your Name"
          className= {`bg-white rounded-md w-90 px-5  h-9 ${errors.username ? "border-red-500 border" : "border border-gray-500"}`}
          
          name="username"
        />
         <span className="text-red-500 text-sm block  h-5"> {errors.username?.message || ""}</span>
        </div>

        <br />
        <div className="">
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
          placeholder="Email address"
          className= {`bg-white rounded-md w-90 px-5  h-9 ${errors.email ? "border border-red-500 " : "border border-gray-500"}`}
          
          name="email"
        />
        <span className="text-red-500 text-sm block  h-5"> {errors.email?.message||""}</span>
        </div>
        <br />
        <div className="">
        <label htmlFor="password">Password<sup className="text-red-500">*</sup></label>
        <br />
        <input  {...register("password",{
          required:"password must required!!",
          pattern: {
            value :/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/,
            message :"Password contain must be at leat 8 characters,at least 1 uppercase, number, and 1 special character",
          }
        })}
          type= {visiblePassword ?"text":"password"}
          placeholder="password"
          className= {`bg-white rounded-md w-90  px-5  h-9 ${errors.password ? "border border-red-500" : "border border-gray-500"} `}
          name="password"
        />
        <span className="flex justify-end items-end" onClick={passwordVisibilityToggle}><FontAwesomeIcon icon={visiblePassword ? faEye:faEyeSlash} className="absolute mr-15  mb-2 text-sm"/></span>
         {(<ul className="text-sm  mt-1 ml-1   list-disc ">
          <li className={`${/.{8,}/.test(password)?"text-green-500" : "text-gray-500"}`}>
          at least 8 charaters </li>
          <li className={`${/[A-Z]/.test(password)?"text-green-500" : "text-gray-500"}`}>
          uppcase 
          
          </li>
          <li className={`${/[a-z]/.test(password)?"text-green-500" : "text-gray-500"}`}>
          lowercase
          </li>
          <li className={`${/[0-9]/.test(password)?"text-green-500" : "text-gray-500"}`}>
          numbers
          </li>
          <li className={`${/[#?!@$%^&*-]/.test(password)?"text-green-500" : "text-gray-500"}`}>
          special character
          </li>
         
         </ul>)}
         </div>
        <br />
        <div className="">
        <label htmlFor="confirm_password">Confirm Password<sup className="text-red-500">*</sup></label>
        <br />
        <input   {...register("confirm_password",{
          required: "confirm password must required!!",
          validate :(value)=>
            value === password || "Password not match"
        })}
        type= {confirmVisiblePassword ?"text":"password"}
          placeholder="Enter Confirm Password "
          className= {`bg-white rounded-md w-90 px-5  h-9 ${errors.confirm_password ? "border border-red-500" : "border border-gray-500"}`}
          
          name="confirm_password"
        />
        <span className="flex justify-end items-end" onClick={confirmPasswordVisibilityToggle}><FontAwesomeIcon icon={confirmVisiblePassword ? faEye:faEyeSlash} className="absolute mr-15  mb-2 text-sm"/></span>
        <span className="text-red-500 text-sm block  h-5"> {errors.confirm_password?.message ||""}</span>
       </div>
        <br />
        <input type="submit"  disabled ={isSubmitting} value={isSubmitting ? "Submitting":"Sign up"}
          className="rounded-md w-90  bg-purple-800 text-white h-10   cursor-pointer "
        />
        <p>
          Have an account?{" "}
          <Link to="/login" className="text-purple-800">
            Login
          </Link>
        </p>
       
      </div>
    </div>
    </form>
  );
};

export default SignUpPage;
