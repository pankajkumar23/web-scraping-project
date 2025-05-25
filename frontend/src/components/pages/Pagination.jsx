import React, { useState } from "react";
import { useDispatch } from "react-redux";




const Pagination = () => {
  const [page, setPage] = useState(1);
  let dispatch = useDispatch()
  dispatch(page)
 
  const nextPageNum = () => {
    setPage((prev) => Math.min(prev + 1, 2));
  };

  const previousePageNum = () => {
    if (page > 1) return setPage((prev) => Math.max(prev - 1));
  };

  const pageNumClick = (pageNum) => {
    setPage(pageNum);
  };

  return (
      
    
    <div className="w-full border-2 h-15  flex flex-row justify-center items-center cursor-pointer">
    
      Page
      <button
        className=" ml-1 rounded-sm p-3 h-10  bg-purple-800 text-white flex justify-center items-center cursor-pointer"
        onClick={previousePageNum}

        
      >
        Prev
      </button>
      {Array.from({ length: 2 }, (_, index) => (
        <button
          className="shadow-2xl rounded-md p-3 h-10  w-10 ml-2 mr-2 text-white bg-purple-800 flex justify-center items-center cursor-pointer" key={index}
          onClick={() => pageNumClick(index + 1)}
        >
          {index + 1}{console.log("pagenumber at pagination.jsx",page)
          }
        </button>
      ))}
      <button
        className=" rounded-sm p-3 h-10 bg-purple-800 text-white flex justify-center items-center cursor-pointer"
        onClick={nextPageNum}
      >
        Next
      </button>
    </div>
 
  );
};

export default Pagination

