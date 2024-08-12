import "./App.css"
// import { Counter } from "./features/counter/Counter"
// import { Quotes } from "./features/quotes/Quotes"
// import logo from "./logo.svg"
import {createBrowserRouter, Outlet, RouterProvider} from 'react-router-dom'
import { Home } from "./features/home/Home"
import { Login } from "./features/login/Login"
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

// const App = () => {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <Counter />
//         <p>
//           Edit <code>src/App.tsx</code> and save to reload.
//         </p>
//         <Quotes />
//         <span>
//           <span>Learn </span>
//           <a
//             className="App-link"
//             href="https://reactjs.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             React
//           </a>
//           <span>, </span>
//           <a
//             className="App-link"
//             href="https://redux.js.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Redux
//           </a>
//           <span>, </span>
//           <a
//             className="App-link"
//             href="https://redux-toolkit.js.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Redux Toolkit
//           </a>
//           <span>, </span>
//           <a
//             className="App-link"
//             href="https://react-redux.js.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             React Redux
//           </a>
//           ,<span> and </span>
//           <a
//             className="App-link"
//             href="https://reselect.js.org"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             Reselect
//           </a>
//         </span>
//       </header>
//     </div>
//   )
// }

function App() {
  return <RouterProvider router={router} />;
}

export default App;
