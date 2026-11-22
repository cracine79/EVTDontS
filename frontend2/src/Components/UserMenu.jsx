import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import LogoutButton from "./LogoutComponent";
import { clearQuestions } from "../Slices/questionsSlice"
import { clearUserResults } from "../Slices/resultsSlice"

// Avatar + dropdown in the nav; same items as the public pages' user menu (templates/_user_menu.html)
export const UserMenu = () => {
    const username = useSelector((state) => state.user.username) || ''
    const name = username ? username[0].toUpperCase() + username.slice(1) : ''
    const navigate = useNavigate()
    const dispatch = useDispatch()
    const [open, setOpen] = useState(false)
    const ref = useRef(null)

    useEffect(() => {
        const close = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false) }
        document.addEventListener('click', close)
        return () => document.removeEventListener('click', close)
    }, [])

    const go = (path) => {
        setOpen(false)
        dispatch(clearQuestions())
        dispatch(clearUserResults())
        navigate(path)
    }

    const item = 'w-full flex items-center gap-3 px-4 py-2 hover:bg-white/10 text-left'
    const icon = 'w-5 text-[#7fd3e6]'

    return (
        <div className="relative" ref={ref} data-tour="menu">
            <button type="button" aria-expanded={open} onClick={() => setOpen(!open)}
                className="flex items-center gap-2 bg-[#344A53]/40 hover:bg-[#344A53]/70 rounded-full pl-1 pr-3 py-1">
                <span className="w-8 h-8 rounded-full bg-[#FFC93C] text-[#111] flex items-center justify-center font-black">{name[0]}</span>
                <span className="hidden sm:inline">{name}</span>
                <i className="fa-solid fa-chevron-down text-xs"></i>
            </button>
            {open && (
                <div className="absolute right-0 mt-2 w-60 bg-[#2B3D45] border border-white/10 rounded-2xl shadow-2xl py-2 text-base font-semibold z-50">
                    <button type="button" className={item} onClick={() => go('/userhome')}><i className={`fa-solid fa-house ${icon}`}></i>My dashboard</button>
                    <a className={item} href="/videos"><i className={`fa-solid fa-video ${icon}`}></i>Video library</a>
                    <button type="button" className={item} onClick={() => go('/quizgenerator')}><i className={`fa-solid fa-bolt ${icon}`}></i>Review quiz</button>
                    <button type="button" className={item} onClick={() => go('/updateunits')}><i className={`fa-solid fa-sliders ${icon}`}></i>Update study plan</button>
                    <hr className="my-2 border-white/10" />
                    {/* The whole row is the button, not just the word */}
                    <LogoutButton className={item} icon={<i className={`fa-solid fa-right-from-bracket ${icon}`}></i>} label="Log out" />
                </div>
            )}
        </div>
    )
}
