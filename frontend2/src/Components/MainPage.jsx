import LogoutButton from "./LogoutComponent"

export const MainPage = () => {
    return(
        <>
            <div className="flex mt">
                {/* <div className="font-serif text-5xl w-1/2 ">
                    Learning economics doesn't have to suck...   But it usually does. 
                </div> */}
                <video autoPlay loop muted>
                    <source src="Intro.mp4" type="video/mp4" />
                </video>
            </div>
            <div className="w-screen h-auto bg-gray-50">
                <div className="mt-20 ml-20 flex justify-around items-center">
                    <div className='h-100 w-100 flex flex-col items-center'>
                        <img src="/Watch.png" alt="Watch the Videos" className="w-4/6 h-4/6" />
                        <p className="mt-2 w-4/6 text-2xl text-center">Seriously, they don’t. We’ve edited out all the parts that flopped, so all you need to do is kick back, press play, and maybe even laugh while learning. (We said maybe.)</p>
                    </div>
                    <div className="flex flex-col items-center">
                        <video autoPlay loop muted className="w-5/6 rounded-3xl">
                            <source src="Sample.mp4" type="video/mp4" />
                        </video>
                    </div>
                </div>

                <div>
                    <div className="mt-40 ml-20 flex justify-around items-center">
                        <div className='w-5/6 mt-20'>

                        </div>
                        <div className='h-100 w-100 flex flex-col items-center'>
                            <img src="/Practice.png" alt="Take the Quizzes" className="w-4/6 h-4/6" />
                            <p className="mt-2 w-4/6 text-2xl text-center">Unlike lots of resources, our practice quizzes DON'T suck.  Nope, these bad boys are almost identical to the AP questions you’ll face on game day.  Why waste time practicing with the wrong tools when you can sharpen your skills with the real deal?</p>
                        </div>
                    </div>
                </div>
          

                <div className="mt-20 ml-20 flex justify-around items-center">
                    <div className='h-100 w-100 flex flex-col items-center'>
                        <img src="/goofs.png" alt="Watch the Videos" className="w-4/6 h-4/6" />
                        <p className="mt-2 w-4/6 text-2xl text-center">Got a question wrong? No worries! Our genius algorithm will make sure it haunts you—in the best way possible. In subsequent review sessions we’ll serve up custom quizzes that focus on your weakest spots until you’re an econ ninja.</p>
                    </div>
                    <div className="w-5/6 flex flex-col items-center">
                        <div className="w-5/6  rounded-3xl">
                           
                        </div>
                    </div>
                </div>

                <div>
                    <div className="mt-40 ml-20 flex justify-around items-center">
                        <div className='w-5/6 mt-20'>

                        </div>
                        <div className='h-100 w-100 flex flex-col items-center'>
                            <img src="/keepGoing.png" alt="Take the Quizzes" className="w-4/6 h-4/6" />
                            <p className="mt-2 w-4/6 text-2xl text-center">The learning never stops, and neither does our algorithm. We’ll keep feeding you personalized practice until you’re ready to crush the AP exam and beyond. Think of it as a never-ending supply of knowledge. You’re welcome.</p>
                        </div>
                    </div>
                </div>
          
            </div>
        </>
    )
}