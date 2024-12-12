import { openSignupModal } from "../Slices/modalSlice"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { getAllChapters } from "../Slices/chaptersActions"

export const MainPage = () => {
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleGetStarted = ()=>{
        dispatch(openSignupModal())
    }



    return(
        <>
            <div className="flex  justify-center">
                {/* <div className="font-serif text-5xl w-1/2 ">
                    Learning economics doesn't have to suck...   But it usually does. 
                </div> */}

                <video className='w-11/12 h-auto mt-20' autoPlay loop muted>
                    <source src="intro2.mp4" type="video/mp4" />
                </video>
       
            </div>
            <div className="w-screen h-auto bg-white">
                <div className="mt-20 flex justify-between items-center">
                    <div className='h-100 w-100 flex flex-col items-center'>
                        <img src="/Watch.png" alt="Watch the Videos" className="w-1/2 h-1/2" />
                        <p className="mt-2 w-4/6 text-xl text-center">For real, they don’t. We’ve edited out all the parts that flopped, so all you need to do is kick back, press play, and maybe even laugh while learning. (We said maybe.)</p>
                    </div>
                    <div className="flex flex-col items-center">
                       
                        <video autoPlay loop muted className="w-5/6 rounded-3xl mr-20">
                            <source src="Sample.mp4" type="video/mp4" />
                        </video>
                    </div>
                </div>

                <div>
                    <div className="mt-20 ml-20 flex justify-around items-center">
                        <div className='w-5/6 ml-20'>
                            <img src='/Sampleq.png' className='rounded-xl'></img>
                        </div>
                        <div className='h-100 w-100 flex flex-col items-center '>
                            <img src="/Practice.png" alt="Take the Quizzes" className="w-1/2 h-1/2" />
                            <p className="mt-2 w-4/6 text-xl text-center">Unlike lots of resources, our practice quizzes DON'T suck.  Nope, these bad boys are almost identical to the AP questions you’ll face on game day.  Why waste time practicing with the wrong tools when you can sharpen your skills with the real deal?</p>
                        </div>
                    </div>
                </div>
          

                <div className="mt-20 flex justify-around items-center">
                    <div className='h-100 w-100 flex flex-col items-center'>
                        <img src="/goofs.png" alt="Watch the Videos" className="w-1/2 h-1/2" />
                        <p className="mt-2 w-4/6 text-xl text-center">Got a question wrong? No worries! Our genius algorithm will make sure it haunts you—in the best way possible. In subsequent review sessions we’ll serve up custom quizzes that focus on your weakest spots until you’re an econ ninja.</p>
                    </div>

                        <div className="w-5/6  rounded-3xl mr-20 -ml-10">
                            <img src='/qresults.png' className='rounded-xl'></img>
                        </div>
             
                </div>

                <div >
                    <div className="-mt-20 mx-20 flex justify-center items-center">
                        <div >
                            <video className='w-11/12 h-auto mt-20' autoPlay loop muted>
                                <source src="whiteEconoWarrior.mp4" />
                            </video>       
                        </div>
                        <div className='flex flex-col items-center mt-10 -ml-10'>
                            <img src="/keepGoing.png" alt="Take the Quizzes" className="w-1/2 h-1/2" />
                            <p className="mt-2 w-4/6 text-xl text-center">The learning never stops, and neither does our algorithm. We’ll keep feeding you personalized practice until you’re ready to crush the AP exam and beyond. Think of it as a never-ending supply of knowledge. You’re welcome.</p>
                        </div>
                    </div>
                </div>
                
            </div>
            <div className='flex justify-center items-center w-full mt-24 mb-12 '>
                   <div className='px-6 bg-slate-300 hover:cursor-pointer hover:bg-slate-500 py-6 border-black border text-center rounded-xl'
                   onClick={handleGetStarted}>
                        <div className='text-3xl '>Sign up to Get Started!</div>
                        <div className=''>C'mon, what else are you doing right now?</div>
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
                        <div className='text-3xl '>Jump to Videos</div>
                        <div className=''>You can always sign up later</div>
                    </div> 
            </div>
        </>
    )
}