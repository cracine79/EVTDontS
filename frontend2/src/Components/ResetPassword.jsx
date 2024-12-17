import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { openLoginModal } from "../Slices/modalSlice";
import { useDispatch } from "react-redux";



export const ResetPassword = () => {
    const dispatch = useDispatch()
    const location = useLocation()
    const navigate = useNavigate()
    const [validToken, setValidToken] = useState(false)
    const [password1, setPassword1] = useState()
    const [password2, setPassword2] = useState()
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

    const submitNewPassword = async (email, password) => {
        const data = {
            email,
            password
        }
        try{
            const response = await fetch("/api/retrieve/reset-password", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            })

            if(response.ok){
                const data = await response.json()

            }
        } catch(error){
            console.error("Error resetting password", error)
        }
    }

    const submitReset = (e) =>{
        e.preventDefault()
        if(password1!=password2){
            setErrorMessage("Passwords Must Match")
        } else if (password1.length < 8) {
            setErrorMessage("Passwords must be a minimum of 8 characters")
        } else {
            submitNewPassword(email, password1)
            setResetSuccessful(true)
        }
    }

    if (!validToken) return <p className="mt-36">Validating token...</p>
    
    return (
        <div className='mt-36 flex items-center  flex-col w-100 h-screen -mb-60'>
            <div className='sm:w-1/2 flex flex-col items-center shadow-2xl rounded-lg sm:mt-16'>
                {
                    !resetSuccessful &&<>
                <p className='text-2xl mt-10'>Password Reset</p>
                <p className='my-6 mx-6'>Enter a new password below to reset and continue on your Econo-quest</p>
                <form className='flex flex-col items-center w-3/4' onSubmit = {submitReset}>
                    <input type="password"  onChange = {(e)=>setPassword1(e.target.value)} className='text-center text-lg my-4 border-2 rounded-md w-full border-black border-solid ' placeholder="New Password" />
                    <input type="password" onChange = {(e)=>setPassword2(e.target.value)} className='text-center  text-lg my-4 border-2 rounded-md w-full border-black border-solid ' placeholder="Confirm Password" />
                    <button type="submit" className='my-4'>Reset Password</button>
                    {errorMessage &&
                        <div className='mb-2 text-sm text-red-400'>{errorMessage}</div>
                    }
                </form>
                    </>
                }
                {
                    resetSuccessful && <>
                        <p className='mt-8'>You successfully reset your password.</p>
                        <button className='my-8' onClick={()=>dispatch(openLoginModal())}>Log In</button>
                    </>
                }
            </div>
    </div>
)
}

