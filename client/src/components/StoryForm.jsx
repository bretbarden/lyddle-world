import React, {useState} from "react";
import { useNavigate } from 'react-router-dom'



const POST_HEADERS = {
    'Content-Type': 'application/json',
    'Accepts': 'application/json'
  }
  
const URL = "/api/v1"



function StoryForm (){

    const navigate = useNavigate()

    const [childName, setChildName] = useState("")
    const [childAge, setChildAge] = useState(0)
    const [childRace, setChildRace] = useState("")
    const [childHairStyle, setChildHairStyle] = useState("")
    const [childEyeColor, setChildEyeColor] = useState("")
    const [childOtherFeatures, setChildOtherFeatures] = useState("")
    const [childLocation, setChildLocation] = useState("")
    const [childClothing, setChildClothing] = useState("")
    const [childInterests, setChildInterests] = useState("")
    const [storySetting, setStorySetting] = useState("")

    // Leaving this here for now, but going with inline functions on form
    // const handleChangeChildName = e => setChildName(e.target.value)
    // const handleChangeChildAge = e => setChildAge(e.target.value)
    // const handleChangeChildRace = e => setChildRace(e.target.value)
    // const handleChangeChildHairStyle = e => setChildHairStyle(e.target.value)
    // const handleChangeChildEyeColor = e => setChildEyeColor(e.target.value)
    // const handleChangeChildOtherFeatures = e => setChildOtherFeatures(e.target.value)
    // const handleChangeChildLocation = e => setChildLocation(e.target.value)
    // const handleChangeChildClothing = e => setChildClothing(e.target.value)
    // const handleChangeChildInterests = e => setChildInterests(e.target.value)
    // const handleChangeStorySetting = e => setStorySetting(e.target.value)


    function handleSubmit(e){
        e.preventDefault()

        let newStoryInput = {childName, childAge, childRace, childHairStyle, childEyeColor, 
            childOtherFeatures, childLocation, childClothing, childInterests, storySetting}

        
        fetch(URL + '/stories', {
            method: "POST",
            headers: POST_HEADERS,
            body: JSON.stringify(newStoryInput)
        })
        .then( ()=> navigate('/storyreturn'))
        // TO UPDATE: Add error handling on the post here
        // Need to make sure that the backend has time to process, 
        // so may need a loading page here while it generates, 
        // or maybe a page saying that the story submission 
        // was a success
    }




 return (
    <div>
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                name="childName"
                value={childName}
                placeholder="e.g. Akeelah, Daphne, Jorge"
                onChange={(e) => setChildName(e.target.value)}/>
            <input
                type="integer"
                name="childAge"
                value={childAge}
                placeholder="0"
                onChange={(e) => setChildAge(e.target.value)}/>
            <input
                type="text"
                name="childRace"
                value={childRace}
                placeholder="Black, Asian, Hispanic or Latino, etc."
                onChange={(e) => setChildRace(e.target.value)}/>
            <input
                type="text"
                name="childHairStyle"
                value={childHairStyle}
                placeholder="e.g., wavy and down to shoulders, buzz cut"
                onChange={(e) => setChildHairStyle(e.target.value)}/>
            <input
                type="text"
                name="childEyeColor"
                value={childEyeColor}
                placeholder="e.g., brown, green, blue, hazel"
                onChange={(e) => setChildEyeColor(e.target.value)}/>
            <input
                type="text"
                name="childOtherFeatures"
                value={childOtherFeatures}
                placeholder="e.g., birthmark on right cheek, uses a wheelchair"
                onChange={(e) => setChildOtherFeatures(e.target.value)}/>
            <input
                type="text"
                name="childLocation"
                value={childLocation}
                placeholder="e.g., New York, Iowa, Salt Lake City"
                onChange={(e) => setChildLocation(e.target.value)}/>
            <input
                type="text"
                name="childClothing"
                value={childClothing}
                placeholder="e.g., dress, overalls, hat)"
                onChange={(e) => setChildClothing(e.target.value)}/>
            <input
                type="text"
                name="childInterests"
                value={childInterests}
                placeholder="e.g., dinosaurs, princesses, trains"
                onChange={(e) => setChildInterests(e.target.value)}/>
            <input
                type="text"
                name="storySetting"
                value={storySetting}
                placeholder="e.g., the mountains, space, the time of dinosaurs"
                onChange={(e) => setStorySetting(e.target.value)}/>

            <button type="submit">Create Story</button>
        </form>
    </div>
 )   
}

export default StoryForm;