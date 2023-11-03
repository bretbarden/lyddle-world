import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import lyddleImage from '../assets/Lyddle.png';

const POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

const URL = "/api/v1";

function StoryForm() {

    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);

    const [childName, setChildName] = useState("");
    const [childAge, setChildAge] = useState(0);
    const [childRace, setChildRace] = useState("");
    const [childPronouns, setChildPronouns] = useState("");
    const [childHairStyle, setChildHairStyle] = useState("");
    const [childLocation, setChildLocation] = useState("");
    const [childClothing, setChildClothing] = useState("");
    const [childInterests, setChildInterests] = useState("");
    const [storySetting, setStorySetting] = useState("");

    function handleSubmit(e) {
        e.preventDefault();
        setIsLoading(true);

        let newStoryInput = { childName, childAge, childPronouns, childRace, childHairStyle, childLocation, childClothing, childInterests, storySetting };

        fetch(URL + '/createstory', {
            method: "POST",
            headers: POST_HEADERS,
            body: JSON.stringify(newStoryInput)
        })
            .then(() => {
                setIsLoading(false);
                navigate('/storyreturn');
            })
            // Add error handling here, and make sure to set isLoading to false in case of an error
    }

    if (isLoading) {
        return <StoryLoading />;
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
            <label htmlFor="childName">Name</label>
            <input
                type="text"
                name="childName"
                value={childName}
                placeholder="Akeelah, Jorge..."
                onChange={(e) => setChildName(e.target.value)}/>
            <br></br>
            <label htmlFor="childAge">Age</label>
            <input
                type="text"
                name="childAge"
                value={childAge}
                placeholder="5, 7"
                onChange={(e) => setChildAge(e.target.value)}/>
            <br></br>
            <label htmlFor="childPronouns">Pronouns</label>
            <input
                type="text"
                name="childPronouns"
                value={childPronouns}
                placeholder="she, they, he..."
                onChange={(e) => setChildPronouns(e.target.value)}/>
            <br></br>
            <label htmlFor="childRace">Race</label>
            <input
                type="text"
                name="childRace"
                value={childRace}
                placeholder="Black, Asian, Hispanic/Latino..."
                onChange={(e) => setChildRace(e.target.value)}/>
            <br></br>
            <label htmlFor="childHairStyle">Hair Style</label>
            <input
                type="text"
                name="childHairStyle"
                value={childHairStyle}
                placeholder="wavy long black hair..."
                onChange={(e) => setChildHairStyle(e.target.value)}/>
           <br></br>
           {/* <label htmlFor="childEyeColor">Eye Color</label>
           <input
                type="text"
                name="childEyeColor"
                value={childEyeColor}
                placeholder="e.g., brown, green, blue, hazel"
                onChange={(e) => setChildEyeColor(e.target.value)}/>
            <br></br> */}
            {/* <label htmlFor="childOtherFeatures">Other features?</label>
            <input
                type="text"
                name="childOtherFeatures"
                value={childOtherFeatures}
                placeholder="e.g., birthmark on right cheek, uses a wheelchair"
                onChange={(e) => setChildOtherFeatures(e.target.value)}/>
            <br></br> */}
            <label htmlFor="childLocation">Where does your child live?</label>
            <input
                type="text"
                name="childLocation"
                value={childLocation}
                placeholder="Queens, Indonesia..."
                onChange={(e) => setChildLocation(e.target.value)}/>
            <br></br>
            <label htmlFor="childClothing">What clothing should your child wear?</label>
            <input
                type="text"
                name="childClothing"
                value={childClothing}
                placeholder="green dress, blue overalls...)"
                onChange={(e) => setChildClothing(e.target.value)}/>
            <br></br>
            <label htmlFor="childInterests">Please list some of your child's interests</label>
            <input
                type="text"
                name="childInterests"
                value={childInterests}
                placeholder="dinosaurs, trains..."
                onChange={(e) => setChildInterests(e.target.value)}/>
            <br></br>
            <label htmlFor="storySetting">Where should the story take place?</label>
            <input
                type="text"
                name="storySetting"
                value={storySetting}
                placeholder="a park, the mountains, space..."
                onChange={(e) => setStorySetting(e.target.value)}/>
            <br></br>

            <button type="submit">Create Story</button>
        </form>
        </div>
    );
}

function StoryLoading() {
    return (
        <div>
            <h2> 🌈 Writing your story! </h2>
            <h3> 🖋️ Crafting perfect prose... </h3>
            <h3> 🎨 Illustrating magical memories... </h3>
            <img src={lyddleImage} alt="Lydia"  style={{ width: '30%', height: 'auto' }}/>
        </div>
    );
}

export default StoryForm;