import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
export const TermsOfService = () => {
    const navigate = useNavigate()
    useEffect(()=>{
        scrollTo(0,0)
    }, [])

    return(<>
              <div className='w-full flex flex-col  items-center  mt-28'>
                <div className='sm:w-1/2 w-5/6 flex flex-col  items-center'>
                    <div className='mt-12 text-4xl font-bold'>Terms of Service</div>
                    <div className='mt-2 text-green-800'>Effective December 12, 2024</div>
                </div>
                <div className='sm:w-5/12 w-5/6 mb-20'>
                    <div className='my-4'>
                        Welcome to <strong>Economics Videos That Don't Suck</strong> ('we', 'our', 'us')  By using our website www.evtds.com (the "Site") and signing up for an account, you agree to comply with and be bound by the following Terms of Service ("Terms"). If you do not agree with these Terms, please do not use our Site.
                    </div>
                    <div>
                    These Terms govern your access to and use of our services, including signing up for an account, watching videos, taking quizzes, and interacting with our features.
                    </div>
                    <div className='text-2xl mt-6'>1. Account Registration and Use</div>
                    <div className='mt-4'>To access certain features of the Site, including quizzes and topic progress tracking, you must create an account. When you sign up, you agree to provide accurate, current, and complete information, including a valid email address. You are responsible for maintaining the confidentiality of your account credentials and for all activity that occurs under your account.</div>
                    <div className='mt-2'>You must be at least 13 years old to use this Site. If you are under 13, please do not attempt to create an account.</div>
               
                    <div className='text-2xl mt-6'>2. User Conduct</div>
                    <div className='mt-4'>By using the Site, you agree not to:</div>
                    <ul className='ml-8 list-disc'>
                        <li className='my-2'>Use the Site for any illegal or unauthorized purposes</li>
                        <li>Interfere with or disrupt the functionality of the Site, servers or networks.</li>
                        <li className='my-2'>Attempt to gain unauthorized access to any part of the Site or its systems.</li>
                        <li>Post or transmit any harmful, offensive or inappropriate content.</li>
                        <li className='my-2'>Misrepresent yourself or impersonate a person or entity.</li>
                    </ul>
                    <div className='mt-4'>We reserve the right to suspend or terminate your account if we suspect any violation of these Terms.</div>

                    <div className='text-2xl mt-6'>3.  Use of Content and Features</div>
                    <div className='mt-4'><strong>Videos and Quizzes</strong>: You may access and view the educational videos and take quizzes provided on the Site. You may not download, distribute, or modify any content without our permission.</div>
                    <div className='mt-4'><strong>Tracking of Activity</strong>: We track the videos you watch and the answers you provide on quizzes to improve our service and tailor future quizzes. This includes collecting information such as quiz scores, video completion status, and your preferences to enhance your learning experience. By using the Site, you consent to this tracking and use of your data as outlined in our <span className='text-blue-600 hover:cursor-pointer' onClick={()=>navigate('/privacypolicy')}>Privacy Policy</span>.</div>
                    <div className='text-2xl mt-6'>4.  Email and Communication</div>
                    <div className='mt-4'>By signing up for an account, you agree to receive communications from us, including emails related to your account, new features, updates, and marketing materials. You can opt out of receiving marketing emails at any time by following the unsubscribe instructions in the email or by contacting us directly.</div>

                    <div className='text-2xl mt-6'>5. User Data and Privacy</div>
                    <div className='mt-4'>We value your privacy. Our use of your personal information, including your email address and activity on the Site, is governed by our <span className='text-blue-600 hover:cursor-pointer' onClick={()=>navigate('/privacypolicy')}>Privacy Policy</span>. By using the Site, you consent to the collection, use, and sharing of your information as described in our Privacy Policy.</div>
                
                    <div className='text-2xl mt-6'>6. Disclaimer of Warranties</div>
                    <div className='mt-4'>The Site and its content are provided "as is" without any warranties of any kind, either express or implied. We do not guarantee the accuracy, reliability, or availability of the Site or its content, and we are not responsible for any errors or interruptions in the service.</div>
                
                    <div className='text-2xl mt-6'>7. Limitation of Liabilities</div>
                    <div className='mt-4'>To the maximum extent permitted by law, Economics Videos That Don't Suck shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of the Site, including but not limited to damages for loss of data, loss of profits, or business interruption.</div>
                
                    <div className='text-2xl mt-6'>8. Termination</div>
                    <div className='mt-4'>We reserve the right to suspend or terminate your account and access to the Site at our sole discretion if you violate these Terms or for any reason deemed necessary by us. Upon termination, your right to use the Site will immediately cease, and any data associated with your account may be deleted.</div>

                    <div className='text-2xl mt-6'>9. Changes to the Terms of Service</div>
                    <div className='mt-4'>We may update these Terms from time to time. When we do, we will post the revised Terms on this page with the updated “Effective Date.” We encourage you to review these Terms periodically. Your continued use of the Site after changes are posted will constitute acceptance of the revised Terms.</div>
               
                    <div className='text-2xl mt-6'>10. Governing Law</div>
                    <div className='mt-4'>These Terms are governed by and construed in accordance with the laws of the United States of America and the State of Colorado. Any disputes arising from these Terms shall be subject to the exclusive jurisdiction of the courts in the United States of America and the State of Colorado.</div>
               
                    <div className='text-2xl mt-6'>11. Contact Us</div>
                    <div className='mt-4'>If you have any questions about these Terms, please <a href='mailto:admin@evtds.com' className='font-bold text-blue-800'>Contact Us Here</a></div>
               </div>

               
              </div>
    </>)
}