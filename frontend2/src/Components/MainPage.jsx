import { openSignupModal } from "../Slices/modalSlice"
import { useDispatch } from "react-redux"
import { useNavigate } from "react-router-dom"
import { getAllChapters } from "../Slices/chaptersActions"
import { useEffect, useState, useRef } from "react"

export const MainPage = () => {
    const videoRef = useRef(null)
    const videoLeftRef = useRef(null)
    const quizRef = useRef(null)
    const quizRightRef = useRef(null)
    const resultsLeftRef = useRef(null)
    const scrollRef = useRef(null)
    let lastScrollY = useRef(window.scrollY)
    const stickyRef = useRef(null)
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const [vidVisible, setVidVisible] = useState(false)
    const [quizVisible, setQuizVisible] = useState(false)
    const [resultsVisible, setResultsVisible] = useState(false)
    const [warriorVisible, setWarriorVisible] = useState(false)
    const [warriorIsFixed, setWarriorIsFixed] = useState(true)
    const [warriorTop, setWarriorTop]= useState(0)

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
        const vidObserver = new IntersectionObserver(
            ([entry])=>{
                setVidVisible(entry.isIntersecting);
            },
            {threshold: 0.5}
        );

        if (videoLeftRef.current){
            vidObserver.observe(videoLeftRef.current);
        }

        return () => {
            if(videoLeftRef.current) vidObserver.unobserve(videoLeftRef.current)
        }
    }, [])

    useEffect(()=>{
        const quizObserver = new IntersectionObserver(
            ([entry])=>{
                setQuizVisible(entry.isIntersecting);
            },
            {threshold: 0.5}
        );

        if (quizRightRef.current){
            quizObserver.observe(quizRightRef.current)
        }

        return () => {
            if(quizRightRef.current) quizObserver.unobserve(quizRightRef.current)
        }
        
    }, [])

    useEffect(()=>{
        const resultsObserver = new IntersectionObserver(
            ([entry])=>{
                setResultsVisible(entry.isIntersecting);
            },
            {threshold: 0.5}
        );

        if (resultsLeftRef.current){
            resultsObserver.observe(resultsLeftRef.current)
        }

        return () => {
            if(resultsLeftRef.current) resultsObserver.unobserve(resultsLeftRef.current)
        }
        
    }, [])


    useEffect(()=>{
        const keepObserver = new IntersectionObserver(
            ([entry])=>{
                const currentScrollY = window.scrollY
                
                if (entry.isIntersecting ){
                    setWarriorVisible(true)
                } else if (!entry.isIntersecting && currentScrollY < lastScrollY.current ){
                    console.log('currentScrollY', currentScrollY)
                    console.log('lastScrolllY', lastScrollY.current)
                    setWarriorVisible(false)
                }
                lastScrollY.current = currentScrollY;            
            },
            {threshold: 0.8}
        )
        if (scrollRef.current) keepObserver.observe(scrollRef.current);
        


        return () => {
            keepObserver.disconnect()
        }
    }, [])

    useEffect(()=>{
        const handleScroll = () => {
            if (!stickyRef.current || !scrollRef.current) return;

            const stickyTop = stickyRef.current.getBoundingClientRect().top;
            const scrollTop = scrollRef.current.getBoundingClientRect().top;
            const middleOfPage = window.innerHeight/2; 
            console.log('middle', middleOfPage)
            console.log('scrollTop', scrollTop)
            if(scrollTop <= middleOfPage){
                if (warriorIsFixed) {
                    setWarriorTop(stickyRef.current.getBoundingClientRect().top + window.scrollY);
                }
                console.log('THEREITGOES')
                setWarriorIsFixed(false)
                lastScrollY = window
            } else {
                setWarriorIsFixed(true)
            }
        }
        window.addEventListener("scroll", handleScroll)
        return()=>window.removeEventListener("scroll", handleScroll)
    })

    useEffect(()=>{
        if(vidVisible){ 
            if(videoRef.current){
                videoRef.current.play().catch(error=>{
                    console.error("Autoplay error:" , error)
                });
            }
        } else {
            if (videoRef.current){
                videoRef.current.pause()
            }
        }
    }, [vidVisible])


    return(
        <div className='flex flex-col w-screen items-center bg-[#344A53] text-white relative'>
            <div className="flex  justify-center sm:mt-8">

                <video className='w-full sm:w-11/12 h-auto sm:mt-24 hidden sm:block rounded-3xl z-20' autoPlay={isAutoplay} loop muted>
                    <source src="intro2.mp4" type="video/mp4" />t
                </video>
                <img src="/MobileBannerTopReal.jpg" className='mt-20 sm:hidden'></img>
       
            </div>
            <div className=' w-11/12 sm:text-2xl text-xs flex justify-around text-center sm:px-28 border-white border-2 border-solid rounded-2xl h-20 items-center'><span>Stop memorizing.</span><span>Start understanding.</span><span>Economics, but finally entertaining.</span></div>
            <div className=' bg-[#2B3D45] w-full pt-12 w-full relative flex '>
            <div className='w-full flex justify-start items-center relative flex-col'>
                    <div className='flex flex-col items-center justify-center text-center text-xl w-['>
                        <div className='text-5xl mb-8'>Ready to Dive In?</div>
                        <div>Browse our <em>free library</em> of economics videos and quizzes!</div>
                        <div className='py-6'>Think of it as an all-you-can-eat buffet of knowledge—without the regret.</div>
                    </div>
                    <div className='button flex flex-col w-[32%] max-w-[450px] h-12 mb-16 !font-light !py-2 !px-6  z-40 '
                        onClick={()=> {
                            dispatch(getAllChapters())
                            navigate('/video-library')
                        }}>
                                <div className='sm:text-lg xl:text-2xl'><span className='hidden sm:inline'>Take Me to the </span>Videos & Quizzes!</div>
                    </div> 
                    <div className='text-xl absolute bottom-0  ml-[17%] p-4 '>Or scroll on to learn how it works!</div>
            </div>
      
            </div>
            
            <div className='w-5/6 items-center justify-center flex relative'>
            
                
                <img className="w-7/12" src='leg1.png'/>
                <div className='w-1/3'></div>
            </div>
        

            <div className="w-screen h-auto items-center bg-[#344A53]">
                {/* 1. Watch the videos an video  */}
                <div className="sm:mt-8 flex sm:flex-row flex-col justify-between sm:w-7/12 items-center" >
                    <div className='h-100 w-100 flex flex-col items-center 'ref={videoLeftRef}>
                        {/* <img src="/Watch.png" alt="1: Watch the Videos that Don't Suck" className="sm:w-1/2 sm:h-1/2 w-3/4" /> */}
                        <div className='flex'>
                                                    
                            <span class="flex items-center justify-center sm:w-[80px] sm:h-[80px]  w-[60px] h-[60px] sm:text-[60px] text-4xl  font-bold sm:font-extrabold  rounded-full  border-[4px] sm:border-[6px] border-[#007ea3]">
                                1
                            </span>
                            <div className='sm:ml-8 wm:ml-2 lg:text-5xl sm:text-4xl text-3xl font-extrabold mb-2'>
                                <div>Watch the Videos</div>
                                <div>(that don't suck)</div>
                            </div>
                        </div>
                        <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">For real, they don’t. We’ve edited out all the parts that flopped, so all you need to do is kick back, press play, and maybe even laugh while learning. (We said maybe.)</p>
                    </div>
                    <div className="flex flex-col items-center">
                       <div >
                            <video autoPlay={isAutoplay} ref={videoRef} loop muted className={`fixed top-1/4 right-0 w-5/12 rounded-3xl hidden sm:block transform  transition-opacity duration-700 sm:mr-12 mt-4 sm:mt-0 ${vidVisible ? "opacity-100":"opacity-0"}`}>
                                <source src="Sample.mp4" type="video/mp4" />
                            </video>
                       </div>
                        <img src="MobileMiniVid.jpg" className= "mt-6 w-5/6 rounded-3xl sm:hidden"></img>
                    </div>
                    
                </div>
                <div className='w-11/12 '>
                     <div className='w-5/6 items-center flex justify-center relative top-0'>
                            <div className='w-1/6'> </div>
                            <img className="w-7/12" src='leg2.png'/>
                            
                        </div>
                </div>
                    

                {/* 2.  Take practice quizzes and quiz  */}
                <div>
                    <div className=" sm:ml-20 flex justify-around flex-col sm:flex-row items-center">
                        <div className={`w-5/6 sm:w-1/3  sm:ml-[5%] sm:block hidden fixed top-[15%] left-20  duration-1000 transition-opacity transform ${quizVisible ? "opacity-100":"opacity-0"}`} ref={quizRef}>
                            <img src='/Sampleq.png' className='rounded-xl'></img>
                        </div>
                        <div className='h-100 sm:w-1/2 sm:ml-[40%] flex flex-col items-center'>
                        {/* <div className='sm:h-96'></div> */}

                        
                        <div className='flex' ref={quizRightRef}>
                            <span class="flex items-center justify-center  sm:w-[80px] sm:h-[80px]  w-[60px] h-[60px] sm:text-[60px] text-4xl  font-bold sm:font-extrabold  rounded-full  border-[4px] sm:border-[6px] border-[#007ea3]">
                                2
                            </span>
                            <div className='sm:ml-8 ml-2 lg:text-5xl sm:text-4xl text-3xl font-extrabold mb-2'>
                                <div>Take practice</div>
                                <div>quizzes like a Boss</div>
                            </div>
                        </div>
                            {/* <img src="/Practice.png" alt="2: Take the Quizzes like a Boss" className="sm:w-1/2 sm:h-1/2 w-3/4" /> */}
                            <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">Unlike some resources, our practice quizzes DON'T suck.  Nope, these bad boys are almost identical to the AP questions you’ll face on game day.  Why waste time practicing with the wrong tools when you can sharpen your skills with the real deal?</p>
                        </div>
                        <div className='sm:w-5/6 w-11/12 mt-4 sm:mt-0 sm:hidden xs:block'>
                            <img src='/Sampleq.png' className='rounded-xl'></img>
                        </div>
                    </div>
                </div>
                <div className='w-11/12'>
                     <div className='w-5/6 items-center flex justify-center relative top-0'>
                            <div className='w-1/3'> </div>
                            <img className="w-7/12" src='leg3.png'/>
                            
                        </div>
                </div>
                    

                <div className=" flex justify-left items-center flex-col sm:flex-row">
                    <div className='h-100 w-100 sm:w-[50%]  flex flex-col items-center '>
                    <div className='flex justify-center items-center ' >
                            <span class="flex items-center justify-center sm:w-[80px] sm:h-[80px]  w-[60px] h-[60px] sm:text-[60px] text-4xl  font-bold sm:font-extrabold  rounded-full  border-[4px] sm:border-[6px] border-[#007ea3]">
                                3
                            </span>
                            <div className='sm:ml-8 ml-2 lg:text-5xl sm:text-4xl text-3xl font-extrabold mb-2' ref={resultsLeftRef}>
                                <div>Turn Goofs into Gold</div>
                            </div>
                        </div>
                        {/* <img src="/goofs.png" alt="3: Turn Goofs into Gold" className="sm:w-1/2 sm:h-1/2 w-3/4" /> */}
                        <p className="mt-2 sm:w-4/6 w-5/6 text-xl text-center">Got a question wrong? No worries! Our genius algorithm will make sure it haunts you—in the best way possible. In subsequent review sessions we’ll serve up custom quizzes that focus on your weakest spots until you’re an econ ninja</p>
                    </div>

                        <div className={`sm:w-[45%] w-5/6  rounded-3xl  hidden sm:block mt-4 sm:mt-0 sm:fixed sm:top-1/4 sm:right-20 duration-1000 transition-opacity  ${resultsVisible ? "opacity-100":"opacity-0"}`}>
                            <img src='/qresults.png' className='rounded-xl'></img>
                        </div>
                        <div className={`sm:hidden w-5/6  rounded-3xl   mt-4 `}>
                            <img src='/qresults.png' className='rounded-xl'></img>
                        </div>
             
                </div>
            
                <div className='w-11/12'>
                     <div className='w-5/6 tems-center flex justify-center relative top-0'>

                            <img className="w-11/12" src='leg4.png'/>
                            
                        </div>
                </div>
                    

                <div className=' sm:mt-16 mb-20'>
                    <div className="sm:-mt-20 sm:mx-20 flex justify-center items-center flex-col sm:flex-row "  ref={scrollRef}>
                        <div>
                            <video className={`sm:w-[40%] pt-40 sm:ml-20 rounded-2xl w-11/12 h-auto z-30 duration-1000 transition-opacity hidden sm:block opacity-0 ${warriorIsFixed ? "fixed top-11 left-10 ":" absolute left-10 "} ${warriorVisible ? "opacity-100": "opacity-0"}  
                                [mask-image:linear-gradient(to_bottom,rgba(0,0,0,1)_98%,rgba(0,0,0,0)_100%),]
                                
                                [webkit-mask-image:linear-gradient(to_bottom,rgba(0,0,0,1)_50%,rgba(0,0,0,0)_100%)]`} 
                                style={!warriorIsFixed ? { top: `${warriorTop}px` } : {}} 
                                autoPlay={isAutoplay} 
                                loop 
                                muted 
                                ref={stickyRef}
                            >
                                <source src="BlueWarrior.mp4" type="video/webm" />
                            </video>       
                        </div>
                        <div className='flex flex-col items-center sm:mt-10 sm:-ml-28 sm:w-1/2 sm:ml-[40%] z-30'>
                        <div className='flex '>
                            <span class="flex items-center justify-center sm:w-[80px] sm:h-[80px]  w-[60px] h-[60px] sm:text-[60px] text-4xl  font-bold sm:font-extrabold  rounded-full  border-[4px] sm:border-[6px] border-[#007ea3]">
                                4
                            </span>
                            <div className='sm:ml-8 ml-2 lg:text-5xl sm:text-4xl text-3xl font-extrabold mb-2'>
                                <div>Keep going,</div>
                                <div>you Econo-Warrior</div>
                            </div>
                        </div>
                            {/* <img src="/keepGoing.png" alt="4. Keep Going You Econo Warrior" className="sm:w-1/2 sm:h-1/2 w-3/4" /> */}
                            <p className="mt-2  w-5/6 text-xl text-center">The learning never stops, and neither does our algorithm. We’ll keep feeding you personalized practice until you’re ready to crush the AP exam and beyond. Think of it as a never-ending supply of knowledge. You’re welcome.</p>
                        </div>
                        <div className='flex flex-col justify-center ml-4 -mb-8 items-center sm:hidden my-4'>
                        <img src='Econowarrior.png' className='w-5/6'></img>
                        </div>
                    </div>
                </div>

                            
                <div className='w-11/12'>
                
                     <div className='w-5/6 tems-center flex justify-center relative -right-10 z-30'>
               
                            <img className="ml-[70%] -mt-[14%] w-7/12 sm:w-9/12" src='leg5test.png'/>
                            
                        </div>
                </div>
                
            </div>
            <div className='bg-[#2B3D45] w-full'>
            <div className='flex flex-col justify-center items-center sm:w-full mb-12 z-20'>
                    <div className='sm:text-5xl text-2xl text-center sm:mb-10 mb-4 mt-8 text-md'>Sign up to access quizzes, track progress, and more!</div>
                   <div className="sm:mt-12 button flex flex-col !font-light !py-2 !px-6"
                   onClick={handleGetStarted}>
                        <div className='sm:text-4xl text-2xl z-40'>Get Started!</div>
                    </div> 
                    <div className='sm:text-xl text-lg mb-2 sm:mb-0 text-md text-center mt-4 '>It's 100% free and we never send you emails.  </div><div>C'mon, what else are you doing right now?</div>
            </div>
            <div className='text-center text-5xl ] font-bold '>
                OR
            </div>
            <div className='flex flex-col justify-center items-center w-full mt-12 mb-12 z-20 '>
                   <div className='button flex flex-col !font-light !py-2 !px-6'
                   onClick={()=> {
                    dispatch(getAllChapters())
                    navigate('/video-library')
                   }}>
                        <div className='sm:text-4xl text-2xl '>Jump to Videos</div>
                    </div> 

                    <div className='m:text-xl text-lg mt-4'>You can always sign up later</div>
            </div>
            </div>
            <div className='flex w-full items-center justify-center flex-col mt-12'>
                <div className='text-3xl mb-8 text-center'>Building The Future of Economics (One Quirk at a Time)</div>
                <img className='w-1/2 md:w-auto'src='/Worker.png'></img>
                <div className='sm:w-1/2 w-3/4 mt-4 mb-24'>Welcome to the early days of what will soon be the most exciting corner of the internet (or at least we hope). Sure, it’s a work in progress—kind of like that IKEA furniture you swore you’d finish assembling months ago. But don't worry, we're not done building. More videos, quizzes, and mind-blowing econ insights are on the way, along with features so cool they'll make you question why you ever doubted economics could be fun. Stick around—it’s only going to get better. And hey, if you spot a bug or something weird, let’s call it a ‘feature in beta.’</div>
            </div>
        </div>
    )
}