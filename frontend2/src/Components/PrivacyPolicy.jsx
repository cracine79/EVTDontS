import { useEffect } from "react"
export const PrivacyPolicy = () => {
    useEffect(()=>{
        scrollTo(0,0)
    }, [])
    return(<>
        <div className='w-full flex flex-col  items-center  mt-28'>
            <div className='sm:w-1/2 w-5/6 flex flex-col  items-center'>
                <div className='mt-12 text-4xl font-bold'>Privacy Policy</div>
                <div className='mt-2 text-green-800'>Effective December 12, 2024</div>
            </div>
          
            <div className='sm:w-5/12 w-5/6 mb-20'>
                <div className='my-4'>
                    At Economics Videos That Don't Suck ("we", "our", "us"), we are committed to protecting your privacy. This Privacy Policy explains how we collect, use, and share information about you when you visit our website www.evtds.com (the "Site").
                </div>
                <div>
                By using our Site, you consent to the practices outlined in this Privacy Policy. If you do not agree with this policy, please do not use our Site.
                </div>

                <div className='text-2xl mt-6'>1. Information We Collect</div>
                <div className='mt-4'>We collect the following types of information when you visit our Site:</div>
                <ul className='list-disc ml-8'>
                    <li className='my-2'><span className='font-bold'>Personal Information</span>: This includes information that you provide directly to us, such as your name, email address, and any other information you submit through contact forms, newsletters, or account registration.</li>
                    <li><span className='font-bold'>Usage Data</span>: We may automatically collect certain information about your device and usage of the Site, such as your IP address, browser type, pages visited,  time spent on the Site, as well as recording types of questions answered and quiz scores. This information is typically collected through cookies and other tracking technologies.</li>
                    <li className='my-2'><span className='font-bold'>Cookies</span>: We use cookies to enhance your experience on our Site. Cookies are small text files placed on your device to remember your preferences and track usage patterns. You can control cookie settings through your browser, but disabling cookies may affect your experience.</li>
               </ul>

               <div className='text-2xl mt-8'>2. How We Use Your Information</div>
                <div className='mt-4'>We use the information we collect to:</div>
                <ul className='list-disc ml-8'>
                    <li className='my-2'>Provide and improve our services and website.</li>
                    <li>Communicate with you, including sending newsletters, updates, or marketing materials if you’ve opted-in.</li>
                    <li className='my-2'>Respond to your inquiries or feedback.</li>
                    <li>Analyze usage patterns to improve our content and features.</li>
                    <li className='my-2'>Comply with legal obligations, prevent fraud, and ensure the security of the Site.</li>
                </ul>

                <div className='text-2xl mt-8'>3.  Sharing Your Information</div>
                <div className='mt-4'>We do not sell or rent your personal information to third parties. We may share your information with trusted third-party service providers who assist us in operating the Site, conducting our business, or servicing you. These third parties are required to maintain the confidentiality of your information and use it only for the purposes specified by us.</div>
                <div className='my-2'>We may also share your information if required by law or if we believe that such action is necessary to protect our rights, your safety, or the safety of others.</div>
              
                <div className='text-2xl mt-8'>4.  Your Rights and Choices</div>
                <div className='mt-4'>Depending on your location, you may have certain rights regarding the personal information we collect, including:</div>
                <ul className='list-disc ml-8'>
                    <li className='my-2'><span className='font-bold'>Access</span>: You can request a copy of the personal information we have about you.</li>
                    <li><span className='font-bold'>Correction</span>: You can update or correct any inaccurate personal information.</li>
                    <li className='my-2'><span className='font-bold'>Deletion</span>: You can request the deletion of your personal information, subject to legal exceptions.</li>
                    <li><span className='font-bold'>Opt-out</span>: You can opt out of receiving marketing communications from us by following the unsubscribe instructions in our emails or contacting us directly.</li>
                </ul>

                <div className='text-2xl mt-8'>5. Data Security</div>
                <div className='mt-4'>We implement reasonable administrative, technical, and physical security measures to protect your personal information from unauthorized access, use, or disclosure. However, no data transmission over the internet is 100% secure, and we cannot guarantee the security of information sent to or from our Site.</div>
              
                <div className='text-2xl mt-8'>6.  Third-Party Links</div>
                <div className='mt-4'>Our Site may contain links to third-party websites. These third-party sites have their own privacy policies, and we are not responsible for their practices. We encourage you to review the privacy policies of any third-party websites you visit.</div>
                
                <div className='text-2xl mt-8'>7. Children's Privacy</div>
                <div className='mt-4'>Our Site is not intended for children under the age of 13. We do not knowingly collect personal information from children. If we become aware that we have inadvertently collected personal information from a child under 13, we will take steps to delete that information as soon as possible.</div>
            
                <div className='text-2xl mt-8'>8. Changes to This Privacy Policy</div>
                <div className='mt-4'>We may update this Privacy Policy from time to time. When we do, we will post the updated policy on this page and revise the “Effective Date” at the top. We encourage you to review this policy periodically for any changes. Your continued use of the Site after changes to the Privacy Policy will be considered acceptance of those changes.</div>


                <div className='text-2xl mt-8'>9.  Contact Us</div>
                <div className='mt-4'>For more information, please <a href='mailto:admin@evtds.com' className='font-bold text-green-800'>Contact Us Here</a></div>

            </div>
       
        </div>
    </>)
}