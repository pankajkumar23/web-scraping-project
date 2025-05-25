import React from "react";
import { Outlet } from "react-router-dom";
import Home from "../pages/Navbar";
import Navbar from "../pages/Navbar";

const Layout = () => {
  return (
    <div>
      <Navbar />
      <Outlet />
    </div>
  );
};

export default Layout;
