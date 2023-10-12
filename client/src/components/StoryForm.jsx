import React, {useState} from "react";



function StoryForm (){


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


    function handleSubmit(e){
        e.preventDefault()

        let newStoryInput = {
            
        }

    }

 return (
    <Form>


    </Form>
 )   
}

export default StoryForm;