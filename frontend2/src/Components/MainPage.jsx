import { openSignupModal } from "../Slices/modalSlice"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { getAllChapters } from "../Slices/chaptersActions"
import { useEffect, useState } from "react"

export const MainPage = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleGetStarted = ()=>{
        dispatch(openSignupModal())
    }
    const [isAutoplay, setIsAutoplay] = useState(true)

    useEffect(()=>{
        if(window.innerWidth >= 640){
            setIsAutoplay(true)
        } else {
            setIsAutoplay(false)
        }
    }, [])


    return(
        <div className='flex flex-col w-screen items-center'>
            <div className="flex  justify-center">

                <video className='w-full sm:w-11/12 h-auto sm:mt-24 hidden sm:block' autoPlay={isAutoplay} loop muted>
                    <source src="intro2.mp4" type="video/mp4" />
                </video>
                <img src="/MobileBannerTopReal.jpg" className='mt-24 sm:hidden'></img>
       
            </div>

            <div className="w-screen h-auto bg-white items-center">
                <div className="sm:mt-20 mt-8 flex sm:flex-row flex-col justify-between items-center">
                    <div className='h-100 w-100 flex flex-col items-center'>
                        <img src="/Watch.png" alt="1: Watch the Videos that Don't Suck" className="sm:w-1/2 sm:h-1/2 w-3/4" />
                        <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">For real, they don’t. We’ve edited out all the parts that flopped, so all you need to do is kick back, press play, and maybe even laugh while learning. (We said maybe.)</p>
                    </div>
                    <div className="flex flex-col items-center">
                       
                        <video autoPlay={isAutoplay} loop muted className="w-5/6 rounded-3xl hidden sm:block sm:mr-20 mt-4 sm:mt-0">
                            <source src="Sample.mp4" type="video/mp4" />
                        </video>
                        <img src="MobileMiniVid.jpg" className= "mt-6 w-5/6 rounded-3xl sm:hidden"></img>
                    </div>
                </div>

                <div>
                    <div className="sm:mt-20 mt-8 sm:ml-20 flex justify-around flex-col sm:flex-row items-center">
                        <div className='w-5/6 sm:ml-20 sm:block hidden'>
                            <img src='/Sampleq.png' className='rounded-xl'></img>
                        </div>
                        <div className='h-100 w-100 flex flex-col items-center '>
                            <img src="/Practice.png" alt="2: Take the Quizzes like a Boss" className="sm:w-1/2 sm:h-1/2 w-3/4" />
                            <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">Unlike lots of resources, our practice quizzes DON'T suck.  Nope, these bad boys are almost identical to the AP questions you’ll face on game day.  Why waste time practicing with the wrong tools when you can sharpen your skills with the real deal?</p>
                        </div>
                        <div className='sm:w-5/6 w-11/12 mt-4 sm:mt-0 sm:hidden xs:block'>
                            <img src='/Sampleq.png' className='rounded-xl'></img>
                        </div>
                    </div>
                </div>
          

                <div className="sm:mt-20 mt-8 flex justify-around items-center flex-col sm:flex-row">
                    <div className='h-100 w-100 flex flex-col items-center'>
                        <img src="/goofs.png" alt="3: Turn Goofs into Gold" className="sm:w-1/2 sm:h-1/2 w-3/4" />
                        <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">Got a question wrong? No worries! Our genius algorithm will make sure it haunts you—in the best way possible. In subsequent review sessions we’ll serve up custom quizzes that focus on your weakest spots until you’re an econ ninja</p>
                    </div>

                        <div className="w-5/6  rounded-3xl sm:mr-20 sm:-ml-10 mt-4 sm:mt-0">
                            <img src='/qresults.png' className='rounded-xl'></img>
                        </div>
             
                </div>

                <div >
                    <div className="sm:-mt-20 sm:mx-20 flex justify-center items-center flex-col sm:flex-row">
                        <div >
                            <video className='w-11/12 h-auto mt-20 hidden sm:block' autoPlay={isAutoplay} loop muted>
                                <source src="whiteEconoWarrior.mp4" />
                            </video>       
                        </div>
                        <div className='flex flex-col items-center mt-10 sm:-ml-10 '>
                            <img src="/keepGoing.png" alt="4. Keep Going You Econo Warrior" className="sm:w-1/2 sm:h-1/2 w-3/4" />
                            <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">The learning never stops, and neither does our algorithm. We’ll keep feeding you personalized practice until you’re ready to crush the AP exam and beyond. Think of it as a never-ending supply of knowledge. You’re welcome.</p>
                        </div>
                        <div className='flex flex-col justify-center items-center sm:hidden my-4'>
                        <img src='MobileKnight.jpg' className='w-5/6'></img>
                        </div>
                    </div>
                </div>
                
            </div>
            <div className='flex justify-center items-center sm:w-full w-3/4  sm:mt-24 mb-12 '>
                   <div className='px-6 bg-slate-300 hover:cursor-pointer hover:bg-slate-500 py-6 border-black border text-center rounded-xl'
                   onClick={handleGetStarted}>
                        <div className='sm:text-3xl text-2xl '>Sign up to Get Started!</div>
                        <div className='sm:text-xl text-md'>C'mon, what else are you doing right now?</div>
                    </div> 
            </div>
            <div className='text-center text-5xl font-bold '>
                OR
            </div>
            <div className='flex justify-center items-center w-full mt-12 mb-12 '>
                   <div className='px-6 bg-slate-300 hover:cursor-pointer hover:bg-slate-500 py-6 border-black border text-center rounded-xl'
                   onClick={()=> {
                    dispatch(getAllChapters())
                    navigate('/videoindex')
                   }}>
                        <div className='sm:text-3xl text-2xl '>Jump to Videos</div>
                        <div className='m:text-xl text-md'>You can always sign up later</div>
                    </div> 
            </div>
            <div className='flex w-full items-center justify-center flex-col sm:mt-12'>
                <div className='text-3xl mb-8 text-center'>Building The Future of Economics (One Quirk at a Time)</div>
                <img className='w-1/2 md:w-auto'src='/Worker.png'></img>
                <div className='sm:w-1/2 w-3/4 mt-4 mb-12'>Welcome to the early days of what will soon be the most exciting corner of the internet (or at least we hope). Sure, it’s a work in progress—kind of like that IKEA furniture you swore you’d finish assembling months ago. But don't worry, we're not done building. More videos, quizzes, and mind-blowing econ insights are on the way, along with features so cool they'll make you question why you ever doubted economics could be fun. Stick around—it’s only going to get better. And hey, if you spot a bug or something weird, let’s call it a ‘feature in beta.’</div>
            </div>
        </div>
    )
}