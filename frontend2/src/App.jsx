
import {createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom'
import { Home } from "./features/home/home"
import { Login } from './features/login/login'

const Layout = () => {
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
  return <RouterProvider router={router} />;
}

export default App;