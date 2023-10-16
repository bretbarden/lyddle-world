import React from "react";
import StoryForm from "./StoryForm";
import {Link} from 'react-router-dom'

function MainPage () {


    return(
        <div>
            <p> Placeholder for image </p>
            <Link to="/createstory">Create Your Story Now!</Link>
        </div>
    )
}

export default MainPage