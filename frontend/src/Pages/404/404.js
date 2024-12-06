
import './404.css'

function NotFound() {
    return <div id="initial-404-view">
        <div className="center-col">
            <h1 id="four-zero-four-text">404 Not Found</h1>
            <p style={{textAlign : "center", maxWidth : "600px"}}>If you were directed to this page it means the 
                feature exists in the backend but the user interface is still in development.
                Stay tuned. Hoping to launch early 2024. </p>
        </div>
    </div>
}

export default NotFound;