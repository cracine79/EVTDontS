import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginComponent from './Components/LoginComponent';
import SignupComponent from './Components/SignupComponent';
// import ProtectedRoute from './components/ProtectedRoute'; // Implement this for protected routes
import LogoutButton from './Components/LogoutComponent';
import { useEffect } from 'react';
import { restoreCSRF } from './csrf';
import './index.css'
import { AuthRoute, ProtectedRoute } from './Components/routes';
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
import { FinishPage } from './Components/FinishPage';
import { FinishUnit } from './Components/FinishedUnit';
import { UnitQuizResults } from './Components/UnitQuizResults';
import { RetrieveData } from './Components/RetrieveData';
import { ResetPassword } from './Components/ResetPassword';

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
        element: <AuthRoute component={MainPage} />
      },
      {
        path:"/userhome",
        element: <ProtectedRoute component={UserHome} />
      },
      {
        path:"/video/:chapterId",
        element: <Video />
      }, 
      {
        path:"/quiz",
        element: <ProtectedRoute component={Quiz} />
      },
      {
        path:"/results",
        element: <ProtectedRoute component={QuizResults} />
      },
      {
        path:'/rqresults',
        element: <ProtectedRoute component={ReviewQuizResults} />
      },
      {
        path:"/getstarted",
        element: <ProtectedRoute component={GetStarted} />
      },
      {
        path:'/videoindex',
        element: <VideoIndex />
      },
      {
        path:'/quizgenerator',
        element: <ProtectedRoute component={QuizGenerator} />
      },
      {
        path: '/whoops',
        element: <Whoops />
      }, 
      {
        path: '/updateunits',
        element: <ProtectedRoute component={UpdateUnits} />
      },
      {
        path: '/finishpage',
        element: <ProtectedRoute component={FinishPage} />
      },
      {
        path:'/finishunit',
        element: <ProtectedRoute component={FinishUnit} />
      },
      {
        path:'/uqresults',
        element: <ProtectedRoute component={UnitQuizResults} />
      },
      {
        path:'/retrievedata',
        element: <RetrieveData />
      },
      {
        path:'/reset-password',
        element: <ResetPassword />
      }
    ]
  }
])

function App() {
  const dispatch = useDispatch();

  console.log('Hellow WOrldio')

  useEffect(() => {
    console.log('UseEffecting . . .')
    restoreCSRF();
    dispatch(restoreUser());
  }, []);

  return (
    <RouterProvider router={router} />
  );
}

export default App;

