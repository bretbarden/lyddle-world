import React from "react";
import {Link} from 'react-router-dom'


function Header () {

return(
    <nav>
        <Link to="/">Home</Link>
        <Link to="/createstory">Create</Link>
        <Link to="/storyreturn">View</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
        <Link to="/login">Login</Link>
    </nav>
    )
}


export default Header;