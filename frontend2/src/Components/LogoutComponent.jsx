import { useDispatch } from 'react-redux';
import { logout } from '../Slices/userSlice';
import { useNavigate } from 'react-router-dom';
import { clearUserUnits } from '../Slices/unitsSlice';
import { clearQuestions } from '../Slices/questionsSlice';
import { clearUserChapters } from '../Slices/userChaptersSlice';
import { clearUserResults } from '../Slices/resultsSlice';
import { clearTopicProg } from '../Slices/topicProgSlice';
import { clearTopics } from '../Slices/topicsSlice';
const LogoutButton = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleLogout = async () => {
    localStorage.setItem('access_token', null);
    dispatch(logout()); // Clear user from Redux state
    dispatch(clearUserUnits())
    dispatch(clearQuestions())
    dispatch(clearUserChapters())
    dispatch(clearUserResults())
    dispatch(clearTopicProg())
    dispatch(clearTopics())
    
    navigate('/')
  };



  return (
    <>

        <button onClick={handleLogout}>Logout</button>
   
    </>
  )
};

export default LogoutButton;
