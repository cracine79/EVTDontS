
import Image from "next/image";
import { useDispatch, useEffect } from "react-redux";
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
import Link from 'next/link';


export default function Home() {

  return (
    <div className='flex relative flex-col w-screen items-center bg-[#344A53] text-white min-h-[100vh] relative'>
       <div className="flex  justify-center sm:mt-8">   {/*Video for desktop, image for mobile*/}
          <video 
                className=" border-white border border-solid w-full sm:w-11/12 h-auto sm:mt-24 hidden sm:block rounded-3xl z-20" 
                autoPlay 
                loop 
                muted 
                playsInline
              >
                <source src="/intro2.mp4" type="video/mp4" />
           
          </video>
          <img src="/MobileBannerTopReal.jpg" className='mt-20 sm:hidden'></img>
       </div>

       <div className=' w-11/12 sm:text-2xl text-xs flex justify-around text-center sm:px-28 border-white border-2 border-solid rounded-2xl h-20 items-center'>
        <span>Stop memorizing.</span>
          <span>Start understanding.</span>
          <span>Economics, but finally entertaining.</span>
      </div>

      <div className=' bg-[#2B3D45] w-full pt-12 w-full relative flex '>
        <div className='w-full flex justify-start items-center relative flex-col'>
             <div className='flex flex-col items-center justify-center text-center text-xl w-['>
                  <div className='text-5xl mb-8'>Ready to Dive In?</div>
                  <div>Browse our <em>free library</em> of economics videos and quizzes!</div>
                  <div className='py-6'>Think of it as an all-you-can-eat buffet of knowledge—without the regret.</div>
              </div>
              <Link className='button flex flex-col w-[32%] max-w-[450px] h-12 mb-16 !font-light !py-2 !px-6  z-40 ' href="/video-library">
              <div className='sm:text-lg xl:text-2xl'><span className='hidden sm:inline'>Take Me to the </span>Videos & Quizzes!</div>
             </Link>
             <div className='text-xl absolute bottom-0  ml-[17%] p-4 '>Or scroll on to learn how it works!</div>
        </div>
        
      </div>

      <div className='w-5/6 items-center justify-center flex relative'>
            
            <img src='/leg1.png'></img>
            <div className='w-1/3'></div>
      </div>
          <div className='relative'>
            
          <div className='absolute'>

          <video className=" border-white border border-solid w-full sm:w-full h-auto sm:mt-24 hidden sm:block rounded-3xl z-20" 
                autoPlay 
                loop 
                muted 
                playsInline>
            <source src="/sample.mp4" type="video/mp4" />
          </video>
          </div>
        </div>

  


    </div>
  );
}

