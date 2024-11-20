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
        <div className='mt-36'>
            <form>
          
                <input type="password" placeholder="New Password" />
                <input type="password" placeholder="Confirm Password" />
                <button type="submit">Reset Password</button>
            </form>
    </div>
)
}

