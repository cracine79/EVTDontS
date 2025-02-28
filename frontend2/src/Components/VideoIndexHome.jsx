export const VideoIndexHome = () => {
    return(<>
     <div className='sm:w-5/6 w-full mb-6'>
                    <div className='flex flex-col items-center'>
                    
                            <div className='text-center sm:mt-6 mt-10 text-4xl font-bold'>
                        Welcome to the Video Cache!
                        </div>
                        <img className='max-h-[50vh] rounded-2xl 'src='https://evtds-seeds.s3.us-east-2.amazonaws.com/ChooseWiselyCartoon_1.png'></img>
                        <div className="sm:w-[80%]">
                        <div className='mx-8 mt-4 text-lg'>
                        Welcome to the ultimate treasure trove of economics videos! Here, you'll find everything you need to navigate the wild world of supply, demand, 
                            and opportunity cost—with just the right amount of bad animation and obscure movie references to keep things interesting. Each video is a 
                            stepping stone to mastering economic concepts, and you can access any and all of our goldmine Videos that absolutely don't suck 
                            <span className='inline sm:hidden'> by accessing the <span className='font-bold'>Video Library</span> above.</span> 
                            <span className='hidden sm:inline'> from the menu on the left.</span>
                            
                        </div>
                        <div className='mx-8 mt-4 text-lg'>After watching the video you can also try a practice quiz to test your economic skills.</div>
                        <div className='mx-8 mt-4 text-lg'>
                        Choose wisely—unlike that guy in Indiana Jones and the Last Crusade. You know, the one who didn’t. Your economics journey depends on it.
                        </div>
                        </div>
                        
                        
                    </div>
    </div>
    </>)
}