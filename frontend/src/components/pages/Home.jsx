import axios from "axios";
import React, { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import toast, { Toaster } from "react-hot-toast";
import HomeCard from "./HomeCard";
import Pagination from "./Pagination";



const Home = () => {
  let [hotelData, setHotelData] = useState([]);


 
  const onChangeSearchValue = async (data) => {
    const searchInput = {
      ...data,
      city_name: data.city_name.trim().toLowerCase(),
    };

    console.log(searchInput.city_name);
    try {
      let response = await axios.post(
        `http://127.0.0.1:8000/web-scraping-playwright?city_name=${searchInput.city_name}`
      );
      if (response.data) {
        console.log("response data", response.data.message);
      }
    } catch (error) {
      if (error.response) {
        const msg = error.response.data?.message || "failed to search";
        toast.error(msg);
        console.log("backend error message", msg);
      } else if (error.request) {
        toast.error("no response from server");
        console.log("no response received", error.request);
      } else {
        toast.error("error");
        console.log("error message:", error.message);
      }
    }
  };
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({ mode: "onChange" });

  useEffect(() => {
    hotelDetails();
  }, []);

  const hotelDetails = async () => {
    let page = 1
    try {
      let response = await axios.get( `http://127.0.0.1:8000/get-hotel-details?page=${page}`);
      let response_data = response.data.message.hotel;
      setHotelData(response_data);
    } catch (error) {
      if (error.response) {
        const msg = error.response.data?.message || "failed to get data";
        toast.error(msg);
        console.log("backend error message", msg);
      } else if (error.request) {
        toast.error("no response from server");
        console.log("no response received", error.request);
      } else {
        toast.error("error");
        console.log("error message:", error.message);
      }
    }
  };

  return (
    <div className="bg-gray-100 h-full ">
      <form onSubmit={handleSubmit(onChangeSearchValue)}>
        <Toaster />
        <div className=" p-5 ">
          <p className="  mb-6 text-gray-700 leading-relaxed">
            {" "}
            This website automatically collects and organizes data from external
            sources in real time. Whether you're tracking hotel prices,
            availability, or other details, the scraper efficiently gathers the
            information for your selected dates or criteria. There's no need for
            manual input — the system fetches and structures the data behind the
            scenes, making it easily accessible for viewing, analysis, or
            integration with other applications.
          </p>
          <div className=" h-90 p-5 w-full flex flex-col justify-center items-center">
            <div className=" w-300 h-50 p-30 flex flex-row justify-center items-center">
              <input
                {...register("city_name")}
                className="rounded-md text-center w-150 h-15 border-2 p-5 mb-50"
                type="text"
                placeholder="Enter City Name to Scrap"
              />
              <br />
              <input
                type="submit"
                disabled={isSubmitting}
                value={isSubmitting ? "Searching..." : "Search"}
                className="m-5 p-2 rounded-md w-20 bg-purple-800 text-white  my-2 cursor-pointer mb-51"
              />
            </div>
          </div>
        </div>
      </form>
      <div className="h-full border-2 ">
      <div
        className=" bg-gray-100 border-2 h-screen grid grid-cols-1 gap-4 w-full place-items-center z-0 
          overflow-x-auto
          "
      >
        {hotelData?.map(
          (
            { id, hotel_name, city_name, img_link, price, availability },
            index
          ) => {
     
            const firstRoom = availability?.[0]?.roomtype?.[0];
            const roomtype_bed = firstRoom?.roomtype_bed;
            const roomtype = firstRoom?.roomtype;
            return (
              <div key={index}>
                <HomeCard
                  id={id}
                  hotel_name={hotel_name}
                  city_name={city_name}
                  img_link={img_link[0]}
                  price={price}
                  availability={availability}
                  roomtype_bed={roomtype_bed}
                  roomtype={roomtype}
                />
                 
              </div>
            );
          }
        )}
       </div>
       <div className="h-screen border-2 flex flex-row justify-center ">
        <Pagination />
</div>
      </div>
     
     
    </div>
  );
};

export default Home;
