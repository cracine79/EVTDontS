import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../Slices/userSlice';
import { csrfFetch } from '../csrf';
import { closeLoginModal } from '../Slices/modalSlice';
import { IoMdClose } from "react-icons/io";
import { useNavigate } from 'react-router-dom';
import { storeUserUnits } from '../Slices/unitsSlice';

const LoginComponent = () => {
  const showModal= useSelector(state=>(state.modal.isLoginOpen))
  const dispatch = useDispatch();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
    const response = await csrfFetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      // Log the status and response text for debugging
      const errorText = await response.text();
      console.error('Error response status:', response.status);
      console.error('Error response body: ', errorText);
      // Optionally, throw an error to handle it later in the catch block
      throw new Error(`Error ${response.status}: ${errorText}`);
    }
   
    const data = await response.json();
    console.log(data)
    localStorage.setItem('access_token', data.user.access_token);
    dispatch(login(data.user));
    dispatch(storeUserUnits(data.units))
    dispatch(closeLoginModal()) // Store user in Redux state
    navigate('/userhome')
  } catch (error) {
    // Log any errors that occur during fetch or processing
    console.error('Error during login:', error);
  }
  };

  const handleClose = ()=>{
    dispatch(closeLoginModal())
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
              <div className="text-xl mt-5">Welcome Back Fellow Econo-Warrior!</div>
              <input
                className='
                            p-2
                            w-4/5
                            border-2
                            border-neutral-300
                            my-5
                        '
                type="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
              />
              <input
                className='
                p-2
                w-4/5
                border-2
                border-neutral-300
                my-5'
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
              />
              <button type="submit">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
  
};

export default LoginComponent;
