import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginComponent from './Components/LoginComponent';
import SignupComponent from './Components/SignupComponent';
// import ProtectedRoute from './components/ProtectedRoute'; // Implement this for protected routes
import LogoutButton from './Components/LogoutComponent';
import { useEffect } from 'react';
import { restoreCSRF } from './csrf';
import './index.css'
import { AppRoot, ProtectedRoute } from './Components/routes';
import { createBrowserRouter, RouterProvider, Outlet, Navigate } from 'react-router-dom';
import { NavBar } from './Components/NavBar';
import { restoreUser } from './Slices/userActions';
import { useDispatch } from 'react-redux';
import { UserHome } from './Components/UserHome';
import { Footer } from './Components/Footer';
import { LegacyVideoRedirect } from './Components/routes';
import { Quiz } from './Components/Quiz';
import { QuizResults } from './Components/QuizResults';
import { GetStarted } from './Components/GetStarted';
import { ReviewQuizResults } from './Components/ReviewQuizResults';
import { QuizGenerator } from './Components/QuizGenerator';
import { UpdateUnits } from './Components/UpdateUnits';
import { FinishPage } from './Components/FinishPage';
import { FinishUnit } from './Components/FinishedUnit';
import { UnitQuizResults } from './Components/UnitQuizResults';
import { RetrieveData } from './Components/RetrieveData';
import { ResetPassword } from './Components/ResetPassword';
import { PrivacyPolicy } from './Components/PrivacyPolicy';
import { TermsOfService } from './Components/TermsOfService';
import { AboutUs } from './Components/AboutUs';
import { ContactUs } from './Components/ContactUs';
import { MessageSent } from './Components/MessageSent';
import { UserlessResults } from './Components/UserlessResults';
import { FreeQuiz } from './Components/FreeQuiz';
import { AuthGate } from './Components/AuthGate';

const Layout = () => {
  return(
    <div className="flex flex-col min-h-screen bg-[#344A53] text-white">
      <NavBar />
      <main className='flex flex-col flex-1'>
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}

const router = createBrowserRouter([
  // Login/signup pages used by the public (server-rendered) site; outside Layout on purpose
  { path: '/login', element: <AuthGate mode="login" /> },
  { path: '/signup', element: <AuthGate mode="signup" /> },
  {
    element: <Layout />,
    children:[
      {
        path:"/",
        element: <AppRoot />
      },
      {
        path:"/userhome",
        element: <ProtectedRoute component={UserHome} />
      },
      // The app's old video pages: everyone now uses the public (server-rendered) video pages
      {
        path:"/video/:chapterId",
        element: <LegacyVideoRedirect />
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
      {
        path:"/video-library/*",
        element: <LegacyVideoRedirect />
      },
      {
        path:"/freequiz/:chapterslug",
        element:<FreeQuiz />
      },
      {
        path:'/quizgenerator',
        element: <ProtectedRoute component={QuizGenerator} />
      },
      // Old error page: login/signup problems now show inside the login box
      {
        path: '/whoops',
        element: <Navigate to="/login" replace />
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
        element: <LegacyVideoRedirect />
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
], { basename: '/app' })

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

