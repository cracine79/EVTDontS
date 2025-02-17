import { useSelector, useDispatch } from "react-redux"
import { getAllChapters } from "../Slices/chaptersActions"
import { useNavigate, useLocation, Link } from "react-router-dom"
import { useState, useEffect } from "react"



export const VideoLibrary = () => {

    const dispatch = useDispatch()
    const navigate = useNavigate()
    const location = useLocation()
    
    const chapters = useSelector(state=>(state.chapters))
    const currentUserChapters = useSelector(state=>state.userChapters)
    const topics = useSelector((state)=>state.topics)
    
    let chaptersObj = []
    
    chaptersObj = Object.keys(chapters).map((key)=>({
        id: key,
        ...chapters[key]
    }))
    
    const [videoId, setVideoId] = useState(false)
    const [chapterId, setChapterId] = useState(false)
    const [menuOpen, setMenuOpen] = useState(false)
    const selectedChapterVideoUrl = location.state?.videoUrl
    
    useEffect(()=>{
        dispatch(getAllChapters())
    }, [dispatch])
    
    useEffect(()=>{
        if(selectedChapterVideoUrl){
            setVideoId(selectedChapterVideoUrl)
        }
    }, [selectedChapterVideoUrl])
    
    const videoGo = (chapter, type) => {
        setMenuOpen(false)
        if(type==='long'){
            setVideoId(chapter.video_url)
            setChapterId(chapter.id)
        } else {
            setVideoId(false);
        }
    }
    return<>
     <div onClick={()=>setMenuOpen(true)} className='sm:hidden absolute bg-[#D6E6E2] -mt-1 z-10 w-1/2 text-center border-blue-600 border-solid border text-black'> ☰ Video Library</div>
                <div className={`sm:static fixed sm:w-1/5 min-h-[100vh] w-5/6  bg-[#D6E6E2]  z-10 text-sm text-black transform ${
                    menuOpen ? 'translate-x-0' : '-translate-x-full'
                } transition-transform sm:translate-x-0`}>
                    <div className='ml-4'>
                    <div className='sm:hidden mt-2 -mb-4' onClick={()=>{setMenuOpen(false)}}>X Close</div>
                    <div className='text-2xl font-bold text-center mt-4 -ml-8'>Video Library</div>
                    <div className='font-bold mt-2 text-lg'>Unit 1: Intro to Economic Concepts</div>
                    {chaptersObj.slice(0,7).map(chapter=>{
                        return(
                            <div key={chapter.id} onClick = {()=>(setMenuOpen(false))}className='hover:cursor-pointer  hover:text-[#0088A8]'  >
                                <Link to={`/video-library/${chapter.slug}`}  >{chapter.name}</Link>
                            </div>
                        )
                    })}
                    <div className='font-bold mt-2 text-lg'>Unit 2: Supply & Demand</div>
                    {chaptersObj.slice(7, 18).map(chapter=>{
                        return(
                            <div key={chapter.id} onClick = {()=>(setMenuOpen(false))}className='hover:cursor-pointer  hover:text-[#0088A8]'  >
                                <Link to={`/video-library/${chapter.slug}`}  >{chapter.name}</Link>
                            </div>
                        )
                    })}
                    <div className='font-bold mt-2 text-lg'>Unit 3: Elasticities</div>
                       {chaptersObj.slice(18, 24).map(chapter=>{
                        return(
                            <div key={chapter.id} onClick = {()=>(setMenuOpen(false))}className='hover:cursor-pointer  hover:text-[#0088A8]'  >
                                <Link to={`/video-library/${chapter.slug}`}  >{chapter.name}</Link>
                            </div>  
                        )
                    })}

                    <div className='font-bold mt-2 text-lg'>Unit 4: Government Intervention </div>
                    {chaptersObj.slice(24, 26).map(chapter=>{
                        return(
                            <>
                                
                            <div key={chapter.id} onClick = {()=>(setMenuOpen(false))}className='hover:cursor-pointer  hover:text-[#0088A8]'  >
                                <Link to={`/video-library/${chapter.slug}`}  >{chapter.name}</Link>
                            </div>
                              
                            </>
                        )
                    })} 
                    <div className='text-gray-600'>4.3 Price Floors (coming soon!)</div>
                    <div className='text-gray-600'>4.4 Price Ceilings (coming soon!)</div>
                    </div>
                </div>
    </>
}