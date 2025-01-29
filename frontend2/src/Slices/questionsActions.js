import { updateQuestions } from "./questionsSlice";
import { csrfFetch } from "../csrf";

export const getQuestions = (data) => async(dispatch) => {
    try {
        const { chapter, type, topics } = data;

        const topicsParam = encodeURIComponent(JSON.stringify(topics))

        let response
        if (type == 'chapterQuizNoUser'){
           response = await csrfFetch(`/api/quiz/questions_nouser?chapter=${chapter}`)
        } else {
           response = await csrfFetch(`/api/quiz/questions?chapter=${chapter}&type=${type}&topics=${encodeURIComponent(topicsParam)}`);
        }

    
    if (!response.ok) {
        // Log the status and response text for debugging
        const errorText = await response.text();
        console.error('Error response status:', response.status);
        console.error('Error response body: ', errorText);
        // Optionally, throw an error to handle it later in the catch block
        throw new Error(`Error ${response.status}: ${errorText}`);
      }

      const results = await response.json()
      const questions = results.questions
      const quiz_blurb = results.quiz_blurb
      const quiz_blurb_img_url = results.quiz_blurb_img_url

      console.log('QUESTIONS', results)
      dispatch(updateQuestions(questions))

      return({
        quiz_blurb,
        quiz_blurb_img_url
      })
    } catch (error) {
        console.error(error)
    }
}