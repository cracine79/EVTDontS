import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';
const LoginComponent = () => {
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('submitting')
    // const response = await csrfFetch('/api/questions/hello')
    // const output = await response.json()
    // console.log(output)
    try {
    const response = await csrfFetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      // Log the status and response text for debugging
      const errorText = await response.text();
      console.error('Error response status:', response.status);
      console.error('Error response body:', errorText);

      // Optionally, throw an error to handle it later in the catch block
      throw new Error(`Error ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    console.log(data)
    localStorage.setItem('access_token', data.access_token);
    dispatch(login(data)); // Store user in Redux state
  } catch (error) {
    // Log any errors that occur during fetch or processing
    console.error('Error during login:', error);
  }

  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginComponent;
