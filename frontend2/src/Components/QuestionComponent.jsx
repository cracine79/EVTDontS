import { useSelector, useDispatch } from "react-redux"
import { useState, useEffect, useRef } from "react";
import { closeQuizModal } from "../Slices/modalSlice";
import { addResults } from "../Slices/resultsActions";
import { useNavigate, useLocation } from "react-router-dom";
import { GrChapterAdd } from "react-icons/gr";
import { finishQuiz, finishReviewQuiz } from "../Slices/resultsActions";


export const QuestionComponent = ({chapter, type, topics}) => {
    const modalContentRef = useRef(null)
    const navigate = useNavigate();
    const showModal = useSelector(state=>(state.modal.isQuizOpen));
    const questions = useSelector(state=>(state.questions));



  
    const location = useLocation()

    const lastUnitId = location.state?.currentUnitId
    const quizChapterName = type == 'chapterQuiz' ? useSelector(state=>(state.chapters[chapter].name)) : "No Name Available"
    const dispatch = useDispatch();
    const [questionNumber, setQuestionNumber] = useState(0)
    const [selectedAnswer,setSelectedAnswer] = useState(null)
    const [submittedAnswers, setSubmittedAnswers] = useState({})
    const [selectAnswerPrompt, setSelectAnswerPrompt] = useState(false)
    const [questionsObj, setQuestionsObj] = useState([])
    const currentChapterId = useSelector(state=>(state.user.currentChapter))
    const userlessChapterId = chapter
    const currentChapter = useSelector(state=>state.chapters[currentChapterId])
    const unitQuizUnitId = location.state?.unit
    const currentUnitId = currentChapter ? currentChapter.unit_id : 2

    const shuffleArray = (array) => {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Swap elements
      }
    };

    useEffect(() => {
      const origQuestionsObj = Object.entries(questions).map(([id, question]) => ({
        ...question,
        id: id
      }));
      shuffleArray(origQuestionsObj);
      setQuestionsObj(origQuestionsObj);
    }, [questions]);  // Dependency array ensures shuffle runs when questions change or the page is visited again
  
    
    const numberOfQuestions = questionsObj.length
    
    const names = topics.map(topic => topic.topic_name)

    const topicQuizName = names.length > 3 
    ? names.slice(0, 3).join (', ') + ', and ' + (names.length - 3).toString() + ' more topics'   
    : names.length > 1
    ? names.slice(0,2).join(', ') + ', and ' + names[names.length-1]
    : names[0]
    const newTopics = []

    if (type == 'shortWeakspotQuiz' || type == 'longWeakspotQuiz' || type == 'unitQuiz'){

      const quizTopicIds = [...new Set(questionsObj.map(question=>question.topic_id))]
      const userProg = useSelector((state)=>state.topicProg)
      const topics = useSelector((state)=>state.topics)
      const userTopicProg = {}
      quizTopicIds.forEach((id)=>{
        userTopicProg[id]={
          ...userProg[id],
          ...topics[id],
          topic_id: id
        }
      })
      const userTopicEntries = Object.values(userTopicProg)

      userTopicEntries.forEach((entry)=>{newTopics.push(entry)})
    }

    const handleClose = () => {
      dispatch(closeQuizModal())
      setSubmittedAnswers([])
      setQuestionNumber(0)
      setSelectedAnswer(null)
    }

    const handleAnswerSelect = (answerId) => {
      const questionId = questionsObj[questionNumber].id;
      const selectedAnswerObj = questionsObj[questionNumber].answers[answerId];
      const isCorrect = selectedAnswerObj.is_correct;
      const topicId = questionsObj[questionNumber].topic_id

      // Update submittedAnswers immediately with answerId and isCorrect
      setSubmittedAnswers(prevSubmittedAnswers => ({
        ...prevSubmittedAnswers,
        [questionId]: { questionId, answerId, isCorrect, topicId } // Store both answerId and isCorrect
      }));
    };


    const Answers = () => {
      if (questionsObj[questionNumber] && questionsObj[questionNumber].answers) {
        return Object.entries(questionsObj[questionNumber].answers).map(([answerId, answer]) => (
          <div className='my-2' key={answerId}>
          <input type='radio'
                  name={`question-${questionNumber}`}
                  id={`answer-${answerId}`} 
                  onChange={() => handleAnswerSelect(answerId)} 
                  checked={submittedAnswers[questionsObj[questionNumber].id]?.answerId === answerId} // Pre-select the answer if it's in submittedAnswers
                  value={answerId} // Set value to answerObj.id
          />
         <label className='ml-4' htmlFor={`answer-${answerId}`}>{answer.text}</label>
          <br />
          </div>
        ));
      } else {
        return <p>No answers available</p>;
      }
    };

    const previousQuestion = () => {
      setSelectAnswerPrompt(false)
      setQuestionNumber(prevNumber => prevNumber -1)
    }


    const handleSubmit = async() => {
      const questionId = questionsObj[questionNumber].id;
      const selectedAnswer = submittedAnswers[questionId]; // Grab the stored answer for this question
      const newSubmittedAnswers = {
        ...submittedAnswers,
      };


    
      // Move to the next question or finish the quiz
      if(submittedAnswers[questionId]){
        if (questionNumber < questionsObj.length - 1) {
          setQuestionNumber(prevNumber => prevNumber + 1);
          if (modalContentRef.current) {
            modalContentRef.current.scrollTo({
              top: 0,
              behavior: 'smooth', // Smooth scrolling animation
            });
          }
        } else {
          
          let numCorrect=0
          const answersObj = Object.values(newSubmittedAnswers)
          answersObj.forEach((result)=>{
            if(result.isCorrect == true){
              numCorrect +=1
            }
          })
          const percentageScore = Math.floor((numCorrect/answersObj.length)*100)
          
          const quizData = {
            chapter_id: currentChapterId,
            quiz_score: percentageScore,
            answers: newSubmittedAnswers
          }
          const otherQuizData = {
            chapter_id: chapter,
            quiz_score: percentageScore,
            answers: newSubmittedAnswers
          }
          
          if (type == 'chapterQuiz'){
            const unitFinished = await dispatch(finishQuiz(quizData));  
      
            dispatch(closeQuizModal());
            setQuestionNumber(0);
            navigate('/results', {state: {unitFinished}})
          } else if (type == 'topicQuiz'){
            dispatch(finishReviewQuiz(quizData))
            dispatch(closeQuizModal());
            setQuestionNumber(0);
            navigate('/rqresults', {state: {topics, type}})
          } else if (type == 'shortWeakspotQuiz'){
            dispatch(finishReviewQuiz(quizData))
            dispatch(closeQuizModal())
            setQuestionNumber(0);
            navigate('/rqresults', {state: {topics : newTopics, type: type}})
          } else if (type == 'unitQuiz'){
            dispatch(finishReviewQuiz(quizData))
            dispatch(closeQuizModal())
            setQuestionNumber(0)
            navigate('/uqresults', {state: {topics: newTopics, unitId: unitQuizUnitId}})
          } else if (type == 'chapterQuizNoUser'){
            dispatch(closeQuizModal())
            setQuestionNumber(0)
            navigate('/userlessresults', {state: {otherQuizData}})
          }
          
        }
        setSelectAnswerPrompt(false)
      } else {
        setSelectAnswerPrompt(true)
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
        
        fixed
        inset-0
        z-50
        outline-none
        focus:outline-none
        bg-slate-200
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
          xl:w-1/2
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
          ref={modalContentRef} 
          className={`
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
            overflow-y-auto
              
          `}
        >
            {questionsObj[questionNumber] ? (
              <div className=' h-full'>
                <div className='flex flex-col items-center mt-6'>
                  {type=='chapterQuiz' && 
                    <div className="text-3xl px-6">{quizChapterName}  - Chapter Quiz</div>
                  }
                  {type=='topicQuiz' && 
                    <div className='flex flex-col items-center'>
                      <div className='text-4xl mb-2'>Topic Quiz for:</div>
                    <div className="text-2xl px-6 text-center">{topicQuizName} </div>
                    </div>
                  }
                  {
                    type=='shortWeakspotQuiz' &&
                    <div className='flex flex-col items-center'>
                      <div className='text-4xl'>Gauntlet Quiz - Take on your Weaknesses!</div>
                    </div>
                  }
                
                </div>
                <div className='flex flex-row justify-center mt-4 -mb-4 h-full'>
                  {questionsObj[questionNumber].image_url && <img className='sm:size-7/12' src={questionsObj[questionNumber].image_url}/>}
                </div>
                <div className="text-2xl mt-8 ml-8 mr-4 mb-6">Question {questionNumber + 1} of {numberOfQuestions}:{questionsObj[questionNumber].text.split('<br>').map((line, index) => (
                      <p key={index}>{line}</p>
                      ))}</div>
                <div className="ml-8 text-xl"><Answers /></div>

              </div>

            ) : (
              type=='shortWeakspotQuiz' ? 
              <div className='mt-8 mx-6'>
                <div className='text-center text-2xl mb-4'>Dude, you're too green!</div>
                <div >Looks like you need to go take some quizzes before we have enough data to judge your weak spots.  Go take some quizzes, flail around in the dark a bit like Shroedinger's cat, and come back when you're battle tested.</div>
              </div> :
              <>
                <div>Oops!  Question Not available</div>
              </>
            )}
            {
              selectAnswerPrompt &&
              <div className='ml-12 -mb-6 text-red-500 font-bold'>
                Please select an answer
              </div>
            }
            <div className='flex justify-around mt-10 mb-10'>
           
            {questionNumber >= 1 ?
            <button className='
                            border-black 
                            h-1/5 
                            sm:w-40
                            w-1/4 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer'
                      onClick={previousQuestion}>
                              
              Previous Question
                            </button> :
              <div className='w-40'></div>
              } { questionsObj[questionNumber] &&
              <button className='
                            border-black 
                            h-1/5 
                            sm:w-40 
                            w-1/4
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer'
                            onClick = {handleSubmit}>{questionNumber < numberOfQuestions - 1 ? <>Next Question</>:<>Submit Quiz</>}</button>
                          }
              <button className='
                            border-black 
                            sm:h-1/5
                            w-1/4 
                            sm:w-40 
                            border-2 
                            flex 
                            justify-center 
                            items-center
                            rounded-lg
                            bg-stone-300
                            hover:bg-slate-500
                            font-medium
                            hover:cursor-pointer'
                            onClick = {handleClose}>Close</button>          

            </div>
    
      </div>
      </div>
      </div>
      </div>
      )

}