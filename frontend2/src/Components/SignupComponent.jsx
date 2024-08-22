import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { login } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';

const SignupComponent = () => {
  const dispatch = useDispatch();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault();
    debugger;
    const response = await csrfFetch('/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await response.json();
    localStorage.setItem('access_token', data.user.access_token);
    dispatch(login(data.user)); // Store user in Redux state
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
         <input
        type="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <button type="submit">Sign Up</button>
    </form>
  );
};

export default SignupComponent;
