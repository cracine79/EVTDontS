
import {createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom'
import { Home } from "./features/home/home"
import { Login } from './features/login/login'
import { useDispatch } from 'react-redux'
import { useState, useEffect } from 'react'
import { restoreSession } from './features/session/sessionSlice'


const Layout = () => {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    dispatch(restoreSession()).then(() => {
      setIsLoaded(true)
    });
  }, [dispatch]);

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
        path: "/goodbye",
        element: <Home />
      },
      {
        path: "/hello",
        element: <Login />
      }
    ]
  }
])


function App() {
  return <RouterProvider router={router} />;
}

export default App;