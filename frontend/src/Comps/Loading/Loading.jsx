import "./Loading.css"

import Lottie from "lottie-react";
import loadingAnimation from "./loadingAnimation.json"


/**
 * @param {Object} props
 * @param {String} props.bottomText Bottom Text
 * @param {String} props.topText Top Text
 * @returns 
 */
function Loading(props) {
    return <div id="loading-container" className="abs-center-div">
        <p className="load-text">{props.topText}</p>
        <Lottie className="brick-loading-animation" animationData={loadingAnimation} loop={true}></Lottie>
        <p className="load-text">{props.bottomText}</p>
    </div>
}


export default Loading;