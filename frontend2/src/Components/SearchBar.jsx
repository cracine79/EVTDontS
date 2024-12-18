import { useState } from "react"
import { useDispatch } from "react-redux"
import { searchChapters } from "../Slices/chaptersActions"
import { useNavigate } from "react-router-dom"

export const SearchBar = ({onSearchSubmit}) =>{
    const dispatch = useDispatch()
    const navigate = useNavigate()
    const [searchTerm, setSearchTerm] = useState("")
    const [query, setQuery] = useState("")
    const findIt = async(e) =>{
        const chapters = await searchChapters(searchTerm)
        navigate('/searchresults', {state:{results:chapters, searchTerm:searchTerm}})
        setSearchTerm("")
    }
    return (
        <div className="flex justify-center h-8 w-full">
            <form onSubmit={(e)=>{
                e.preventDefault()
                onSearchSubmit()
                findIt()}} className="flex justify-center h-8 w-full">
            <input className='lg:w-5/6 md:w-2/3 w-3/4 rounded-tl pl-4 rounded-bl border-t border-black
                            border-l border-b'   
                    value={searchTerm}
                    placeholder='Search for Economics Videos Here' 
                    onChange={(e)=>setSearchTerm(e.target.value)}></input>
            <button type='submit' className='bg-slate-400 hover:bg-slate-500 hover:cursor-pointer w-1/12 min-w-12 rounded-tr rounded-br
                                border-black border-r border-t border-b'
                   >Get It!</button>
            </form>
       
        </div>
    )
}