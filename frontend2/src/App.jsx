import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginComponent from './Components/LoginComponent';
import SignupComponent from './Components/SignupComponent';
// import ProtectedRoute from './components/ProtectedRoute'; // Implement this for protected routes
import LogoutButton from './Components/LogoutComponent';
import { useEffect } from 'react';
import { restoreCSRF } from './csrf';
import './index.css'
import { AuthRoute } from './Components/routes';
import { createBrowserRouter, RouterProvider, Outlet } from 'react-router-dom';
import { NavBar } from './Components/NavBar';
import { MainPage } from './Components/MainPage';
import { restoreUser } from './Slices/userActions';
import { useDispatch } from 'react-redux';



const Layout = () => {
  return(
    <>
      <NavBar />
      <Outlet />
    </>
  )
}

const router = createBrowserRouter([
  {
    element: <Layout />,
    children:[
      {
        path:"/",
        element: <MainPage />
      }
    ]
  }
])

function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    restoreCSRF();
    dispatch(restoreUser());
  }, []);

  return (
    <RouterProvider router={router} />
    // <Router>
    //   <Routes>
    //     <Route path="/login" element={<LoginComponent />} />
    //     <Route path="/signup" element={<SignupComponent />} />
    //     {/* <Route
    //       path="/protected"
    //       element={<ProtectedRoute><ProtectedPage /></ProtectedRoute>}
    //     /> */}
    //   </Routes>
    //   <LogoutButton />
    // </Router>
  );
}

export default App;

