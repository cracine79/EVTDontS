import { useSelector } from "react-redux"
import { useLocation, useNavigate } from "react-router-dom"
import { useState } from "react"
import { UserMenu } from "./UserMenu"
import { goToPublicHome } from "./routes"
import LoginComponent from "./LoginComponent"
import SignupComponent from "./SignupComponent"

// Same search as the public pages: the server-rendered library does the searching
const SearchForm = ({ className = '' }) => (
    <form action="/videos" method="get" role="search" className={`flex h-10 w-full ${className}`}>
        <input name="q" aria-label="Search economics videos"
            className="flex-1 min-w-0 border-white bg-transparent text-white border-b pl-2 focus:outline-none placeholder-white text-sm focus:ring-0"
            placeholder="Search For Econ Videos Here" />
        <button type="submit" aria-label="Search" className="bg-transparent px-3 border-white border-b text-xl text-white hover:text-[#344A53]">
            <i className="fa-solid fa-magnifying-glass"></i>
        </button>
    </form>
)

export const NavBar = () => {
    const navigate = useNavigate()
    const { pathname } = useLocation()
    const currentUser = useSelector(state => state.user.username)
    const [mobileSearch, setMobileSearch] = useState(false)
    // Pages like the free-quiz results open these pop-ups directly
    const loginOpen = useSelector(state => state.modal.isLoginOpen)
    const signupOpen = useSelector(state => state.modal.isSignupOpen)

    const linkClass = (active) =>
        `hidden md:flex items-center gap-2 ${active ? 'text-[#FFC93C]' : 'hover:text-[#344A53]'}`
    const onDashboard = pathname.startsWith('/userhome')
    const onReview = pathname.startsWith('/quizgenerator')

    return (
        <>
            <nav className="w-full bg-[#0088A8] text-white flex items-center justify-between fixed top-0 z-50 px-4 sm:px-8 lg:px-12 py-3 gap-4">
                <button type="button" className="flex items-center gap-2 shrink-0"
                    onClick={() => (currentUser ? navigate('/userhome') : goToPublicHome())}>
                    <img src="/app/EvtdsDarkerGBlue.png" alt="Economics Videos That Don't Suck logo" className="h-10 sm:h-14 w-auto" width="144" height="56" />
                    <span className="text-sm sm:text-2xl font-bold">BETA</span>
                </button>
                <div className="hidden lg:flex flex-1 max-w-md">
                    <SearchForm />
                </div>
                <div className="flex items-center gap-3 sm:gap-5 xl:gap-6 text-sm sm:text-base xl:text-lg font-bold whitespace-nowrap">
                    {currentUser ? (
                        <>
                            <a className={linkClass(false)} href="/videos"><i className="fa-solid fa-video"></i> Video Library</a>
                            <button type="button" className={linkClass(onDashboard)} onClick={() => navigate('/userhome')}><i className="fa-solid fa-house"></i> My Dashboard</button>
                            <button type="button" className={`${linkClass(onReview)} md:hidden xl:flex`} onClick={() => navigate('/quizgenerator')}><i className="fa-solid fa-bolt"></i> Review Quiz</button>
                        </>
                    ) : (
                        <>
                            <a className="hidden md:block hover:text-[#344A53]" href="/videos">Jump To Videos</a>
                            <button type="button" className="hidden md:block hover:text-[#344A53]" onClick={() => navigate('/aboutus')}>About Us</button>
                            <button type="button" className="hidden md:block hover:text-[#344A53]" onClick={() => navigate('/contactus')}>Contact Us</button>
                        </>
                    )}
                    <button type="button" className="lg:hidden hover:text-[#344A53]" aria-label="Search videos"
                        onClick={() => { window.scrollTo({ top: 0, behavior: 'smooth' }); setMobileSearch(!mobileSearch) }}>
                        <i className="fa-solid fa-magnifying-glass"></i>
                    </button>
                    {currentUser ? <UserMenu /> : (
                        <>
                            <button type="button" className="hover:text-[#344A53]" onClick={() => navigate('/login')}>Log In</button>
                            <button type="button" className="btn-primary px-4 sm:px-5 py-2 text-sm sm:text-base" onClick={() => navigate('/signup')}>Get Started</button>
                        </>
                    )}
                </div>
            </nav>
            <div className={`lg:hidden fixed left-0 top-0 mt-[64px] sm:mt-[80px] w-full bg-[#0088a8] py-2 px-4 shadow-md z-40 transition-transform duration-300 ${mobileSearch ? 'translate-y-0' : '-translate-y-[200%]'}`}>
                <SearchForm />
            </div>
            {loginOpen && <LoginComponent />}
            {signupOpen && <SignupComponent />}
        </>
    )
}
