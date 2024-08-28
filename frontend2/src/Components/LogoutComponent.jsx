import { useDispatch } from 'react-redux';
import { logout } from '../Slices/userSlice';
import { useNavigate } from 'react-router-dom';

const LogoutButton = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = async () => {
    localStorage.setItem('access_token', null);
    dispatch(logout()); // Clear user from Redux state
    navigate('/')
  };



  return (
    <>

        <button onClick={handleLogout}>Logout</button>
   
    </>
  )
};

export default LogoutButton;
