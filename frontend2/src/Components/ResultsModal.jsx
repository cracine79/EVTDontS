import { useSelector, useDispatch } from "react-redux"
import { closeResultsModal } from "../Slices/modalSlice"
import { useState, useEffect, useRef } from "react"
import { FaArrowLeft } from "react-icons/fa6";
export const ResultsModal = ({answers}) => {
    const showModal = useSelector(state=>(state.modal.isResultsOpen))
    let answers1 = useSelector(state=>(state.results))
    
    const questions = useSelector(state=>(state.questions))
    const [answerNumber, setAnswerNumber] = useState(0)
    const wrongAnswers = []
    const modalRef = useRef(null)

    if(Object.values(answers1).length===0){
        answers1 = answers
    }

    useEffect(()=>{
        modalRef.current.scrollTo({
            top:0
        })
        }
    ,[answerNumber])

        console.log('answers', answers1)
    
    
        Object.values(answers1 || {}).forEach((entry) => {
            if (entry.isCorrect === false) {
                wrongAnswers.push(entry);
            }
        });
  
    const dispatch = useDispatch();

    const handleClose = () => {
        dispatch(closeResultsModal())
        setAnswerNumber(0)
    }

    const createComment = (answer, answerId) => {
        if (answer.is_correct === true){
            return(
                <span className='font-bold items-center flex ml-8'>   <FaArrowLeft /> &nbsp; Correct Answer</span>
            )
        }

        if (answerId == wrongAnswers[answerNumber].answerId){
            return(
                <span className='font-bold flex items-center ml-8'>
                <FaArrowLeft />&nbsp;  Your Answer
                </span>
            )
        }
    }

    const appropriateRadio = (answerId) => {
        
        if(answerId == wrongAnswers[answerNumber].answerId){
            return(
                <>
                <input type='radio'  className="opacity-100" disabled checked/>
             </>
            )
        } else {
            return(
            <>
                <input type='radio' className="opacity-100 form-radio cursor-not-allowed" disabled/>
            </>
            )
        }
      
        
    }


    const Answers = () => {
        
        if (wrongAnswers[answerNumber] && questions[wrongAnswers[answerNumber].questionId] && questions[wrongAnswers[answerNumber].questionId].answers) {
          return Object.entries(questions[wrongAnswers[answerNumber].questionId].answers).map(([answerId, answer]) => (
            <div className='my-4 flex' key={answerId}>
                {appropriateRadio(answerId)}
                <div className='ml-4 flex flex-row items-center' >{answer.text}  <span>{createComment(answer, answerId)}</span></div>
            <br />
            </div>
          ));
        } else {
          return <p className='mb-10 text-2xl text-center'>You got 100% on the last quiz.  Get out of here before we make you write the EVTDS Textbook</p>;
        }
      };
    
    const Question = () => {
        const currentAnswer = wrongAnswers[answerNumber];
        
        if (!currentAnswer || currentAnswer.questionId === undefined) {
            return (
                <>
                    
                </>
            );
        }

        if(questions[currentAnswer.questionId]){
                return(
                    <>
                    <div className="flex items-center justify-center">
                        {questions[wrongAnswers[answerNumber].questionId].image_url ? <img className='sm:size-7/12 ' src={questions[wrongAnswers[answerNumber].questionId].image_url}/>:<></>}
                    </div>
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

    const NextButton = ()=>{
        if (answerNumber < wrongAnswers.length - 1){
            return(
                <button className="button"
                onClick={()=>{
                    setAnswerNumber(answerNumber+1)
                    }}>
                    
                    Next Question
                </button>
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
          md:w-5/6
          lg:w-4/6
          xl:w-3/5
          my-6
          mx-auto
          max-h-[95vh]
          lg:h-auto
          md:h-auto
          flex
          justify-center
          items-center
        `}
      >
        <div
        ref={modalRef}
          className={`
            overflow-y-auto
            translate
            max-h-[95vh]
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
        <div className='text-2xl mt-8 ml-8 mr-4 mb-6'>
            <Question />
        </div>
        <div className='ml-8 text-xl'>
            <Answers />
        </div>
        <div className='flex justify-around mb-8 mt-8'>
            <button className="button"
            onClick = {handleClose}>Close Results</button>
            <NextButton />
        </div>
        </div>
        </div>
        </div>
    </>)
}