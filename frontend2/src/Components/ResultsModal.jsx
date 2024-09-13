import { useSelector, useDispatch } from "react-redux"
import { closeResultsModal } from "../Slices/modalSlice"
import { useState } from "react"
import { FaArrowLeft } from "react-icons/fa6";

export const ResultsModal = () => {
    const showModal = useSelector(state=>(state.modal.isResultsOpen))
    const answers = useSelector(state=>(state.results))
    const questions = useSelector(state=>(state.questions))
    const [answerNumber, setAnswerNumber] = useState(0)
    const wrongAnswers = []

    console.log(answers)

   Object.values(answers).forEach((entry)=>{
       
        if (entry.isCorrect == false){
            wrongAnswers.push(entry)        }
    })
    console.log('wronganswers are ', {wrongAnswers})

    const dispatch = useDispatch();

    const handleClose = () => {
        dispatch(closeResultsModal())
    }

    const createComment = (answer, answerId) => {
        if (answer.is_correct === true){
            return(
                <span className='font-bold items-center flex ml-8'>   <FaArrowLeft /> Correct Answer</span>
            )
        }

        if (answerId == wrongAnswers[answerNumber].answerId){
            return(
                <span className='font-bold flex items-center ml-8'>
                <FaArrowLeft /> Your Answer
                </span>
            )
        }
    }


    const Answers = () => {
        
        if (wrongAnswers[answerNumber] && questions[wrongAnswers[answerNumber].questionId] && questions[wrongAnswers[answerNumber].questionId].answers) {
          return Object.entries(questions[wrongAnswers[answerNumber].questionId].answers).map(([answerId, answer]) => (
            <div className='my-2' key={answerId}>
    
                <div className='ml-4 flex flex-row items-center' >{answer.text}  <span>{createComment(answer, answerId)}</span></div>
        
            <br />
            </div>
          ));
        } else {
          return <p>No answers available</p>;
        }
      };
    
    const Question = () => {
        const currentAnswer = wrongAnswers[answerNumber];
        
        if (!currentAnswer || currentAnswer.questionId === undefined) {
            return (
                <>
                    Loading...
                </>
            );
        }

        if(questions[currentAnswer.questionId]){
                return(
                    <>
                    {questions[wrongAnswers[answerNumber].questionId].text}
                    </>
                )
        } else {
            return (
                <>
                 Oops, Question unavailable!
                </>
            )
        }
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
        <Question />
        
        <Answers />
        
        <button onClick = {handleClose}>Close Results</button>
        </div>
        </div>
        </div>
    </>)
}