import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";


export const ResetPassword = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const [validToken, setValidToken] = useState(false)

    const queryParams = new URLSearchParams(location.search)
    const token = queryParams.get("token")
    console.log(token)
    
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

    if (!validToken) return <p className="mt-36">Validating token...</p>
    
    return (
        <div className='mt-36 flex items-center  flex-col w-100 h-screen -mb-60'>
            <div className='w-1/3 flex flex-col items-center shadow-2xl rounded-lg mt-36'>
                <p className='text-2xl mt-10'>Password Reset</p>
                <p className='my-6'>Enter a new password below to reset and continue on your Econo-quest</p>
                <form className='flex flex-col items-center'>
            
                    <input type="password"  className='text-center my-4 ' placeholder="New Password" />
                    <input type="password" className='text-center my-4' placeholder="Confirm Password" />
                    <button type="submit" className='my-4'>Reset Password</button>
                </form>
            </div>
    </div>
)
}

