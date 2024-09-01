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
import { UserHome } from './Components/UserHome';
import { Footer } from './Components/Footer';
import { Video } from './Components/Video';


const Layout = () => {
  return(
    <div className="flex flex-col">
      <NavBar />
      <div className='flex flex-col -mt-24'>
        <Outlet />
      </div>
      <Footer />
    </div>
  )
}

const router = createBrowserRouter([
  {
    element: <Layout />,
    children:[
      {
        path:"/",
        element: <MainPage />
      },
      {
        path:"/userhome",
        element: <UserHome />
      },
      {
        path:"/video",
        element: <Video />
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
  );
}

export default App;

