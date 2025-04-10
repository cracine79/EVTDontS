import { useLocation } from "react-router-dom"
import { useState } from "react"
import { useDispatch } from "react-redux"
import { loginUser, signupUser } from "../Slices/userActions"
import { useNavigate } from "react-router-dom"
import { BsFillEyeFill, BsFillEyeSlashFill } from "react-icons/bs";

export const Whoops = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const error = location.state?.error;
    const source = location.state?.source;
    const dispatch = useDispatch();
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const [email, setEmail] = useState();
    const [showPassword, setShowPassword] = useState(false);

    let action = '';

    if (source == 'login'){
        action = ' logging in';
    } else if (source == 'signup'){
        action = ' signing up';
    } 

    const problem = (error.split('-')[1]);
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (source == 'login'){
            const result = await dispatch(loginUser(username, password))
            if(result.error){
            navigate('/whoops', {state: {error: result.error, source: 'login'}})
            } else {
            navigate('/userhome')
            }
        } else if (source == 'signup') {
            const result = await dispatch(signupUser(username, email, password))
            if (result.error){
                navigate('/whoops', {state: {error: result.error, source: 'signup'}})
            } else {
                navigate('/getstarted')
            }
        }
    }

    return(
        <div className='sm:mt-48 mt-24 flex flex-col items-center h-full min-h-screen'>
            <div className='sm:w-2/3 flex flex-col items-center shadow-2xl rounded-lg relative'>
                    <form className='flex flex-col  items-center w-100' onSubmit = {handleSubmit}>
                    <img src='oops.png' className = 'flex flex-col items-center w-1/2 mt-16'></img>
                    <p className = 'my-4 text-2xl'>There was a problem{action}:</p>
                    <p className = 'text-xl'>{problem}</p>
                    <p className = 'text-xl my-2'> Give it another shot</p>
                        {source =='signup' &&<input type='email' placeholder = 'Email' className='p-2 w-1/2 border-2 border-neutral-300 my-4' onChange = {(e)=>setEmail(e.target.value)}></input>}
                        <input type='username' placeholder = 'Username' className='p-2 w-1/2 border-2 border-neutral-300 my-4' onChange = {(e)=>setUsername(e.target.value)}></input>
                        <div className='w-1/2 relative'>
                            <input type={showPassword ? 'text' : 'password'} placeholder = 'Password' className='p-2 w-full border-2 border-neutral-300 my-4' onChange = {(e)=>setPassword(e.target.value)}></input>
                            <button type="button" className="absolute inset-y-0 right-3  flex items-center" onClick = {()=>setShowPassword((prev)=>!prev)}> {showPassword ? <BsFillEyeSlashFill className="text-gray-400"  size={24}/> : <BsFillEyeFill className="text-gray-400" size={24} />} </button>
                        </div>
                        <button type='submit' className='mt-8 mb-16 button w-[15%]'>{source=='login' ? 'Login' : 'Sign Up'}</button>
                        {source=='login' && <div className='button  w-[15%] -mt-8 mb-8' onClick={()=>navigate('/retrievedata', {state:{source: 'forgotPassword'}})}>Forgot Password?</div>}
                    </form>
            </div>
         
        </div>
    )
}