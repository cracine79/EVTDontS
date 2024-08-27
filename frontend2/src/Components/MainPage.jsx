import LogoutButton from "./LogoutComponent"

export const MainPage = () => {
    return(
        <>
            <div className="mt-20 ml-20 flex w-11/12">
                <div className="font-serif text-5xl w-1/2 ">
                    Learning economics doesn't have to suck...   But it usually does. 
                </div>
                <video className="w-1/2" autoPlay muted>
                    <source src="Intro.mp4" type="video/mp4" />
                </video>
            </div>
        </>
    )
}