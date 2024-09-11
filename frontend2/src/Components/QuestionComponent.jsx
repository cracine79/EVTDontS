import { useSelector, useDispatch } from "react-redux"
import { useState, useEffect } from "react";
import { closeQuizModal } from "../Slices/modalSlice";


export const QuestionComponent = () => {
    const showModal = useSelector(state=>(state.modal.isQuizOpen));
    const questions = useSelector(state=>(state.questions))
    const questionsObj = Object.values(questions)
    // console.log(questionsObj)
    const dispatch = useDispatch();
    const [questionNumber, setQuestionNumber] = useState(0)
    const [selectedAnswer,setSelectedAnswer] = useState(null)
    const [submittedAnswers, setSubmittedAnswers] = useState([])
    console.log(submittedAnswers)
    const handleClose = () => {
      dispatch(closeQuizModal())
      setSubmittedAnswers([])
      setQuestionNumber(0)
      setSelectedAnswer(null)
    }

    const handleAnswerSelect = (answerId) => {
      // console.log("Selected answer:", answerId); // Log selected answer to console
      setSelectedAnswer(answerId); // Update state
    };


    const Answers = () => {
      if (questionsObj[questionNumber] && questionsObj[questionNumber].answers) {
        return Object.entries(questionsObj[questionNumber].answers).map(([answerId, answer]) => (
          <>
          <input type='radio'
                  name={`question-${questionNumber}`}
                  id={`answer-${answerId}`} 
                  onChange = {()=>handleAnswerSelect(answerId)}
                  checked={answerId === selectedAnswer} // Check if answer matches
                  value={answerId} // Set value to answerObj.id
          />
         <label htmlFor={`answer-${answerId}`}>{answer.text}</label>
          <br />
          </>
        ));
      } else {
        return <p>No answers available</p>;
      }
    };

    const handleSubmit = () => {

      // console.log( {[questionNumber]:(questionsObj[questionNumber].answers)[selectedAnswer]})
      const answerToSubmit = {[questionNumber]:(questionsObj[questionNumber].answers)[selectedAnswer]}
      setSubmittedAnswers(prevSubmittedAnswers => [...prevSubmittedAnswers, answerToSubmit]);
      setQuestionNumber(prevNumber => prevNumber + 1)
      
      // setSubmittedAnswers(submittedAnswers.append(answerToSubmit))
      // console.log(submittedAnswers)
    }
    

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
            <div className='flex justify-around mt-10'>
              <button onClick = {handleSubmit}>Submit</button>
              <button onClick = {handleClose}>Close</button>          
            </div>
         
      </div>
      </div>
      </div>
      </div>
      )

}