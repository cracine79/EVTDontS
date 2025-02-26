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
        <div className="sm:mr-28 flex justify-between sm:w-[15vw] items-center">
            <div className="sm:w-16  text-white flex items-center  text-center justify-end mt-2 flex-col hover:cursor-pointer hover:text-[#97afb9]" onClick={()=>{navigate('/video-library')}}>
                <i className="fa-solid fa-video text-xl "></i>
                <p> Videos</p>
            </div>
            <div className="w-16  text-white flex items-center mr-4 text-center justify-end mt-2 flex-col hover:cursor-pointer hover:text-[#97afb9]" onClick={()=>{navigate('/userhome')}}>
                <i className="fa-solid fa-house text-xl "></i>
                <p> Home</p>
                
            </div>
            
            <UserMenu/>
            {/* <LogoutButton/> */}
        </div>
    ) : (
        <div className="flex sm:w-1/4 justify-between items-center mr-4 sm:mr-36 text-xs md:text-sm text-white">
            <p className="hover:cursor-pointer hover:text-[#344A53] sm:text-lg font-bold text center" onClick = {handleLogin} >Log In</p>
            <p className="button sm:block text-center font-bold  sm:!px-6 sm:!py-2" onClick = {handleSignup}>Get Started</p>
           
        </div>
    )

    const goToVideos = () => {
        navigate('/video-library')
    }
    return(
        <>
            <div className='relative'>
                <nav className=
                    "w-full  
                 
                    bg-[#0088A8]
                    items-center 
                    flex justify-between
                    fixed
                    top-0
                    z-50">
                    <div className='flex w-2/3  items-center  h-full py-4 '>
                        <span className='flex sm:w-1/6 sm:min-w-72 max-w-72 items-center'>
                            <img src="/EvtdsDarkerGBlue.png" onClick = {()=>navigate('/')}alt="EVTDS Logo" className=" w-1/2 my-2 sm:ml-14 ml-4 lg:ml-16 min-w-16 hover:cursor-pointer"/>
                            <span className='ml-2 md:text-2xl text-sm font-bold text-white text-slate-600'>BETA</span>
                        </span>

                        <div className="sm:flex flex-auto px-4 xl:ml-0 hidden  w-1/2 justify-left">
                            <div className="flex items-center w-11/12">
                            <SearchBar onSearchSubmit={() => setMobileSearchBarVisible(false)} />
                            </div>
                        </div>

                    </div>
                    <div className={`flex items-center justify-between ${!currentUser && 'w-2/3'}`}>
                        {!currentUser &&
                            <>
                                <button className="sm:mr-4 mr-2 text-xs md:text-lg sm:font-bold text-white hover:text-[#344A53 hidden sm:block" onClick={goToVideos}>Jump To Videos</button>
                                <button className="sm:mr-4 mr-2 text-xs md:text-lg sm:font-bold text-white hover:text-[#344A53 hidden sm:block" onClick={()=>navigate('/aboutus')}>About Us</button>
                                <button className="sm:mr-4 mr-2 text-xs md:text-lg sm:font-bold text-white hover:text-[#344A53] hidden sm:block" onClick={()=>navigate('/contactus')}>Contact Us</button>
                            </>
                        }
                        <span className={`text-xs text-white sm:hidden ${currentUser ? 'mr-6':''}`} onClick={()=>
                            {window.scrollTo({
                                top: 0,
                                behavior: 'smooth'
                            })
                            setMobileSearchBarVisible(!mobileSearchBarVisible)}}>Search Videos</span>
                        {sessionLinks}
                    </div>
                </nav>
                <div className={`left-0  absolute bg-[#0088a8] py-2 mt-[70px] w-full shadow-md z-30 transition-transform x-51 duration-300 ${
                    mobileSearchBarVisible ? 'translate-y-0' : '-translate-y-full'
                        } ` }>
                    <div className='flex w-full flex-col items-center justify-center relative '>
         
                    <SearchBar onSearchSubmit={() => setMobileSearchBarVisible(false)}/>
                    <div className='text-xs text-white mt-2' onClick={()=>setMobileSearchBarVisible(false)}>X Close</div>
                    </div>
                </div>
            </div>
            {loginFormOpen && (<LoginComponent className="z-10" />)}   
            {signupFormOpen && (<SignupComponent className="z-10" />)}     
        </>
    )
}