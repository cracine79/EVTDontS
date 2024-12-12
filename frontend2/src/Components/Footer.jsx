import { useNavigate } from "react-router-dom"

export const Footer = () => {
    const navigate = useNavigate()
    return (
        <div className = 'w-full'>
            <div className='h-52 bg-green-600 flex flex-col  items-center w-full'>
            <div className='mt-8 text-white text-xl w-1/3 flex justify-between'>
                <a href="#">About Us</a> | <span className='hover:cursor-pointer'onClick={()=>navigate('/privacypolicy')}>Privacy Policy</span> | <a href="#">Terms of Service</a>
                | <a href="mailto:admin@evtds.com">Contact Us</a> 
            </div>    
            <div className='flex w-1/4 justify-around'>
                <div className = 'text-white text-4xl mt-6 hover:cursor-pointer'> 
                    <a className='text-white hover:text-green-800' href='https://github.com/cracine79'>
                        <i class="fa-brands fa-github"></i> 
                    </a>
                </div>
                <div className = 'text-white text-4xl mt-6 hover:cursor-pointer'> 
                    <a className='text-white hover:text-green-800' href='https://www.youtube.com/channel/UC84BLMH2b5kquBloCaiddrw'>
                        <i class="fa-brands fa-youtube"></i> 
                    </a>
                </div>

                <div className = 'text-white text-4xl mt-6 hover:cursor-pointer'> 
                    <a className='text-white hover:text-green-800' href='https://www.instagram.com/econ_quick_hits/?igsh=MTl5cWM1aWN6ZnBoaw%3D%3D'>
                        <i class="fa-brands fa-instagram"></i> 
                    </a>
                </div>

                <div className = 'text-white text-4xl mt-6 hover:cursor-pointer'> 
                    <a className='text-white hover:text-green-800' href='https://www.linkedin.com/in/charlee-racine-50241a7b/'>
                        <i class="fa-brands fa-linkedin"></i> 
                    </a>
                </div>

                <div className = 'text-white text-4xl mt-6 hover:cursor-pointer'> 
                    <a className='text-white hover:text-green-800' href='https://cracine79.github.io/Portfolio/'>
                        <i class="fa-solid fa-folder-open"></i> 
                    </a>
                </div>
            </div>
    
   

            
       
            <div className="text-white ml-8 mt-4 flex flex-col justify-center items-center">    
                    <p>EVTDS is a work in progress by CharLee Racine.</p>
                    <p>© 2024 EVTDS. All rights reserved.</p>
            </div>
          
            </div>
        </div>
    )
}