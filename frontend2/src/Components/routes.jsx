import { useEffect } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

// A real saved login token (logout used to store the string "null")
export const hasStoredToken = () => {
  const token = localStorage.getItem('access_token');
  return !!token && token !== 'null' && token !== 'undefined';
};

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
  const authChecked = useSelector(state => state.user.authChecked);

  if (loggedIn) return <Component {...props} />;
  // Still checking a saved login (e.g. after a page refresh): wait instead of bouncing the student out
  if (!authChecked && hasStoredToken()) return null;
  return <Navigate to="/" replace={true} />;
};

/**
 * /app/ has no homepage of its own: logged-in students go to their dashboard,
 * everyone else to the public homepage. Old /app/?login=1 and ?signup=1 links still work.
 */
export const AppRoot = () => {
  const loggedIn = useSelector(state => !!state.user.username);
  const authChecked = useSelector(state => state.user.authChecked);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.has('login')) { navigate('/login', { replace: true }); return; }
    if (params.has('signup')) { navigate('/signup', { replace: true }); return; }
    if (loggedIn) { navigate('/userhome', { replace: true }); return; }
    if (authChecked || !hasStoredToken()) window.location.replace('/');
  }, [loggedIn, authChecked, location.search, navigate]);

  return null;
};

// "HTTP error! Status: 400 - Someone is already using..." -> "Someone is already using..."
export const friendlyAuthError = (message, fallback) => {
  const m = /Status:\s*(\d+)\s*-\s*(.+)$/.exec(message || '');
  if (!m) return fallback;
  if (m[1] === '401') return 'Invalid username or password. Please try again.';
  const text = m[2].trim();
  return text && !/^(Unknown error|INTERNAL SERVER ERROR)$/i.test(text) ? text : fallback;
};

// Full page load to the public (server-rendered) homepage
export const goToPublicHome = () => window.location.assign('/');

/**
 * Old in-app video URLs (/app/video/6, /app/video-library/<slug>, /app/searchresults).
 * A full page load lets the server redirect to the matching public video page.
 */
export const LegacyVideoRedirect = () => {
  const location = useLocation();
  useEffect(() => {
    window.location.replace('/app' + location.pathname + location.search);
  }, [location.pathname, location.search]);
  return null;
};
