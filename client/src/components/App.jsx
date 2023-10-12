import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Header from "./Header";

const POST_HEADERS = {
  "Content-Type": "application/json", 
  "Accept": "application/json"
}

// Create a const of URL for ease of reference
const URL = "http://localhost:5555/api/v1"


function App() {

  const [currentUser, setCurrentUser] = useState(null)

  // Fetch request
  useEffect(() => {
    fetch( URL + '/check_session' )
    .then (response => {
      if (response.ok) {
        response.json()
        .then ( data => setCurrentUser(data) )
      }
    })
  }, [])



  // Signup, Login, and Log out
  async function attemptSignup(userInfo) {
    try {
      const response = await fetch(URL + "/users", {
        method: "POST", 
        headers: POST_HEADERS,
        body: JSON.stringify(userInfo)    
      })
      if (response.ok) {
        const data = await response.json()
        setCurrentUser(data)
      } else {
        alert('Signup not sucessful')
      }
    } catch (error) {
      alert (error)
    }
  }
 

  async function attemptLogin(userInfo) {
    try {
      const response = await fetch (URL + "/login", {
        method: "POST",
        headers: POST_HEADERS,
        body: json.stringify(userInfo)
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

  function logout() {
    setCurrentUser(null)
  }

  // If using cookies, make logout delete cookies from the site based on the URL
  function logout() {
    setCurrentUser(null)
    fetch(URL + '/logout', {
      method: 'DELETE'
    })
  }



  return (
    <div className="App">
      <h1> Login or Signup  </h1>
        <Header />
        <Home />
        <Login />
        

      <UserPanel
      currentUser={currentUser}
      attemptLogin={attemptLogin}
      attemptSignup={attemptSignup}
      logout={logout} />

      <Notes />

    </div>
  )
}

export default App;
