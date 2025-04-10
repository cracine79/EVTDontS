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
import { PrivacyPolicy } from './Components/PrivacyPolicy';
import { TermsOfService } from './Components/TermsOfService';
import { AboutUs } from './Components/AboutUs';
import { SearchResults } from './Components/SearchResults';
import { ContactUs } from './Components/ContactUs';
import { MessageSent } from './Components/MessageSent';
import { UserlessResults } from './Components/UserlessResults';
import { VideoIndexVideo } from './Components/VideoIndexVideo';
import { VideoIndexHome } from './Components/VideoIndexHome';
import { FreeQuiz } from './Components/FreeQuiz';

const Layout = () => {
  return(
    <div className="flex flex-col">
      <NavBar />
      <div className='flex flex-col'>
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
        element: <Quiz />
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
      // {
      //   path:'/video-library',
      //   element: <VideoIndex />,
      // },
      {
        path:"/video-library",
        element:<VideoIndex />,
        children: [
          {
            index:true, 
            element: <VideoIndexHome />
          },
          {
            path: ":slug",
            element: <VideoIndexVideo />
          }
        ]
      },
      {
        path:"/freequiz/:chapterslug",
        element:<FreeQuiz />
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
        path:'/userlessresults',
        element:<UserlessResults />
      },
      {
        path:'/retrievedata',
        element: <RetrieveData />
      },
      {
        path:'/reset-password',
        element: <ResetPassword />
      },
      {
        path:'/privacypolicy',
        element: <PrivacyPolicy />
      },
      {
        path:'/termsofservice',
        element: <TermsOfService />
      },
      {
        path:'/aboutus',
        element: <AboutUs />
      },
      {
        path: '/searchresults',
        element: <SearchResults />
      },
      {
        path:'/contactus',
        element: <ContactUs/>
      },
      {
        path:'/messagesent',
        element: <MessageSent />
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

