import { useSelector, useDispatch } from "react-redux"
import { useState, useEffect, useRef } from "react";
import { closeQuizModal } from "../Slices/modalSlice";
import { useNavigate, useLocation } from "react-router-dom";
import { finishQuiz, finishReviewQuiz } from "../Slices/resultsActions";
import { unitStyle } from "./ui";
import { QuestionFigure } from "./QuestionFigure";


export const QuestionComponent = ({chapter, type, topics}) => {
    const modalContentRef = useRef(null)
    const navigate = useNavigate();
    const showModal = useSelector(state=>(state.modal.isQuizOpen));
    const questions = useSelector(state=>(state.questions));



  
    const location = useLocation()

    const quizChapter = useSelector(state=>(state.chapters[chapter]))
    const quizChapterName = quizChapter?.name || ''
    const quizUnit = useSelector(state=>(quizChapter ? state.units[quizChapter.unit_id] : null))
    const dispatch = useDispatch();
    const [questionNumber, setQuestionNumber] = useState(0)
    const [submittedAnswers, setSubmittedAnswers] = useState({})
    const [selectAnswerPrompt, setSelectAnswerPrompt] = useState(false)
    const [questionsObj, setQuestionsObj] = useState([])
    const currentChapterId = useSelector(state=>(state.user.currentChapter))
    const unitQuizUnitId = location.state?.unit

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

    const topicQuizName = names.length == 4 
    ? names.slice(0, 3).join (', ') + ', and one more topic'
    : names.length > 4
    ? names.slice(0, 3).join (', ') + ', and ' + (names.length - 3).toString() + ' more topics'
    : names.length > 1
    ? names.slice(0,names.length -1 ).join(', ') + ', and ' + names[names.length-1]
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


    const LETTERS = 'ABCDEFGHIJ'
    const Answers = () => {
      const question = questionsObj[questionNumber]
      if (!question || !question.answers) return <p>No answers available</p>
      return (
        <div className="space-y-3" role="radiogroup">
          {Object.entries(question.answers).map(([answerId, answer], i) => {
            const selected = submittedAnswers[question.id]?.answerId === answerId
            return (
              <label key={answerId} htmlFor={`answer-${answerId}`} className="block cursor-pointer">
                <input type="radio" className="sr-only"
                  name={`question-${questionNumber}`}
                  id={`answer-${answerId}`}
                  onChange={() => { setSelectAnswerPrompt(false); handleAnswerSelect(answerId) }}
                  checked={selected}
                  value={answerId} />
                <span className={`flex items-center gap-4 rounded-2xl border-2 px-4 py-3 transition ${selected ? 'border-[#FFC93C] bg-[#FFC93C]/15' : 'border-white/15 hover:border-white/40'}`}>
                  <span className={`w-9 h-9 shrink-0 rounded-full border-2 flex items-center justify-center font-extrabold ${selected ? 'bg-[#FFC93C] border-[#FFC93C] text-[#111]' : 'border-white/40'}`}>{LETTERS[i]}</span>
                  <span>{answer.text}</span>
                </span>
              </label>
            )
          })}
        </div>
      )
    };

    const previousQuestion = () => {
      setSelectAnswerPrompt(false)
      setQuestionNumber(prevNumber => prevNumber -1)
    }


    const handleSubmit = async() => {
      const questionId = questionsObj[questionNumber].id;
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
            // The chapter this quiz is for (not necessarily the student's current "up next" chapter)
            chapter_id: type == 'chapterQuiz' ? Number(chapter) : currentChapterId,
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
            navigate('/results', {state: {unitFinished, chapterId: Number(chapter)}})
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

    const quizTitle = () => {
      if (type == 'chapterQuiz' || type == 'chapterQuizNoUser') return <>{quizChapterName} · Chapter quiz</>
      if (type == 'topicQuiz') return <>Topic quiz: {topicQuizName}</>
      if (type == 'shortWeakspotQuiz') return <>The Gauntlet: take on your weaknesses</>
      if (type == 'unitQuiz') return <>Unit quiz</>
      return null
    }
    const question = questionsObj[questionNumber]

    if (!showModal) return null

    // Full-screen "focus mode": covers the nav and footer while the student answers
    return (
      <div ref={modalContentRef} className="fixed inset-0 z-[60] overflow-y-auto bg-[#344A53] text-white" style={unitStyle(quizUnit)}>
        <div className="max-w-3xl mx-auto px-5 sm:px-8 pt-8 sm:pt-12 pb-16">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-2 min-w-0">
              {quizUnit && <span className="text-xs font-extrabold px-2 py-0.5 rounded unit-bg shrink-0">UNIT {quizUnit.number}</span>}
              <span className="font-bold truncate">{quizTitle()}</span>
            </div>
            <button type="button" onClick={handleClose} className="text-sm text-gray-300 hover:text-white whitespace-nowrap">
              <i className="fa-solid fa-xmark mr-1"></i>Quit
            </button>
          </div>

          {question ? (
            <>
              <div className="mt-4" aria-hidden="true">
                <div className="flex gap-1.5">
                  {questionsObj.map((q, i) => (
                    <span key={q.id} className={`h-2 flex-1 rounded-full ${
                      i === questionNumber ? 'bg-white ring-2 ring-[#FFC93C]'
                      : submittedAnswers[q.id] ? 'bg-[#FFC93C]' : 'bg-[#2B3D45]'}`}></span>
                  ))}
                </div>
              </div>
              <p className="mt-2 text-sm text-gray-300">Question <b className="text-white">{questionNumber + 1}</b> of {numberOfQuestions}</p>

              <section className="mt-6 panel rounded-3xl p-6 sm:p-8">
                <QuestionFigure question={question} className="mx-auto max-w-md mb-6" />
                <h1 className="text-xl sm:text-2xl font-bold leading-snug">
                  {question.text.split('<br>').map((line, index) => <span key={index} className="block">{line}</span>)}
                </h1>
                <div className="mt-6"><Answers /></div>
              </section>

              {selectAnswerPrompt && <p className="mt-4 font-bold text-[#FF6FAE]" role="alert">Pick an answer first.</p>}

              <div className="mt-6 flex items-center justify-between gap-3">
                {questionNumber >= 1
                  ? <button type="button" className="btn-secondary px-5 py-2" onClick={previousQuestion}><i className="fa-solid fa-arrow-left"></i> Back</button>
                  : <span></span>}
                <button type="button" className="btn-primary px-7 py-2.5"
                  onClick={(e) => { e.currentTarget.blur(); handleSubmit(); }}>
                  {questionNumber < numberOfQuestions - 1
                    ? <>Next question <i className="fa-solid fa-arrow-right"></i></>
                    : <>Submit quiz <i className="fa-solid fa-check"></i></>}
                </button>
              </div>
            </>
          ) : type == 'shortWeakspotQuiz' ? (
            <section className="mt-8 panel rounded-3xl p-6 sm:p-8 text-center">
              <h1 className="text-2xl font-extrabold">Dude, you're too green!</h1>
              <p className="mt-3 text-gray-200">Looks like you need to take some quizzes before we have enough data to judge your weak spots. Go take some quizzes, flail around in the dark a bit like Schrödinger's cat, and come back when you're battle tested.</p>
              <button type="button" className="btn-primary px-6 py-2.5 mt-6" onClick={handleClose}>Got it</button>
            </section>
          ) : (
            <section className="mt-8 panel rounded-3xl p-6 sm:p-8 text-center">
              <h1 className="text-2xl font-extrabold">Loading questions…</h1>
              <p className="mt-3 text-gray-300">If this takes more than a few seconds, quit and try again.</p>
            </section>
          )}
        </div>
      </div>
    )
}
