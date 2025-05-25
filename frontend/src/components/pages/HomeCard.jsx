import React from 'react'
import { Link } from 'react-router-dom'
const HomeCard = ({id,hotel_name,img_link,price,availability,roomtype_bed ,roomtype}) => {
  return (
    <div className=' h-80 w-200 shadow-2xl rounded-xl pt-8  pb-8 pl-5 flex flex-row ' key={id}>

        <div className=' shadow-2xl h-60 w-60 flex flex-row' > 
            <Link to="/availability"><img className='  h-full rounded-xl cursor-pointer' src={img_link} /></Link>
        </div>
      <div className=' flex flex-row w-100 h-60'>
        <div className='ml-5 flex flex-col pt-2'>
        <p className='h-15 w-80  text-blue-800   text-xl font-bold '> {hotel_name}</p>
        <p className=' w-90 font-bold'>{roomtype}</p>
        <p className='text-sm font-light'>{roomtype_bed.replace("Choose your bed (if available)","")}</p>
        </div>
        </div>  
        <div className=' w-40 h-60  pt-25 '>
        <p className='  w-20  ml-15 pl-4 flex justify-center items-center'>{price}</p>
        <Link to='/availability'><p className='   rounded-md h-10 w-35  mt-5 flex justify-center items-center text-white bg-blue-800 cursor-pointer'>See availability</p></Link></div>
      </div>
      
  )
}

export default HomeCard