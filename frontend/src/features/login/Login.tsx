import { useDispatch, useSelector } from "react-redux"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAppSelector } from "../../app/hooks"

export const Login = () => {
    const dispatch = useDispatch();
    const [username, setUsername] = useState("");
    const [password, setPassword]=useState("");
    const [email, setEmail]=useState("");

    const user = useAppSelector((state)=>state.user.user)
    console.log(user)

    return (
        <>
            <form>
                <p>Hello {user} </p>
                <p>Username</p>
                <input type='text' className='border-black border'></input>
                <p>Password</p>
                <input type='text' className='border-black border'></input>
                <input type='submit'/>
            </form>
            
        </>
    )
}
