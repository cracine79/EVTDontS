import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginComponent from './Components/LoginComponent';
import SignupComponent from './Components/SignupComponent';
// import ProtectedRoute from './components/ProtectedRoute'; // Implement this for protected routes
import LogoutButton from './Components/LogoutComponent';
import { useEffect } from 'react';
import { restoreCSRF } from './csrf';
import './index.css'

function App() {

  useEffect(() => {
    restoreCSRF();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginComponent />} />
        <Route path="/signup" element={<SignupComponent />} />
        {/* <Route
          path="/protected"
          element={<ProtectedRoute><ProtectedPage /></ProtectedRoute>}
        /> */}
      </Routes>
      <LogoutButton />
    </Router>
  );
}

export default App;

