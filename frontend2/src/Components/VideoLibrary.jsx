import { useSelector, useDispatch } from "react-redux"
import { getAllChapters } from "../Slices/chaptersActions"
import { useNavigate, useLocation, Link } from "react-router-dom"
import { useState, useEffect } from "react"

// Sidebar headings; chapters are grouped under each by their unit_id
const LIBRARY_UNITS = [
    { id: 1, title: 'Unit 1: Intro to Economic Concepts' },
    { id: 2, title: 'Unit 2: Supply & Demand' },
    { id: 3, title: 'Unit 3: Elasticities' },
    { id: 4, title: 'Unit 4: Government Intervention' },
    { id: 5, title: 'Unit 5: Market Failure' },
    { id: 6, title: 'Unit 6: Production, Costs, Perfect & Imperfect Competition' },
]


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

    const openMenu = () => {
        setMenuOpen(true);
        document.body.style.overflow = 'hidden'

    }

    const closeMenu = () => {
        setMenuOpen(false);
        document.body.style.overflow = 'auto';
    }
    
    return<>
     <div onClick={()=>openMenu()} className='sm:hidden absolute bg-[#D6E6E2] mt-2 z-10 w-1/2 text-center border-blue-600 border-solid border text-black'> ☰ Video Library</div>
                <div className={`sm:static fixed sm:w-1/5 min-h-[100vh] w-5/6  bg-[#D6E6E2]  z-30 text-sm text-black transform ${
                    menuOpen ? 'translate-x-0 overflow-auto h-screen' : '-translate-x-full'
                } transition-transform sm:translate-x-0 `}>
                    <div className='ml-4'>
                    <div className='sm:hidden mt-2 -mb-4' onClick={()=>closeMenu()}>X Close</div>
                    <div className='text-2xl font-bold text-center mt-4 -ml-8'>Video Library</div>
                    {LIBRARY_UNITS.map(unit=>(
                        <div key={unit.id}>
                            <div className='font-bold mt-2 text-lg'>{unit.title}</div>
                            {chaptersObj.filter(chapter=>chapter.unit_id===unit.id).map(chapter=>(
                                <div key={chapter.id} onClick = {()=>closeMenu()} className='hover:cursor-pointer  hover:text-[#0088A8]'  >
                                    <Link to={`/video-library/${chapter.slug}`}  >{chapter.name}</Link>
                                </div>
                            ))}
                        </div>
                    ))}
                    <div className='h-28'></div>
                    </div>
                </div>
    </>
}