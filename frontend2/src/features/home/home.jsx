import { useDispatch, useSelector } from "react-redux"
export const Home = () => {
    const user = useSelector((state)=>state.user.user)

      const getIt = async (e)=>{
        e.preventDefault()
        fetch('/api/questions/hello')
            .then(res=>console.log(res))
    }

        const getOne = async(e) => {
            e.preventDefault()
            fetch('/api/questions/hello')
                .then(res=>jsonify(res))
                .then(res=>console.log(res))
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
