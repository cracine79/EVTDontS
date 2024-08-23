import { useDispatch } from 'react-redux';
import { logout } from '../Slices/userSlice';


const LogoutButton = () => {
  const dispatch = useDispatch();

  const handleLogout = async () => {
    localStorage.setItem('access_token', null);
    dispatch(logout()); // Clear user from Redux state
  };



  return (
    <>

        <button onClick={handleLogout}>Logout</button>
   
    </>
  )
};

export default LogoutButton;
