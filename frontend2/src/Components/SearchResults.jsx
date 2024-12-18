import { useLocation, useNavigate } from "react-router-dom"
import { useSelector } from "react-redux"

export const SearchResults = () => {
    const user = useSelector((state)=>state.user)
    const location = useLocation()
    const navigate = useNavigate()

    const search_results = location.state?.results
    const search_term = location.state?.searchTerm
    const searchObj = search_results.chapters

    const goToAllVids = (videoUrl) => {
        navigate('/videoindex', {state:{videoUrl:videoUrl}})
    }
    return(
        <div className='mt-32'>
            <div className='w-full flex items-center flex-col justify-center'>
                <div className='text-2xl mb-8'>Search Results For "{search_term}"</div>
                <div className='w-full flex flex-wrap justify-around'> 
                    {
                        searchObj.map((chapter)=>{
                            return(<div key={chapter.id} className='w-1/4 min-w-72 border border-black flex flex-col h-auto items-center m-4 '>
                                <div className='mt-2 font-bold'>
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
                                    
                                <button className="border-black border hover:cursor-pointer bg-slate-300 hover:bg-slate-500 rounded my-4"
                                        onClick = {()=>goToAllVids(chapter.video_url)}>
                                    Jump to this Video
                                </button>

                                }
                            </div>)
                        })
                    }
                </div>
            </div>
        </div>
    )
}