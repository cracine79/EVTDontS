import { useSelector } from "react-redux"
export const UserHome = () => {
    const userName = useSelector((state)=>state.user.username)
    return(
        <div className='mt-40'>
            Hello there {userName}
        </div>
    )
}