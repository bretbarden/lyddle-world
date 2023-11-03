import { useState } from 'react'

function Login({attemptLogin}) {

  // STATE //

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // EVENTS //

  const handleChangeEmail = e => setEmail(e.target.value)
  const handleChangePassword = e => setPassword(e.target.value)

  function handleSubmit(e) {
    e.preventDefault()
    attemptLogin({email, password})
  }

  // RENDER //

  return (
    <form className='user-form' onSubmit={handleSubmit} >

      <h2>Login</h2>

      <input type="text"
      onChange={handleChangeEmail}
      value={email}
      placeholder='email address'
      />

      <input type="text"
      onChange={handleChangePassword}
      value={password}
      placeholder='password'
      />

      <input type="submit"
      value='Login'
      />

    </form>
  )

}

export default Login
