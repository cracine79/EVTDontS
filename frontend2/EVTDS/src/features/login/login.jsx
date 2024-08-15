import { useDispatch, useSelector } from "react-redux"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
// import { useAppSelector } from "../../app/hooks"

export const Login = () => {
    // const dispatch = useDispatch();
    // const [username, setUsername] = useState("");
    // const [password, setPassword]=useState("");
    // const [email, setEmail]=useState("");

    const user = useSelector((state)=>state.user.user)
    console.log(user)


    const getIt = async (e)=>{
        e.preventDefault()
        const res = await fetch('/questions/hello')
        if(res.ok){
            console.log(res)
            const data = await res.json();
            console.log(data.headers)
        }    
    }

    return (
        <>
            <form>
                <p>Hello {user} </p>
                <p>Username</p>
                <input type='text' className='border-black border'></input>
                <p className='text-lg text-orange-800'>Password</p>
                <input type='text' className='border-black border'></input>
                <input type='submit' onClick={getIt}/>
            </form>
            
        </>
    )
}
