import React, { useState, useEffect } from 'react';
import lyddleImage from '../assets/Lyddle.png';
import { Link, useNavigate } from 'react-router-dom';

const URL = "/api/v1";

function StoryReturn() {
    const [data, setData] = useState(null);
    const [currentPage, setCurrentPage] = useState(0);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await fetch(URL + '/getlaststory');
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        fetchData();
    }, []);

    if (!data) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                Loading...<br />
                <img src={lyddleImage} alt="Lydia" style={{ width: '30%', height: 'auto' }} />
            </div>
        );
    }

    if (!data.pages || data.pages.length === 0) {
        return <div>No story data available.</div>;
    }

    console.log('Received data:', data);

    const handleNext = () => {
        setCurrentPage((prevPage) => Math.min(prevPage + 1, data.pages.length - 1));
    };

    const handlePrev = () => {
        setCurrentPage((prevPage) => Math.max(prevPage - 1, 0));
    };

    return (
        <div>
            <h1>{data.title_text}</h1>
            <button onClick={handlePrev} disabled={currentPage === 0}>Previous Page</button>
            <button onClick={handleNext} disabled={currentPage === data.pages.length - 1}>Next Page</button>
            <div>
                <p>{data.pages[currentPage].text}</p>
                <img src={data.pages[currentPage].imageurl} alt="Story image" style={{ width: '100%', height: 'auto' }}/>
            </div>
        </div>
    );
}

export default StoryReturn;