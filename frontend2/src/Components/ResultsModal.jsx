import { useSelector, useDispatch } from "react-redux"
import { closeResultsModal } from "../Slices/modalSlice"

export const ResultsModal = () => {
    const showModal = useSelector(state=>(state.modal.isResultsOpen))
    const dispatch = useDispatch();

    const handleClose = () => {
        dispatch(closeResultsModal())
    }

    return(<>
      <div
      className={`
        justify-center
        items-center
        flex
        overflow-x-hidden
        overflow-y-auto
        fixed
        inset-0
        z-50
        outline-none
        focus:outline-none
        bg-neutral-800/70
        ${showModal ? 'translate-y-0 opacity-100' : 'translate-y-full opacity-0'}
      `}
    >
      <div
        className={`
          translate
          relative
          w-full
          md:w-4/6
          lg:w-3/6
          xl:w-2/5
          my-6
          mx-auto
          h-full
          lg:h-auto
          md:h-auto
          flex
          justify-center
          items-center
        `}
      >
        <div
          className={`
            translate
            h-full
            min-h-64
            lg:h-auto
            md:h-auto
            border-0
            rounded-lg
            shadow-lg
            relative
            flex
            flex-col
            w-full
            bg-white
            outline-none
            focus:outline-none
             transition-transform
            duration-300
              
          `}
        >
        MotherFucking Results Modal Bitch
        <button onClick = {handleClose}>Close Results</button>
        </div>
        </div>
        </div>
    </>)
}