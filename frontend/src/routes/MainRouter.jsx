import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "../components/layout/Layout";
import LoginPage from "../components/pages/LoginPage";
import SignUpPage from "../components/pages/SignUpPage";
import ProfilePage from "../components/pages/ProfilePage";
import Home from "../components/pages/Home";
import Availability from "../components/pages/Availability";




const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home/>,
      },
      {
        path: "/signup",
        element: <SignUpPage />,
      },

      {
        path: "/login",
        element: <LoginPage />,
      },

      {
        path: "/profile",
        element: <ProfilePage />,
      },
      {
        path :"/availability",
        element :<Availability/>
      }

    ],
  },
]);

const MainRouter = () => {
  return <RouterProvider router={router} />;
};

export default MainRouter;
