import { useState } from "react"
export const Tutorial = () => {
    const [modalState, setModalState] = useState(['on', 0])
    return (
        <>
          return (
        {modalState[0] == 'on' && <>
            {/* Dark overlay with a clear cutout */}

<div
  className="fixed inset-0 bg-black bg-opacity-60 z-40"
  style={{
    clipPath: `polygon(
      0 0, 
      100% 0, 
      100% 100%, 
      0 100%, 
      0 230px, /* Move these percentages to change the cutout */
      58% 230px, 
      58% 550px, 
      88% 550px, 
      88% 230px, 
      0 230px
    )`, 
  }}
>
</div>
<div className="absolute top-10 mt-48 left-1/3 z-50 bg-gray-800 z-100 text-white p-4 rounded-md shadow-lg max-w-xs">
                <p className="mb-4">Welcome to your user dashboard page!</p>
                <p className='mb-4'>Your current chapter and next thing to be done that doesn't suck can be accessed here</p>
                <div className='flex justify-around flex-row'>
                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700">Next</button>
                    <button className="bg-blue-500 px-4 py-2 rounded-md text-white hover:bg-blue-700">Skip</button>
                </div>
            </div>

                
                     {/* Highlighted Section */}
            {/* <div className="relative z-60 mx-auto mt-28 w-3/4 p-6 bg-white shadow-2xl rounded-lg">
                <p className="text-gray-800">This is the highlighted section with no custom CSS.</p>
            </div> */}

            {/* Explanation Box */}
        

       
        </>}
    );
        </>
    )
}