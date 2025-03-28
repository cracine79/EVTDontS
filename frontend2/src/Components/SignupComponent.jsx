import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';
import { closeSignupModal } from '../Slices/modalSlice';
import { IoMdClose } from 'react-icons/io';
import { GetStarted } from './GetStarted';
import { useNavigate } from 'react-router-dom';
import { signupUser } from '../Slices/userActions';
import { BsFillEyeFill, BsFillEyeSlashFill } from "react-icons/bs";

const SignupComponent = (results) => {
  const showModal= useSelector(state=>(state.modal.isSignupOpen))
  const dispatch = useDispatch();
  const quizData = useSelector((state)=>state.modal.sourceData)
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('')
  const navigate = useNavigate()
  const [showPassword, setShowPassword] = useState(false);

  console.log(quizData)
  
  const handleSubmit = async (e) => {
    e.preventDefault(); 
    const result = await dispatch(signupUser(username, email, password, quizData))
    dispatch(closeSignupModal())
    if(result.error){
      navigate('/whoops', {state: {error: result.error, source: 'signup'}})
    } else {
      navigate('/getstarted')
    }
  };

  const handleClose = ()=>{
    dispatch(closeSignupModal())
  }

  return (
    <div
      className="
        justify-center
        items-center
        flex
        overflow-x-hidden
        overflow-y-auto
        fixed
        inset-0
        z-50
        outline-none
        focus:outline-none
        bg-neutral-800/70
      "
    >
      <div
        className={`
          translate
          relative
          w-full
          md:w-4/6
          lg:w-3/6
          xl:w-2/5
          my-6
          mx-auto
          h-full
          lg:h-auto
          md:h-auto
          flex
          justify-center
          items-center
        `}
      >
        <div
          className={`
            translate
            h-full
            lg:h-auto
            md:h-auto
            border-0
            rounded-lg
            shadow-lg
            relative
            flex
            flex-col
            w-full
            bg-white
            outline-none
            focus:outline-none
             transition-transform
            duration-300
            z-30
              ${showModal ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'}
          `}
        >
          <div className='"w-full mb-5 relative'>
          <button
										onClick={handleClose}
										className="
											p-1
											border-0
											hover:opacity-70
											transition
											absolute
											right-3
                      top-2
										"
									>
										<IoMdClose size={18}/>
						</button>
            <form className="flex flex-col justify-center items-center"onSubmit={handleSubmit}>
              <div className="text-lg md:mt-5 mt-28 px-6 text-center">Sign Up to Access Quizzes, Track Progress, and More!</div>
              {quizData && <div>Your progress from this quiz will be saved!</div>}
              <input
                className='
                            p-2
                            w-4/5
                            border-2
                            border-neutral-300
                            my-5
                        '
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
              />
              <input
                className='
                            p-2
                            w-4/5
                            border-2
                            border-neutral-300
                            my-5
                        '
                type="text"
                id="username"
                name="username"
                required
                pattern="[A-Za-z0-9_]{3,15}" 
                title="Username must be 3-15 characters long and can only contain letters, numbers, and underscores."
                maxLength="15"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
              />
              <div className='relative w-4/5'>

              <input
                className='
                p-2
                w-full
                border-2
                border-neutral-300
                my-5'
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                minlength="8"
                maxlength="20"        
                pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}"
                title='Password must include at least one uppercase letter, one lowercase letter, one numeral(0-9), and one special character?=.*[!@#$%^&*(),.?\, and be beween 8 and 20 chars long'
                
              />
              
              <button type="button" className="absolute inset-y-0 right-3  flex items-center" onClick = {()=>setShowPassword((prev)=>!prev)}> {showPassword ? <BsFillEyeSlashFill className="text-gray-400"  size={24}/> : <BsFillEyeFill className="text-gray-400" size={24} />} </button>
            </div>
              <button type="submit" className='mt-2
                            button !text-base !py-0 !px-4 my-4 !rounded-3xl !px-8
                            mb-4'>Sign Up</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
export default SignupComponent;
