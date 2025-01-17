import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';
import { closeLoginModal } from '../Slices/modalSlice';
import { IoMdClose } from "react-icons/io";
import { useNavigate } from 'react-router-dom';
import { storeUserUnits } from '../Slices/unitsSlice';
import { updateChapters } from '../Slices/chaptersSlice';
import { storeTopicProg } from '../Slices/topicProgSlice';
import { storeUserChapters } from '../Slices/userChaptersSlice';
import { storeTopics } from '../Slices/topicsSlice';
import { loginUser } from '../Slices/userActions';

const LoginComponent = () => {
  const showModal= useSelector(state=>(state.modal.isLoginOpen))
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(loginUser(username, password))
    dispatch(closeLoginModal())
    if(result.error){

      navigate('/whoops', {state: {error: result.error, source: 'login'}})
    } else {

      navigate('/userhome')
    }
  };

  const handleClose = ()=>{
    dispatch(closeLoginModal())
  }

  const goToForgot = () => {
    dispatch(closeLoginModal())
    navigate('/retrievedata', {state:{source: 'forgotPassword'}})
  }

  const goToForgotUsername = () => {
    dispatch(closeLoginModal())
    navigate('/retrievedata', {state:{source: 'forgotUsername'}})
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
              <div className="text-xl md:mt-5 mt-28">Welcome Back Fellow Econo-Warrior!</div>
              <input
                className='
                            p-2
                            w-4/5
                            border-2
                            border-neutral-300
                            mt-5
                        '
                type="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
              />
              <div className='w-4/5'>
               
                <button onClick={goToForgotUsername} className='text-xs text-blue-400 font-bold' type='button'>Forgot Username?</button>
              </div>
              <input
                className='
                p-2
                w-4/5
                border-2
                border-neutral-300
                mt-5'
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
              />
              <div className='w-4/5'>
              <button onClick={goToForgot} className='text-xs text-blue-400 font-bold' type='button'>Forgot Password?</button>
             
              </div>
              <button type="submit" className='mt-6'>Login</button>


              
            </form>
          </div>
        </div>
      </div>
    </div>
  );
  
};

export default LoginComponent;
