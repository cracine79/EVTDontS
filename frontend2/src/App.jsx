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
import { Quiz } from './Components/Quiz';
import { QuizResults } from './Components/QuizResults';
import { GetStarted } from './Components/GetStarted';
import { ReviewQuizResults } from './Components/ReviewQuizResults';
import { VideoIndex } from './Components/VideoIndex';
import { QuizGenerator } from './Components/QuizGenerator';
import { Whoops } from './Components/Whoops';
import { UpdateUnits } from './Components/UpdateUnits';


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
        path:"/video/:chapterId",
        element: <Video />
      }, 
      {
        path:"/quiz",
        element: <Quiz />
      },
      {
        path:"/results",
        element: <QuizResults />
      },
      {
        path:'/rqresults',
        element: <ReviewQuizResults />
      },
      {
        path:"/getstarted",
        element: <GetStarted />
      },
      {
        path:'/videoindex',
        element: <VideoIndex />
      },
      {
        path:'/quizgenerator',
        element: <QuizGenerator />
      },
      {
        path: '/whoops',
        element: <Whoops />
      }, 
      {
        path: '/updateunits',
        element: <UpdateUnits />
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

