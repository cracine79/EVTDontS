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
        if(searchTerm.length > 0){
            const chapters = await searchChapters(searchTerm)
            navigate('/searchresults', {state:{results:chapters, searchTerm:searchTerm}})
            setSearchTerm("")
        }
    }
    return (
        <div className="flex justify-center h-12 w-full">
            <form onSubmit={(e)=>{
                e.preventDefault()
                onSearchSubmit()
                findIt()}} className="flex justify-center h-12 w-full">
            <input className='w-1/2 border-white bg-transparent text-white border-b pl-4 focus:outline-none placeholder-white text-xxs sm:text-sm focus:ring-0'   
                    value={searchTerm}
                    placeholder='Search For Econ Videos Here' 
                    onChange={(e)=>setSearchTerm(e.target.value)}></input>
            <button type='submit' className='bg-transparent hover:cursor-pointer w-1/12 min-w-12 r
                                border-white border-b text-2xl text-white hover:text-[#344A53]'
                   ><i className="fa-solid fa-magnifying-glass"></i></button>
            </form>
       
        </div>
    )
}