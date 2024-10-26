import { useState, useEffect } from "react"
export const Tutorial = ({showModal}) => {
    const [modalState, setModalState] = useState(['off', 0])

    useEffect(() => {
        if (showModal) {
          setModalState(['on', 0]); // Show the modal
          localStorage.setItem('hasVisitedDashboard', 'true'); // Set the key
        }
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
                                <p className="mb-4 text-2xl text-center">Welcome to Your User Dashboard!</p>
                                <div>
                                    <p className='mb-4'>Give us a quick second to walk you through the page. We know, we know, you’ve been on a million websites before—you're basically the internet whisperer—but humor us, alright? This isn’t just any page. This is <em>your</em> dashboard, where you can review your progress, videos watched, quiz scores and topic mastery.  Dont worry, no judgment here... okay, maybe just a little. </p>
                              
                                </div>
                                <p classHae = 'mb-4'>And don’t worry, we’ll try to keep the jargon and cringe to a minimum. Ready? Cool, let’s do 
                                       h7mm!</p>
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
                    0 0, /* Move these percentages to change the cutout */
                    85% 0, 
                    85% 300px, 
                    100% 300px, 
                    100% 0, 
                    0 0
                    )`, 
                }}
                >
                </div>
                <div className="absolute top-10 mt-12 left-1/2 z-50 bg-slate-100 z-100  p-4 rounded-md shadow-lg w-1/4 min-w-80">
                                <p className='mb-4'>You can teleport out of this Econo-wasteland to any other part of the site by accessing your user menu.  From here you can go straight to your next task or access all of our captivating videos in one place </p>
                                <p className='mb-4'>You can also visit our quiz generator, which will allow you to hand-craft a quiz by selecting topics</p>
                                <div className='flex justify-around flex-row'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 2])}>Amazing! More!</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700"  onClick={()=>setModalState(['off', 1])}>Boring.  No more. </button>
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
                    0 230px, /* Move these percentages to change the cutout */
                    58% 230px, 
                    58% 470px, 
                    88% 470px, 
                    88% 230px, 
                    0 230px
                    )`, 
                }}
                >
                </div>
                <div className="absolute top-10 mt-48 left-1/4 z-50 bg-slate-100 z-100  p-4 rounded-md shadow-lg w-1/4 min-w-80">
                                <p className='mb-4'>Ah, the mighty Progress Box—your personal cheerleader, telling you what chapter you're currently <i>surviving</i>. Whether you're about to watch another mind-blowing video or dive into a quiz that you totally remember all the answers to, this button is your trusty guide. ust click it, and boom—on to your next step toward total mastery (or at least faking it till you make it)!"</p>
                                <div className='flex justify-around flex-row'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 3])}>Keep it the magic going!</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700"  onClick={()=>setModalState(['off', 0])}>Eh, I'll wing it</button>
                                </div>
                            </div>
            </>}

            {modalState[1]==3 && <>
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
                    2% 100%, 
                    98% 100%, 
                    98% 530px, 
                    0 530px
                    )`, 
                }}
                >
                </div>
                <div className="absolute top-10 mt-48 left-1/3 z-50 bg-slate-100 z-100  p-4 rounded-md shadow-lg w-1/4 min-w-80">
                                <p className='mb-4'>Welcome to your grand master plan... or as we like to call it, 'organized chaos.' Here’s where all your units live, along with a handy tracker to show exactly how much you’ve actually done. Spoiler: It's probably less than you'd like, but hey, progress is progress! </p>
                                <p> Click on your first unit to expand it.</p>
                                <div className='flex justify-around flex-row mt-4'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 4])}>OK, I expanded it</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700"  onClick={()=>setModalState(['off', 1])}>I don't feel like it.  I'm out.</button>
                                </div>
                            </div>
            </>}

            {modalState[1]==4 && <>
                <div
                className="fixed inset-0 bg-black bg-opacity-60 z-40"
                style={{
                    clipPath: `polygon(
                    0 0, 
                    100% 0, 
                    100% 100%, 
                    0 100%, 
                    0 700px, /* Move these percentages to change the cutout */
                    2% 700px, 
                    2% 780px, 
                    98% 780px, 
                    98% 700px, 
                    0 700px
                    )`, 
                }}
                >
                </div>
                <div className="absolute top-36 mt-36 left-1/4 z-50 bg-slate-100 z-100  p-4 rounded-md shadow-lg w-1/3">
                                
                                    <p className='mb-2'>Here’s your chapter breakdown! You’ll see the chapter name (so fancy, right?), whether you’ve watched the video (but no judgment if you want to watch it again, we know they’re that thrilling), and your quiz status with a grade that we promise we’re not judging... much.</p>
                                <div className='flex flex-row items-'>
                                    <div className='flex flex-row items-center mb-4'>
                                    <p> Once you've taken the a quiz, we'll award you with mastery level here, which is our humble attempt to quantify how well you’ve mastered the chapter topics (our algorithm tries its best!).</p>

                                <img src='topicMastery.png' className='w-1/4 object-contain'></img>
                                    </div>
                                   
                                </div>
                                <p className='mb-4'> Need more practice? Just hit the quiz button and show those questions who’s boss!</p>
                                    <div className='flex justify-around flex-row mt-4'>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700" onClick={()=>setModalState(['on', 0])}>I wasn't paying attention. Start over.</button>
                                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700"  onClick={()=>setModalState(['off', 0])}>Enough talk. Let's go.</button>
                                </div>
                            </div>
            </>}

        

       
        </>}
    );
        </>
    )
}