import { useState } from "react"
import { useSelector } from "react-redux"
export const VideoIndex = () => {
    const chapters = useSelector(state=>(state.chapters))
    const chaptersObj = Object.values(chapters)
  
    const [videoId, setVideoId] = useState(false)

    const videoGo = (videoUrl) => {
        setVideoId(videoUrl)
    }

    const chapterVid = (videoId) => {
        const chapter = chaptersObj.find(chapter=>chapter.video_url === videoId)
        return chapter.name
    }
    return(
        <div className = 'mt-24'>

            <div className='h-screen w-100 flex'>
                <div className='h-full w-1/4 bg-lime-100'>
                    <div>Video Library</div>
                    {chaptersObj.map(chapter=>{
                        return(
                            <div className='hover:cursor-pointer' onClick={()=>videoGo(chapter.video_url)}>{chapter.name}</div>
                        )
                    })}
                </div>
                <div className='w-5/6'>
                    <div className='text-center mt-10 text-5xl font-bold'>
                    Welcome to the Video Cache!
                    </div>
                    <div className='mx-8 mt-10 text-lg'>
                        You can access any and all of our treasure trove of videos that absolutely don't suck from the navigation bar on the left. 
                    </div>
                    <div className='mx-8 mt-4 text-lg'>
                    Choose wisely, and don't be like the Nazi guy in the end of Indiana Jones & The Last Crusade!
                    </div>
                    <div className='flex flex-col items-center justify-center mt-10 border'>
                        <div className='text-3xl my-4'>
                            {videoId ? `Video for ${chapterVid(videoId)}`: 'Choose a video already!'}
                        </div>
                        {videoId && (
                        <>
                        <div>
                            <iframe 
                                width="920" 
                                height="540" 
                                src={videoId} 
                                allowFullScreen>
                            </iframe>
                        </div>
                        <div className='my-8 border py-4 px-2 bg-slate-400 border-black rounded-xl hover:bg-slate-600 hover:cursor-pointer'>
                            Jump to Chapter Quiz
                        </div>
                        </>
                        )}
                    </div>
                </div>

            
                    
            </div>
        
        </div>
    )
}