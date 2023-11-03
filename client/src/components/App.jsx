import React, { useEffect, useState } from "react";
// import { Switch, Route } from "react-router-dom";
import Header from "./Header";
// import MainPage from "./MainPage";
import UserDetails from "./UserPanel";
// import Login from "./UserPanel/Login";
// import Signup from "./UserPanel/Signup"
import { Outlet } from 'react-router-dom'
// import Stories from './Stories'
// Note: Some components above turned off since currently not used


const POST_HEADERS = {
  "Content-Type": "application/json", 
  "Accept": "application/json"
}

// Create a const of URL for ease of reference
const URL = "/api/v1"


function App() {

  const [currentUser, setCurrentUser] = useState(null)

  // Fetch request
  useEffect(() => {
    fetch( URL + '/check_session' )
    .then(response => {
      if (response.ok) {
        response.json()
        .then (data => setCurrentUser(data))
      }
    })
  },[])



  // Signup, Login, and Log out
  // async function attemptSignup(userInfo) {
  //   try {
  //     const response = await fetch(URL + "/users", {
  //       method: "POST", 
  //       headers: POST_HEADERS,
  //       body: JSON.stringify(userInfo)    
  //     })
  //     if (response.ok) {
  //       const data = await response.json()
  //       setCurrentUser(data)
  //     } else {
  //       alert('Signup not sucessful')
  //     }
  //   } catch (error) {
  //     alert (error)
  //   }
  // }

  async function attemptSignup(userInfo) {
    const response = await fetch(URL + '/users', {
      method: 'POST',
      headers: POST_HEADERS,
      body: JSON.stringify(userInfo)
    })
    if (response.ok) {
      const data = await response.json()
      setCurrentUser(data)
    } else {
      alert('Invalid sign up')
    }
  }
 

  async function attemptLogin(userInfo) {
    try {
      const response = await fetch (URL + "/login", {
        method: "POST",
        headers: POST_HEADERS,
        body: JSON.stringify(userInfo)
      })
      if (response.ok) {
        const data = await response.json()
        setCurrentUser(data)
      } else {
        alert('Login not sucessful')
      }
    } catch (error) {
      alert (error) 
    }
  }

  //Non-Cookie version of logout
  // function logout() {
  //   setCurrentUser(null)
  // }

  // If using cookies, make logout delete cookies from the site based on the URL
  function logout() {
    setCurrentUser(null)
    fetch(URL + '/logout', {
      method: 'DELETE'
    })
  }



  return (
    <div className="App">
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
        <h1> ✨📚 Lyddle World 📚✨</h1>
      </div>
      <div>
        <Header />
        <Outlet />
        {/* TO UPDATE: REPLACE BELOW WITH SEPARATE SIGNUP AND LOGIN */}
        <UserDetails
        currentUser={currentUser}
        attemptLogin={attemptLogin}
        attemptSignup={attemptSignup}
        logout={logout} />
      </div>
    </div>
  )
}

export default App;
