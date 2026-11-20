import { useEffect, useRef } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useLocation, useNavigate } from 'react-router-dom'
import { openLoginModal, openSignupModal } from '../Slices/modalSlice'
import LoginComponent from './LoginComponent'
import SignupComponent from './SignupComponent'

// Only allow going back to pages on this site (e.g. "/videos/taxes"), never another domain
const safeNext = (value) => (value && value.startsWith('/') && !value.startsWith('//') ? value : '/')

/**
 * /app/login and /app/signup: the login/signup modal over a plain background in the public
 * site's colors, used by the server-rendered pages' "Log In" / "Get Started" buttons.
 * Closing the modal returns the visitor to the page they came from (?next=...).
 */
export const AuthGate = ({ mode }) => {
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    const next = safeNext(new URLSearchParams(location.search).get('next'))
    const loggedIn = useSelector((state) => !!state.user.username)
    const isOpen = useSelector((state) => (mode === 'signup' ? state.modal.isSignupOpen : state.modal.isLoginOpen))
    const wasOpen = useRef(false)

    useEffect(() => {
        dispatch(mode === 'signup' ? openSignupModal() : openLoginModal())
    }, [mode, dispatch])

    // Already logged in (e.g. a stale "Log In" link): go to the dashboard
    useEffect(() => {
        if (loggedIn && !isOpen) navigate('/userhome', { replace: true })
    }, [loggedIn, isOpen, navigate])

    // Modal closed without logging in -> back to the page they came from
    useEffect(() => {
        if (isOpen) {
            wasOpen.current = true
        } else if (wasOpen.current && !loggedIn && location.pathname.match(/\/(login|signup)$/)) {
            window.location.assign(next)
        }
    }, [isOpen, loggedIn, location.pathname, next])

    return (
        <div className="min-h-screen bg-[#344A53] flex flex-col">
            <div className="bg-[#0088A8] px-4 sm:px-12 py-3 flex items-center">
                <a href="/" className="flex items-center gap-2">
                    <img src="/app/EvtdsDarkerGBlue.png" alt="Economics Videos That Don't Suck" className="h-10 sm:h-14" />
                    <span className="text-sm sm:text-2xl font-bold text-white">BETA</span>
                </a>
            </div>
            <div className="flex-1 flex flex-col items-center justify-center text-center px-6 opacity-40 text-white">
                <div className="text-4xl sm:text-6xl font-extrabold">
                    Economics videos that <span className="text-[#FFC93C]">don&apos;t suck.</span>
                </div>
            </div>
            {/* the modals bring their own (dark-text) styling */}
            {mode === 'signup' ? <SignupComponent /> : <LoginComponent />}
        </div>
    )
}
