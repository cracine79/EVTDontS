import { useDispatch, useSelector } from "react-redux"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
// import { useAppSelector } from "../../app/hooks"
import csrfFetch from "../session/csrf"
import { loginUser } from "../session/sessionSlice"

export const Login = () => {
    const dispatch = useDispatch();
    const [username, setUsername] = useState("");
    const [password, setPassword]=useState("");
    // const [email, setEmail]=useState("");

    const user = useSelector((state)=>state.user.user)

    // console.log(username)
    // console.log(password)

    const getIt = async (e)=>{
        e.preventDefault()
        csrfFetch('/api/questions/hello')
                .then(response=>{
                    if(!response.ok){
                        throw new Error("oops")
                    }
                    return response.json();
                })
                .then(data=>{
                    console.log(data)
                })
    }

    const handleLogin = () => {
        dispatch(loginUser({username, password}))
    }

    return (
        <>
             <h1 className="text-3xl text-orange-800">
             Hello from home!! Dude I love it
             </h1>

             <form>
                <p>Hello {user} </p>
                <p>Username</p>
                <input type='text' className='border-black border' onChange = {e=>setUsername(e.target.value)}></input>
                <p className='text-lg text-orange-800'>Password</p>
                <input type='text' className='border-black border' onChange = {e=>setPassword(e.target.value)}></input>
                <input type='submit' onClick={handleLogin}/>
     
            </form>
          
        </>
    )
}
