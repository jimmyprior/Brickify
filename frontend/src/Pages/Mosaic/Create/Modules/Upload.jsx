import "./Upload.css"

import {useState, useEffect, useRef} from "react"


const OVER_COLOR = "lightgrey";
const REGULAR_COLOR = "#ffffff";
//has onImageUpload callback in props 
function ImageUpload(props) {
    const inputElement = useRef();

    const [image, setImage] = useState(null)
    const [dragInProg, setDragInProg] = useState(false);

    useEffect(() => {
        if (image != null) {
            props.onImageUpload(image);
        }
    }, [image])


    function setImageElement(file) {
        /*
        take the file and set the image element 
        */
        let image = new Image();
        let reader = new FileReader();
        reader.onload = () => {
            image.onload = () => {
                setImage(image);
            }
            let dataURL = reader.result;
            image.src = dataURL;
        }
        reader.readAsDataURL(file);
    }

    function onImageUpload(event) {
        let fileList = event.target.files;
        if (fileList.length > 0) {
            setImageElement(fileList[0]);
        }
        else {
            setImage(null);
        }
    }


    return (
        <div id="image-upload" 
            style={{backgroundColor : dragInProg ? OVER_COLOR : REGULAR_COLOR}}
            className="abs-center-div"
            onDragEnter={() => {setDragInProg(true)}}
            onDragLeave={() => {setDragInProg(false)}}
            onDragOver={(event) => {event.preventDefault()}}
            onDrop={(event) => {
                event.preventDefault();
                const files = event.dataTransfer.files;
                if (files.length > 0) {
                    const file = event.dataTransfer.files[0];
                    if (!file.type.includes("image") || file.type.includes("heic")) {
                        props.setError("Invalid image format")
                    }
                    setImageElement(file)
                }
                else {
                    console.log("Dragged image must be from desktop");
                }
                setDragInProg(false);
            }}>

            <input 
                style={{display:"none"}} 
                type="file" ref={inputElement} 
                onChange={(event) => onImageUpload(event)} 
                accept="image/*"/>

            <div 
                style={{pointerEvents: dragInProg ? "none" : "auto"}} 
                id="image-select" 
                onClick={() => {inputElement.current.click()}}>
                <img id="upload-icon" src="/image-icon.png"></img>
                <p>Select Image</p>
            </div>

            <p>or</p>
            
            <div id="drop-zone">
                <p>Drop Image Here</p>
            </div>
        </div>
    )
}

export default ImageUpload;