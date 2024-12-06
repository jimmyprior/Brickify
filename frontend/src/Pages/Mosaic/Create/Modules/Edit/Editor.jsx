import "./Editor.css"

import {useState, useEffect} from "react"

import Effects from "./Effects.jsx"
import Size from "./Size.jsx"

import fs from "./Utils/glfx.js"
import {getDivisibleSize, getReducedSize} from "./Utils/math.js"
import {PiecelistSelect} from "./Piecelist"
import DEFAULTS from "./Utils/defaults";

//state is being forgotten when componetns dismount on tab switch for size and piecelist 
//can fix that by making them display none instead of actually unmounting the components.

//https://michaelcurrin.github.io/dev-cheatsheets/cheatsheets/javascript/general/jsdoc.html


const MULTIPLE = 16; // what the adjusted image edge sizes must be divisible by
const IMAGE_TYPE = "image/png" 


//Note: The preview image does not factor in the size of the pieces which means in the next stage 
//when the piece positions are computed some colors may change slightly due to size constraints. 

/**
 * @callback onSubmit
 * @param {Object} data Includes image, piecelist, size and other data
*/

/**
 * Get a rough preview of what the mosaic will probably look like 
 * before sending it to the server to actually be created
 * @param {Object} props 
 * @param {HTMLImageElement} props.image unedited image element
 * @param {Piecelist} props.piecelist starting pieceList
 * @param {Number} props.length length of the image's long edge
 * @param {Object} props.effects image effects to be applied originally
 * @param {Number} props.effects.contrast float between -1 to 1 
 * @param {Number} props.effects.brightness float between -1 to 1 
 * @param {Number} props.effects.vibrance float between -1 to 1 
 * @param {onSubmit} props.onSubmit callback when user clicks continue (sends all data to callback)
*/
function Editor(props) {

    const [effects, setEffects] = useState({
        contrast : 0,
        brightness : 0,
        vibrance : 0
    }); //effects applied to the unedited before preview render

    const [defaults, setDefaults] = useState(DEFAULTS);
    const [piecelist, setPiecelist] = useState(Object.values(DEFAULTS)[0]);

    const [length, setLength] = useState(16*6); //long edge length of the image 
    const [preview, setPreview] = useState(null);  //base64 edited image
    
    const [error, setError] = useState(); //bool and error message (need to implement this look at friendrdle error comp)
    const [disabled, setDisabled] = useState(false); //whether or not the inputs should be disabled
    

    async function changePiecelist(piecelistID) {
        /* 
        piecelist has to be an object with a special serarch function 

        piecelistID : uuid of the piecelist 
    
        state used:
            error (sets if it runs into an error)
            piecelist : piecelist information id and color data
            disabled : [bool] if the some input data is being changed set to ture 
                        so that inputs can be disabled and to false afterwards

        makes an http request to the server to get data about piecelist (strictly color data)
        set loading state to true 
        sets the piecelist state to Piecelist object (will be a tree) with fast search
        set loading state to false (don't need to this because updatePreview useEffect will
        run after which will set to false again after)

        if failure to get data, (timeout)
        display error message
        */        
        setDisabled(true);

        //setPiecelist()

        
    }

    function updatePreview() {
        /*
        updates the image preview of ideal mosaic 

        unedited : this is the unedited image

        state write: 
            preview : stores base64 preview image (this is what is updated)
            disabled : used to disable the inputs when updating the preview

        state read:
            image effects ()
            length : long edge of the image 
            effects : 
            piecelist : 
        
        applies image effects to the image 
        resizes the image (if there is no quality difference do this before effects for efficency)
        recolors the image with the new color list (piecelist) 
        used a method on the piecelist object that does quick comparisons to find the nearest color
        returns recolored image (maybe build in a method that does this on the piecelist object)
        set preview the edited and recolored image
        */
        setDisabled(true);
        
        //does the image operations
        let glfx = fs.canvas();
        let imageTexture = glfx.texture(props.image);
        glfx.draw(imageTexture);
        glfx.brightnessContrast(effects.brightness, effects.contrast);
        glfx.vibrance(effects.vibrance);
        glfx.update();

        const canvas = document.createElement("canvas");

        let smaller = getReducedSize(props.image.width, props.image.height, length);
        const [width, height] = getDivisibleSize(smaller[0], smaller[1], MULTIPLE);

        const ctx = canvas.getContext("2d");

        canvas.width = width;
        canvas.height = height;
        ctx.drawImage(glfx, 0, 0, width, height);

        piecelist.object.recolorImage(canvas)

        setPreview(canvas.toDataURL(IMAGE_TYPE));
        
        setDisabled(false);

    }

    useEffect(() => {
        /*
        re-renders the edited image when piecelist, effects or length are changed
        */
        if (props.image != null && piecelist != null && length != null && !disabled) {
            updatePreview();
        }
        else {
            console.info("did not update. necessary values are not set")
        }
    }, [piecelist, effects, length])

    const [selector, setSelector] = useState("SIZE");

    const selectedStyle = {
        backgroundColor: "white",
        boxShadow: "4px 0px rgb(232, 185, 43)",
        zIndex: 1,
        border: "none",
    }

    const select = {
        "EFFECTS" : <Effects effects={effects} setEffects={setEffects}></Effects>,
        "SIZE" : <Size length={length} setLength={setLength}></Size>,
        "PIECELIST" : <PiecelistSelect setError={props.setError}setPiecelist={(plData)=> {
            if (!(plData.id in defaults)) {
                
                setDefaults((defaults) => {
                    const newDefaults = {...defaults};
                    newDefaults[plData.id] = plData;
                    return newDefaults;
                });
            }
            setPiecelist(plData);
        }} defaults={defaults} piecelist={piecelist}></PiecelistSelect>,
        "OTHER" : null
    }

    return (
        <div className="biggest-edit-cont">
            <div className="preview-box">
                <div className="preview-title-box">
                    <h2>Preview</h2>
                    <img className="tool-tip-icon" src="/icons/help.svg"></img>
                </div>
                <img className="editor-image" src={preview}></img>

            </div>
            <div className="big-container">
                <ul id="editor-selector">
                    <li onClick={() => setSelector("SIZE")} style={selector === "SIZE" ? selectedStyle : null}>Size</li>
                    <li onClick={() => setSelector("EFFECTS")} style={selector === "EFFECTS" ? selectedStyle : null}>Effects</li>
                    <li onClick={() => setSelector("PIECELIST")} style={selector === "PIECELIST" ? selectedStyle : null}>Pieces</li>
                    <li onClick={() => setSelector("OTHER")} style={selector === "OTHER" ? selectedStyle : null}>Other</li>
                </ul>
                <div className="edit-parent" style={{
                    boxSizing: "border-box",
                    boxShadow: "4px 4px rgb(232, 185, 43)",
                }}>
                    {select[selector]}
                </div>
            </div>

            <button id="continue-button" disabled={disabled} onClick={() => {
                const imageData = preview.split(",")[1];
                props.onSubmit({
                    image : imageData,
                    pieceListID : piecelist.id,
                    settings : {
                        maxDist : 12,
                        shuffle : false
                    }
                });
            }}>Continue</button>
        </div>
    )
}




export default Editor;