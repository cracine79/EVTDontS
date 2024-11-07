import { useSelector, useDispatch } from "react-redux"
import { useState, useEffect } from "react";
import { closeQuizModal } from "../Slices/modalSlice";
import { addResults } from "../Slices/resultsActions";
import { useNavigate } from "react-router-dom";
import { GrChapterAdd } from "react-icons/gr";
import { finishQuiz, finishReviewQuiz } from "../Slices/resultsActions";


export const QuestionComponent = ({chapter, type, topics}) => {
    const navigate = useNavigate();
    const showModal = useSelector(state=>(state.modal.isQuizOpen));
    const questions = useSelector(state=>(state.questions));
    const questionsObj = Object.entries(questions).map(([id, question]) => ({
      ...question,
      id: id
    }))
    const numberOfQuestions = questionsObj.length
  
    const quizChapterName = type == 'chapterQuiz' ? useSelector(state=>(state.chapters[chapter].name)) : "No Name Available"
    const dispatch = useDispatch();
    const [questionNumber, setQuestionNumber] = useState(0)
    const [selectedAnswer,setSelectedAnswer] = useState(null)
    const [submittedAnswers, setSubmittedAnswers] = useState({})
    const [selectAnswerPrompt, setSelectAnswerPrompt] = useState(false)
    const currentChapter = useSelector(state=>(state.user.currentChapter))
    
    const names = topics.map(topic => topic.topic_name)

    const topicQuizName = names.length > 1 
    ? names.slice(0, -1).join (', ') + ' and ' + names[names.length -1]    
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
        [questionId]: { answerId, isCorrect, topicId } // Store both answerId and isCorrect
      }));
    };


    const Answers = () => {
      if (questionsObj[questionNumber] && questionsObj[questionNumber].answers) {
        return Object.entries(questionsObj[questionNumber].answers).map(([answerId, answer]) => (
          <div className='my-2' key={answerId}>
          <input type='radio'
                  name={`question-${questionNumber}`}
                  id={`answer-${answerId}`} 
                  onChange={() => handleAnswerSelect(answerId)} // Update state on change
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


    const handleSubmit = () => {
      const questionId = questionsObj[questionNumber].id;
      const selectedAnswer = submittedAnswers[questionId]; // Grab the stored answer for this question
      const newSubmittedAnswers = {
        ...submittedAnswers,
      };
    
      // Move to the next question or finish the quiz
      if(submittedAnswers[questionId]){
        if (questionNumber < questionsObj.length - 1) {
          setQuestionNumber(prevNumber => prevNumber + 1);
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
            chapter_id: currentChapter,
            quiz_score: percentageScore,
            answers: newSubmittedAnswers
          }
          
          if (type == 'chapterQuiz'){
            console.log('CHAPTPPPTER QUIZ SUBMIT')
            dispatch(finishQuiz(quizData));  // Call dispatch directly with the new state
            dispatch(closeQuizModal());
            setQuestionNumber(0);
            navigate('/results')
          } else if (type == 'topicQuiz'){
            console.log('REVIEWWWW QUIZAA SUBMIT')
            dispatch(finishReviewQuiz(quizData))
            dispatch(closeQuizModal());
            setQuestionNumber(0);
            navigate('/rqresults', {state: {topics, type}})
          } else if (type == 'shortWeakspotQuiz'){
            console.log('WEAKNESS QUIZ SUBMIT', newTopics)
            dispatch(finishReviewQuiz(quizData))
            dispatch(closeQuizModal())
            setQuestionNumber(0);
            console.log('THE MUTHA CHICKEN NEW TOPICS ARE', newTopics)
            navigate('/rqresults', {state: {topics : newTopics, type: type}})
          } else if (type == 'unitQuiz'){
            console.log('unit QUIZ')
            dispatch(finishReviewQuiz(quizData))
            dispatch(closeQuizModal())
            setQuestionNumber(0)
            navigate('/uqresults', {state: {topics: newTopics}})
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
          md:w-5/6
          lg:w-4/6
          xl:w-1/2
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
                <div className='flex flex-col items-center mt-6'>
                  {type=='chapterQuiz' && 
                    <div className="text-3xl px-6">{quizChapterName}  - Chapter Quiz</div>
                  }
                  {type=='topicQuiz' && 
                    <div className="text-3xl px-6">{topicQuizName}  - Topic Quiz</div>
                  }
                
                </div>
                <div className='flex flex-row justify-center mt-4 -mb-4 w-full'>
                  <img src={questionsObj[questionNumber].image_url}/>

                </div>
                <div className="text-2xl mt-8 ml-8 mr-4 mb-6">Question {questionNumber + 1} of {numberOfQuestions}:{questionsObj[questionNumber].text.split('<br>').map((line, index) => (
                      <p key={index}>{line}</p>
                      ))}</div>
                <div className="ml-8 text-xl"><Answers /></div>

              </div>

            ) : (
              <div>No question available</div>
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
                            w-40 
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
              } 
              <button className='
                            border-black 
                            h-1/5 
                            w-40 
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
              <button className='
                            border-black 
                            h-1/5 
                            w-40 
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