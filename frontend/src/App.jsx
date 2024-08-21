
import {createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom'
import { Home } from "./features/home/home"
import { Login } from './features/login/login'
import { useDispatch } from 'react-redux'
import { useState, useEffect } from 'react'
import { restoreSession } from './features/session/sessionSlice'


const Layout = () => {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false)

  // useEffect(() => {
  //   dispatch(restoreSession()).then(() => {
  //     setIsLoaded(true)
  //   });
  // }, [dispatch]);

  return(
    <>
      <Outlet/>
    </>
  )
}

const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <Home />
      },
      {
        path: "/login",
        element: <Login />
      }
    ]
  }
])


function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchCsrfToken = async () => {
      const response = await csrfFetch('/api/csrf/restore'); // Endpoint to fetch the token
      const token = response.headers.get('X-CSRF-TOKEN');
      dispatch(setCsrfToken(token));
      sessionStorage.setItem('X-CSRF-TOKEN', token);
    };

    fetchCsrfToken();
  }, [dispatch]);
  
  return <RouterProvider router={router} />;
}

export default App;