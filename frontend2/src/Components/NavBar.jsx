import { useSelector, useDispatch } from "react-redux"
import LoginComponent from "./LoginComponent"
import SignupComponent from "./SignupComponent"
import LogoutButton from "./LogoutComponent"
import { openLoginModal, openSignupModal } from "../Slices/modalSlice"
import { UserMenu } from "./UserMenu"
import { useNavigate } from "react-router-dom"
import { getAllChapters } from "../Slices/chaptersActions"
import { SearchBar } from "./SearchBar"
import { useState } from "react"


export const NavBar = () => {
    const navigate = useNavigate()
    let loginFormOpen = useSelector(state=>(state.modal.isLoginOpen))
    let signupFormOpen = useSelector(state=>(state.modal.isSignupOpen))
    const currentUser = useSelector(state=>(state.user.username))
    const [mobileSearchBarVisible, setMobileSearchBarVisible] = useState(false)
    const dispatch = useDispatch()
   
    const handleLogin = ()=>{
        dispatch(openLoginModal())
    }

    const handleSignup = () => {
        dispatch(openSignupModal())
    }

    const sessionLinks = currentUser ? (
        <div className="mr-8">
            <UserMenu/>
            {/* <LogoutButton/> */}
        </div>
    ) : (
        <div className="flex w-32 justify-between mr-4 sm:mr-10 text-xs md:text-sm">
            <p className="hover:cursor-pointer" onClick = {handleSignup}>Sign Up</p>
            <p className="hover:cursor-pointer" onClick = {handleLogin} >Log In</p>
        </div>
    )

    const goToVideos = () => {
        navigate('/videoindex')
    }
    return(
        <>
            <div className='relative'>
                <nav className=
                    "w-full  
                    z-10
                    bg-lime-500
                    items-center 
                    flex justify-between
                    sticky
                    top-0">
                    <span className='flex w-full items-center  h-full'>
                        <span className='flex sm:w-1/6 sm:min-w-72 max-w-72 items-center'>
                            <img src="/Logo.svg" onClick = {()=>navigate('/')}alt="EVTDS Logo" className=" w-1/2 my-2 sm:ml-14 ml-4 lg:ml-16 min-w-16 hover:cursor-pointer"/>
                            <span className='ml-2 md:text-2xl text-sm font-bold text-slate-600'>BETA</span>
                        </span>

                        <div className="sm:flex flex-1 px-4 xl:ml-0 hidden justify-center">
                            <div className="flex items-center w-full">
                            <SearchBar onSearchSubmit={() => setMobileSearchBarVisible(false)} />
                            </div>
                        </div>

                    </span>
                    <div className='flex items-center justify-between'>
                        {!currentUser &&
                            <button className="sm:mr-4 mr-2 text-xs md:text-sm" onClick={goToVideos}>Jump To Videos</button>
                        }
                        <span className={`text-xs sm:hidden ${currentUser ? 'mr-8 -ml-8':''}`} onClick={()=>
                            {window.scrollTo({
                                top: 0,
                                behavior: 'smooth'
                            })
                            setMobileSearchBarVisible(!mobileSearchBarVisible)}}>Search Videos</span>
                        {sessionLinks}
                    </div>
                </nav>
                <div className={`left-0  absolute bg-lime-500 py-2 w-full shadow-md transition-transform x-51 duration-300 ${
                    mobileSearchBarVisible ? 'translate-y-0' : '-translate-y-full'
                        } ` }>
                    <div className='flex w-full flex-col items-center justify-center relative z-51'>
         
                    <SearchBar onSearchSubmit={() => setMobileSearchBarVisible(false)}/>
                    <div className='text-xs mt-2' onClick={()=>setMobileSearchBarVisible(false)}>X Close</div>
                    </div>
                </div>
            </div>
            {loginFormOpen && (<LoginComponent className="z-10" />)}   
            {signupFormOpen && (<SignupComponent className="z-10" />)}     
        </>
    )
}