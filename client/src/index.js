import React from "react";
import App from "./components/App";
import "./index.css";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

import App from './components/App'
import MainPage from '/.components/MainPage'
import About from './components/About'
import StoryForm from './components/StoryForm'
import Login from './components/User/Login.jsx'
import Signup from './components/User/Signup.jsx'



//Loaders would go here//

const router = createBrowserRouter([
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                index: true,
                element: <MainPage />
            },
            {
                path: "about",
                element: <About />
            },
            {
                path: "createstory",
                element: <StoryForm />
            },
            {
                path: "contact",
                element: <Contact />
            },
            {
                path: "storyreturn",
                element: <StoryReturn />
            },
        ]
    }
])


const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);





