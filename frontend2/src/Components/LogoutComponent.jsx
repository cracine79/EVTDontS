import { useDispatch } from 'react-redux';
import { logout } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';

const LogoutButton = () => {
  const dispatch = useDispatch();

  const handleLogout = async () => {
    // await csrfFetch('/api/auth/logout', {
    //   method: 'POST',
    // });
    localStorage.setItem('access_token', null);
    dispatch(logout()); // Clear user from Redux state
  };

  const test = async () => {
    const res = await csrfFetch('/api/questions/hello')
    const better=await res.json()
    console.log(better)
  }

  return (
    <>
      {/* "Logout Button" */}
        <button onClick={handleLogout}>Logout</button>
        {/* <button onClick={test}>Test</button> */}
    </>
  )
};

export default LogoutButton;
