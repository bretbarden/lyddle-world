import React, { useState, useEffect } from 'react';
import lyddleImage from '../assets/Lyddle.png';


const URL = "/api/v1";

function StoryReturn() {
    const [data, setData] = useState(null);
    const [currentPage, setCurrentPage] = useState(0);

    useEffect(() => {
        async function fetchData() {
            const response = await fetch(URL + `/getlaststory`);
            const result = await response.json();
            setData(result);
        }

        fetchData();
    }, []);

    if (!data) {
        return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>Loading...<br></br><img src={lyddleImage} alt="Lydia"  style={{ width: '30%', height: 'auto' }}/></div>;
    }

    const handleNext = () => {
        setCurrentPage((prevPage) => Math.min(prevPage + 1, 5));
    };

    const handlePrev = () => {
        setCurrentPage((prevPage) => Math.max(prevPage - 1, 0));
    };

    return (
        <div>
            <h1>{data.title_text}</h1>
            <div>
                <p>{data.pages[currentPage].text}</p>
                <img src={data.pages[currentPage].imageurl} alt="Story image" />
            </div>
            <button onClick={handlePrev} disabled={currentPage === 0}>Previous</button>
            <button onClick={handleNext} disabled={currentPage === 5}>Next</button>
        </div>
    );
}

export default StoryReturn;