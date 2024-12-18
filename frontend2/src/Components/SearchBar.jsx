import { useState } from "react"
import { useDispatch } from "react-redux"
import { searchChapters } from "../Slices/chaptersActions"
import { useNavigate } from "react-router-dom"

export const SearchBar = () =>{
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const [searchTerm, setSearchTerm] = useState("")
    const findIt = async() =>{
        const chapters = await searchChapters(searchTerm)
        navigate('/searchresults', {state:{results:chapters, searchTerm:searchTerm}})
    }
    return (
        <div className="flex justify-center h-8 w-full">
            <input className='lg:w-5/6 md:w-2/3 w-1/2 rounded-tl pl-4 rounded-bl border-t border-black
                            border-l border-b'   
                    placeholder='Search for Economics Videos Here' 
                    onChange={(e)=>setSearchTerm(e.target.value)}></input>
            <button className='bg-slate-400 hover:bg-slate-500 hover:cursor-pointer w-1/12 min-w-12 rounded-tr rounded-br
                                border-black border-r border-t border-b'
                    onClick = {()=>findIt()}>Get It!</button>
        </div>
    )
}