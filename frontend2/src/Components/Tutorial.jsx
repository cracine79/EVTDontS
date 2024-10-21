import { useState, useEffect } from "react"
export const Tutorial = () => {
    const [modalState, setModalState] = useState(['off', 0])

    useEffect(() => {
        const hasVisited = localStorage.getItem('hasVisitedDashboard');
        // if (!hasVisited) {
          setModalState(['on', 0]); // Show the modal
          localStorage.setItem('hasVisitedDashboard', 'true'); // Set the key
        // }
      }, []);

      useEffect(() => {
        if (modalState[0] === 'on') {
          document.body.style.overflow = 'hidden'; // Prevent scrolling
        } else {
          document.body.style.overflow = 'auto'; // Allow scrolling
        }
    
        // Clean up the effect on unmount
        return () => {
          document.body.style.overflow = 'auto'; // Ensure scrolling is enabled on unmount
        };
      }, [modalState]);
    return (
        <>
          return (
        {modalState[0] == 'on' && <>
            {modalState[1]==0 && <>
                <div
                className="fixed inset-0 bg-black bg-opacity-60 z-40 w-full"
              
                >
                </div>
                <div className="absolute  left-1/4 top-56 z-50 w-1/3  bg-slate-100 p-4 rounded-md shadow-lg">
                                <p className="mb-4 text-center">Welcome to Your User Dashboard!</p>
                                <p className='mb-4'>Give us a quick second to walk you through the page. We know, we know, you’ve been on a million websites before—you're basically the internet whisperer—but humor us, alright? This isn’t just any page. This is <em>your</em> dashboard, where you can review your progress, videos watched, quiz scores and topic mastery.  Dont worry, no judgment here... okay, maybe just a little. </p>
                                <p classHae = 'mb-4'>And don’t worry, we’ll try to keep the jargon and cringe to a minimum. Ready? Cool, let’s do this!</p>
                                <div className='flex justify-around flex-row mt-6'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 1])}>Next Stop: Enlightenment</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['off', 1])}>Skip the awkward tour</button>
                                </div>
                            </div>
            </>}
            {modalState[1]==1 && <>
                <div
                className="fixed inset-0 bg-black bg-opacity-60 z-40"
                style={{
                    clipPath: `polygon(
                    0 0, 
                    100% 0, 
                    100% 100%, 
                    0 100%, 
                    0 230px, /* Move these percentages to change the cutout */
                    58% 230px, 
                    58% 450px, 
                    88% 450px, 
                    88% 230px, 
                    0 230px
                    )`, 
                }}
                >
                </div>
                <div className="absolute top-10 mt-48 left-1/3 z-50 bg-slate-100 z-100  p-4 rounded-md shadow-lg w-1/5">
                                <p className='mb-4'>In case you are like Guy Pearce from Memento and you can't remember what you just did - you can find the chapter you are currently working on, as well as access your next assignment here. </p>
                                <div className='flex justify-around flex-row'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 2])}>Keep it Coming!</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700"  onClick={()=>setModalState(['off', 1])}>Get me outta here.</button>
                                </div>
                            </div>
            </>}

            {modalState[1]==2 && <>
                <div
                className="fixed inset-0 bg-black bg-opacity-60 z-40"
                style={{
                    clipPath: `polygon(
                    0 0, 
                    100% 0, 
                    100% 100%, 
                    0 100%, 
                    0 530px, /* Move these percentages to change the cutout */
                    2% 530px, 
                    2% 950px, 
                    98% 950px, 
                    98% 530px, 
                    0 530px
                    )`, 
                }}
                >
                </div>
                <div className="absolute top-10 mt-48 left-1/3 z-50 bg-slate-100 z-100  p-4 rounded-md shadow-lg w-1/5">
                                <p className='mb-4'>All units that you are studying, past, present and future, can be found here.  As you finish videos that don't suck, and complete quizzes, your progress is logged.  Click on your first unit to expand it.</p>
                                <div className='flex justify-around flex-row'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 2])}>OK, I expanded it</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700"  onClick={()=>setModalState(['off', 1])}>I don't feel like it.  I'm out.</button>
                                </div>
                            </div>
            </>}

        

       
        </>}
    );
        </>
    )
}