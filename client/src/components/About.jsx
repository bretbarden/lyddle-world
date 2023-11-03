import React from "react";
import lyddleSmiles from '../assets/LyddleSmiles.png';

function About (){

    return(
        <div>
            <p>An early love of reading is one of the most important lessons you can instill in your child. But these days, it's harder than ever to keep kids engaged. We're competing with ever-present streaming services, video games, social media - you name it.</p>
            <p>At Lyddle World, we use Artificial Intelligence (AI) to make reading dynamic, exciting, and fun for your child. With our app, you can make endless stories, customized specifcally for your Lyddle One, so that they never get bored and stay engaged with stories specifically about them and their own Lyddle World. </p>
            <p>This app is dedicated to my favorite Lyddle One: my daughter, Lydia, who inspires me every day to create and build a build a better Lyddle World for her.</p>
            <img src={lyddleSmiles} alt="Lydia smiling wearing hanbok"  style={{ display: 'block', margin: '0 auto', width: '30%', height: 'auto' }}/>
        </div>
    )
}

export default About