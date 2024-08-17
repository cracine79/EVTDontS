import { useDispatch, useSelector } from "react-redux"
import csrfFetch from "../session/csrf"
export const Home = () => {
    const user = useSelector((state)=>state.user.user)

      const getIt = async (e)=>{
        e.preventDefault()
        fetch('/api/questions/hello')
                .then(response=>{
                    if(!response.ok){
                        throw new Error("oops")
                    }
                    return response.json();
                })
                .then(data=>{
                    console.log(data)
                })
    }

        const getOne = (e) => {
            e.preventDefault()
            csrfFetch('/api/questions/hello')
                .then(response=>{
                    if(!response.ok){
                        throw new Error("oops")
                    }
                    return response.json();
                })
                .then(data=>{
                    console.log(data)
                })
                
        }
    return (
        <>
             <h1 className="text-3xl text-orange-800">
             Hello from home!! Dude I love it
             </h1>

             <form>
                <p>Hello {user} </p>
                <p>Username</p>
                <input type='text' className='border-black border'></input>
                <p className='text-lg text-orange-800'>Password</p>
                <input type='text' className='border-black border'></input>
                <input type='submit' onClick={getIt}/>
                <input type='submit' onClick={getOne}/>
            </form>
          
        </>
    )
}
