import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { openLoginModal } from "../Slices/modalSlice";
import { useDispatch } from "react-redux";
import { PASSWORD_HINT, PasswordChecklist, passwordOk } from "./PasswordRules";



export const ResetPassword = () => {
    const dispatch = useDispatch()
    const location = useLocation()
    const navigate = useNavigate()
    const [validToken, setValidToken] = useState(false)
    const [password1, setPassword1] = useState('')
    const [password2, setPassword2] = useState('')
    const [errorMessage, setErrorMessage] = useState()
    const [email, setEmail]= useState()
    const [resetSuccessful, setResetSuccessful] = useState(false)

    const queryParams = new URLSearchParams(location.search)
    const token = queryParams.get("token")

    
    useEffect(()=>{

        const validateToken = async () => {
            
            try{
                const response = await fetch("/api/retrieve/validate-token", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({token})
                })

                const data = await response.json()
               
                if(response.ok){
                    setEmail(data.email)
                    setValidToken(true)
                } else {
                    alert(data.error || "Invalid or expired token")
                    navigate("/")
                }
            } catch (error) {
                console.error("Error validating token", error)
                navigate("/")
            }
            
        }
        if (token) {
            validateToken()
        }
    }, [token, navigate])

    const submitNewPassword = async (password) => {
        const data = {
            token,
            password
        }
        try{
            const response = await fetch("/api/retrieve/reset-password", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            })

            if(response.ok){
                setResetSuccessful(true)
            } else {
                const data = await response.json().catch(()=>({}))
                setErrorMessage(data.error || data.message || "Something went wrong. Please request a new reset link.")
            }
        } catch(error){
            console.error("Error resetting password", error)
            setErrorMessage("Something went wrong. Please try again.")
        }
    }

    const submitReset = (e) =>{
        e.preventDefault()
        if(password1!=password2){
            setErrorMessage("Passwords Must Match")
        } else if (!passwordOk(password1)) {
            setErrorMessage(PASSWORD_HINT)
        } else {
            submitNewPassword(password1)
        }
    }

    if (!validToken) return <p className="pt-36 pb-32 text-center text-gray-300">Checking your reset link…</p>

    return (
        <div className="pt-24 sm:pt-28 pb-16 px-5 sm:px-10">
            <section className="max-w-xl mx-auto panel rounded-3xl p-6 sm:p-10 border-t-8 border-[#7fd3e6]">
                {!resetSuccessful ? <>
                    <h1 className="text-3xl font-extrabold">Pick a new password</h1>
                    <p className="mt-3 text-gray-200">Enter a new password below to reset it and continue on your Econo-quest.</p>
                    <form className="mt-6 space-y-4" onSubmit={submitReset}>
                        <div>
                            <input type="password" autoComplete="new-password" value={password1} onChange={(e) => setPassword1(e.target.value)} className="field" placeholder="New password" aria-describedby="password-rules" maxLength={20} />
                            <PasswordChecklist password={password1} dark className="mt-3" />
                        </div>
                        <input type="password" autoComplete="new-password" value={password2} onChange={(e) => setPassword2(e.target.value)} className="field" placeholder="Type it again" maxLength={20} />
                        {password2 && <p className={`text-sm ${password1 === password2 ? 'text-[#C6E83A]' : 'text-gray-400'}`}>
                            <i className={`fa-solid ${password1 === password2 ? 'fa-circle-check' : 'fa-circle-xmark'} mr-2`}></i>
                            {password1 === password2 ? 'Passwords match' : "Passwords don't match yet"}
                        </p>}
                        {errorMessage && <p className="font-bold text-[#FF6FAE]" role="alert">{errorMessage}</p>}
                        <button type="submit" className="btn-primary px-7 py-3">Reset my password</button>
                    </form>
                </> : <>
                    <h1 className="text-3xl font-extrabold"><i className="fa-solid fa-circle-check text-[#C6E83A] mr-2"></i>Password reset</h1>
                    <p className="mt-3 text-gray-200">You're all set. Log in with your new password.</p>
                    <button type="button" className="btn-primary px-7 py-3 mt-6" onClick={() => dispatch(openLoginModal())}>Log in</button>
                </>}
            </section>
        </div>
    )
}
