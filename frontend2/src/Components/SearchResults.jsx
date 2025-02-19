import { useLocation, useNavigate } from "react-router-dom"
import { useSelector, useDispatch } from "react-redux"
import { getAllChapters } from "../Slices/chaptersActions"

export const SearchResults = () => {
    const dispatch = useDispatch()
    const user = useSelector((state)=>state.user)
    const location = useLocation()
    const navigate = useNavigate()

    const search_results = location.state?.results
    const search_term = location.state?.searchTerm
    const searchObj = search_results.chapters
    console.log(searchObj)
    const goToAllVids = async(chapter) => {
        await dispatch(getAllChapters())
        navigate(`/video-library/${chapter.slug}`, {state:{chapter}})
    }

    const goToThisVid = ( (chapterId) => {
        navigate(`/video/${chapterId}`)
    })
    return(
        <div className='mt-60'>
            <div className='w-full flex items-center flex-col  min-h-[75vh] '>
                <div className='text-2xl mb-8'>Search Results For "{search_term}"</div>
                <div className='w-full flex flex-wrap justify-around'> 
                    {
                        searchObj.map((chapter)=>{
                            return(<div key={chapter.id} className='sm:w-1/4 min-w-72 border border-slate-200 px-2 shadow-xl flex flex-col h-auto items-center m-4 rounded '>
                                <div className='my-4 text-lg text-center font-bold'>
                                {chapter.name}
                                </div>
                                <div className="w-full min-w-72 relative" style={{paddingBottom: '56.25%'}}> {/* Aspect Ratio 16:9 */}
                                    <iframe className="absolute top-0 left-0 w-full h-full" 
                                            src={`${chapter.video_url}?modestbranding=1&rel=0&controls=1&autohide=1`}
                                            title="title" 
                                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                                            referrerPolicy="strict-origin-when-cross-origin" 
                                            allowFullScreen>
                                    </iframe>
                                </div>
                                { !user.username && 
                                    
                                <button className="button py-2 my-4"
                                        onClick = {()=>goToAllVids(chapter)}>
                                    Jump to this Video
                                </button>

                                }
                                { user.username && 
                                    
                                    <button className="border-black border hover:cursor-pointer bg-slate-300 hover:bg-slate-500 rounded my-4"
                                            onClick = {()=>goToThisVid(chapter.id)}>
                                        Jump to this Video
                                    </button>
    
                                    }
                            </div>)
                        })
                    }
                </div>
  
                {
                    searchObj.length == 0 && <div className='sm:w-1/3 w-11/12'>
                       <div className='text-xl mb-2 font-bold text-center'>Whoops!  Looks like we don't have a video for that search yet!</div>  
                       <img src='https://evtds-seeds.s3.us-east-2.amazonaws.com/IslandNight.png'></img>
                        <div className='mt-8 my-8'>We blame the economics gods for not blessing us with one yet. But hey, if you reach out to us (and it's actually about economics, not like that time you searched for "cooking with Keynes"), we'll see what we can do. No promises, though... the gods are a tough crowd.</div>
                    </div>
                }
            </div>
        </div>
    )
}