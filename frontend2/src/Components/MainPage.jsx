import LogoutButton from "./LogoutComponent"

export const MainPage = () => {
    return(
        <>
            <div className="flex top-0 ">
                {/* <div className="font-serif text-5xl w-1/2 ">
                    Learning economics doesn't have to suck...   But it usually does. 
                </div> */}
                <video autoPlay loop muted>
                    <source src="Intro.mp4" type="video/mp4" />
                </video>
            </div>
            <img src="/Watch.png" alt="Watch the Videos" className="w-1/2 mt-10 ml-6" />
        </>
    )
}