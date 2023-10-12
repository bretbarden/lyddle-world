import React from "react";

function Header () {

return(
    <nav>
        <div>
            <Logo />
        </div>
        <div>
        <nav>
            <Link to="/">Home</Link>
            <Link to="/createstory">Create Your Story</Link>
            <Link to="/about">About Lyddle World</Link>
            <Link to="/contact">Contact</Link>
            <Link to="/login">Login or Create Account</Link>
        </nav>
            {/* Maybe change this to have a logo as the login link */}
        </div>
    </nav>
      )
}


export default Header;