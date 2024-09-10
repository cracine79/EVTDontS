import { useSelector, useDispatch } from "react-redux"
import { useState, useEffect } from "react";
import { closeQuizModal } from "../Slices/modalSlice";


export const QuestionComponent = () => {
    const showModal = useSelector(state=>(state.modal.isQuizOpen));
    const questions = useSelector(state=>(state.questions))
    const questionsObj = Object.values(questions)
    console.log(questionsObj)
    const dispatch = useDispatch();
    const [questionNumber, setQuestionNumber] = useState(0)
    const handleClose = () => {
      dispatch(closeQuizModal())
    }

    const Answers = () => {
      if (questionsObj[questionNumber] && questionsObj[questionNumber].answers) {
        return Object.values(questionsObj[questionNumber].answers).map((answer, index) => (
          <>
          <input type='radio'
                  name={`question-${questionNumber}`}
                  id={`answer-${index}`} 
          />
         <label htmlFor={`answer-${index}`}>{answer.text}</label>
          <br />
          </>
        ));
      } else {
        return <p>No answers available</p>;
      }
    };
    

    return(
      <div >

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
            {questionsObj[questionNumber] ? (
              <div>
                <div>{questionsObj[questionNumber].text}</div>
                <div><Answers /></div>

              </div>

            ) : (
              <div>No question available</div>
            )}

            <button onClick = {handleClose}>Close</button>          
         
      </div>
      </div>
      </div>
      </div>
      )

}