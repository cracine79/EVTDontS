import { useNavigate } from "react-router-dom"
export const MessageSent = () => {
    const navigate = useNavigate()
    return (<div className='mt-24 flex flex-col items-center w-full min-h-[75vh]'>
       
        <div className='mt-12 border sm:w-1/2 w-11/12 border-black p-4 rounded-xl flex flex-col items-center'>
            <div className='text-3xl mb-4'>Success!</div>
            <div>
                Your message has been successfully hurled into the digital abyss! Something may or may not emerge on the other side. If you sent us something mean, don’t worry—we’ll absolutely ugly cry about it and possibly start a support group.
            </div>
            <div className='flex sm:w-2/3 w-full justify-around mt-4'>
                <button className='mt-2
                            flex
                            flex-col
                            border-black 
                            h-auto
                            sm:w-1/3
                            w-5/12 
                            border
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-slate-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mb-4'
                            onClick = {()=>navigate('/')}>
                    Back Home
                </button>
                <button className='mt-2
                            w-5/12
                            flex
                            flex-col
                            border-black 
                            h-auto
                            sm:w-1/3 
                            border
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-slate-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer
                            mb-4'
                            onClick = {()=>navigate('/contactus')}>
                    Send Another
                </button>
            </div>
        </div>
       

    </div>)
}