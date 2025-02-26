import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

export const AuthRoute = ({ component: Component, ...props }) => {
  const loggedIn = useSelector(state => !!state.user.username);

  return (
    !loggedIn ?
      <Component {...props} /> :
      <Navigate to="/userhome" replace={true} />
  );
};

export const ProtectedRoute = ({ component: Component, ...props }) => {
  const loggedIn = useSelector(state => !!state.user.username);

  return (
    loggedIn ? 
      <Component {...props} /> :
      <Navigate to="/" replace={true} />
  );
};