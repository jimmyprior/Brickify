import './Error.css'

/**
 * set the error to null on x icon call 
 * @callback setError
 * @param {string} data Includes image, piecelist, size and other data
*/

/**
 * 
 * @param {Object} props 
 * @param {string} props.msg
 * @param {setError} props.msg
 * @returns 
 */
function Error(props) {
    //if no error returns nothing otherwise returns the error 
    if (props.msg == null || props.msg == "") {
        return null;
    }
    return <div className="alert-box"> 
        <p>{props.msg}</p>
        <img onClick={() => props.setError(null)} className="x-icon"></img>
    </div>
}

export default Error;