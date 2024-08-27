import LogoutButton from "./LogoutComponent"

export const MainPage = () => {
    return(
        <>
            <div className="flex ">
                {/* <div className="font-serif text-5xl w-1/2 ">
                    Learning economics doesn't have to suck...   But it usually does. 
                </div> */}
                <video autoPlay loop muted>
                    <source src="Intro.mp4" type="video/mp4" />
                </video>
            </div>
        </>
    )
}