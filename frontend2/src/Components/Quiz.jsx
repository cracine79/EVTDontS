import { useSelector, useDispatch } from "react-redux"
import { useLocation } from "react-router-dom"

export const Quiz = () => {

    const location = useLocation()
    const chapter = location.state?.chapter

    return (
        <div className="w-full flex flex-col justify-center items-center">
            <div className='mt-40  aspect-video justify-center w-3/4'>
                This is the page for the quiz for Chapter {chapter}
            </div>
        </div>
      
    )
}