import { useDispatch } from 'react-redux';
import { logout } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';

const LogoutButton = () => {
  const dispatch = useDispatch();

  const handleLogout = async () => {
    await csrfFetch('/api/auth/logout', {
      method: 'POST',
    });

    dispatch(logout()); // Clear user from Redux state
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;
