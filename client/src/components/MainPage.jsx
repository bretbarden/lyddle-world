import React from "react";
// import StoryForm from "./StoryForm";
import {Link} from 'react-router-dom'

function MainPage () {


    return(
        <div>
            <h4>Welcome to Lyddle World! Please log in or sign up, and then click the link below to create your Lyddle One's story.</h4>
            <Link to="/createstory">Create Your Story Now!</Link>

            {/* <UserDetails
                currentUser={currentUser}
                attemptLogin={attemptLogin}
                attemptSignup={attemptSignup}
                logout={logout} /> */}
        </div>
    )
}

export default MainPage