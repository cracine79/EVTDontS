import { useLocation } from "react-router-dom"
import { useState } from "react"
import { useDispatch } from "react-redux"
import { loginUser } from "../Slices/userActions"
import { useNavigate } from "react-router-dom"

export const Whoops = () => {
    const navigate = useNavigate()
    const location = useLocation()
    const error = location.state?.error
    const source = location.state?.source
    const dispatch = useDispatch()
    const [username, setUsername] = useState()
    const [password, setPassword] = useState()
    const [email, setEmail] = useState()

    let action = ''
    if (source == 'login'){
        action = ' logging in'
    } else if (source == 'signup'){
        action = ' signing up'
    } 

    const problem = (error.split('-')[1])
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (source == 'login'){
            const result = await dispatch(loginUser(username, password))
            if(result.error){
            navigate('/whoops', {state: {error: result.error, source: 'login'}})
            } else {
            navigate('/userhome')
    }
        }
    }

    return(
        <div className='mt-48 flex flex-col items-center h-full min-h-screen'>
            <div className='w-2/3 flex flex-col items-center shadow-2xl rounded-lg'>
                    <form className='flex flex-col  items-center w-100' onSubmit = {handleSubmit}>
                    <img src='oops.png' className = 'flex flex-col items-center w-1/2 mt-16'></img>
                    <p className = 'my-4 text-2xl'>There was a problem{action}:</p>
                    <p className = 'text-xl'>{problem}</p>
                    <p className = 'text-xl my-2'> Give it another shot</p>
                        <input type='username' placeholder = 'Username' className='p-2 w-1/2 border-2 border-neutral-300 my-4' onChange = {(e)=>setUsername(e.target.value)}></input>
                        {source =='signup' &&<input type='email' placeholder = 'Email' className='p-2 w-1/2 border-2 border-neutral-300 my-4' onChange = {(e)=>setEmail(e.target.value)}></input>}
                        <input type='password' placeholder = 'Password' className='p-2 w-1/2 border-2 border-neutral-300 my-4' onChange = {(e)=>setPassword(e.target.value)}></input>
                        <button type='submit' className='mt-8 mb-16'>{source=='login' ? 'Login' : 'Sign Up'}</button>
                    </form>
            </div>
         
        </div>
    )
}