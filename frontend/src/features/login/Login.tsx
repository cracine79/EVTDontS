import { useDispatch, useSelector } from "react-redux"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

export const Login = () => {
    const dispatch = useDispatch();
    const [username, setUsername] = useState("");
    const [password, setPassword]=useState("");
    const [email, setEmail]=useState("");


    return (
        <>
            <form>
                <p>Username</p>
                <input type='text' className='border-black border'></input>
                <p>Email</p>
                <input type='text' className='border-black border'></input>
                <p>Password</p>
                <input type='text' className='border-black border'></input>
                <input type='submit'/>
            </form>
            
        </>
    )
}
