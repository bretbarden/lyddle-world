import React from "react";
import "./index.css";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

import App from './components/App'
import MainPage from './components/MainPage'
import About from './components/About'
import StoryForm from './components/StoryForm'
import Login from './components/UserPanel/Login.jsx'
import Signup from './components/UserPanel/Signup.jsx'
import Contact from "./components/Contact";
import StoryReturn from "./components/StoryReturn";
import ErrorPage from "./components/ErrorPage";


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
            {
                path: "signup",
                element: <Signup />
            },
            {
                path: "login",
                element: <Login />
            }
        ]
    }
])

// Below approach does not use router
// const container = document.getElementById("root");
// const root = createRoot(container);
// root.render(<App />);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render( <RouterProvider router={router} /> );







