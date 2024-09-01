import { useSelector } from "react-redux"
export const Video = () => {
    const chapters = useSelector((state)=>state.chapters)
    const source = chapters[1].video_url
    return(
        <div className="w-full flex flex-col justify-center items-center">
        <div className='mt-40  aspect-video justify-center w-3/4'>
                
            <iframe className="w-full h-full" src="https://www.youtube.com/embed/mfGKKxwC_fE?controls=1&rel=0" title="1.1 Scarcity, Choice &amp; Opportunity Cost" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
            </div>
            <div>
                Text text text text
            </div>
            <div>
                <div>
                    Mark as Complete
                    (take me to the quiz)
                </div>
            </div>
        </div>
    )
}