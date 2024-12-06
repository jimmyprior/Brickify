import { useState, useEffect } from "react";

//https://stackoverflow.com/a/71754608/13950701

/**
 * @callback setLength
 * @param {number} length long edge length of the mosaic  (null if width and height)
 * @param {number} divisor calculated edge must be divisible by 
*/

/**
 * @param {Object} props 
 * @param {number} props.length [width, height] (resized image size)
 * @param {number} props.divisor
 * @param {boolean} props.disabled whether or not it is disabled because preview is updating
 * @param {setLength} props.setLength callback to set length on change
*/


const MULTIPLE = 16;
const MIN = 16;
const MAX = 256;

const clamp = (num, min, max) => Math.min(Math.max(num, min), max);
const round = (num, multiple) => multiple * Math.ceil(num/multiple)


const defaults = {
    64 : "Extra Small",
    80 : "Small",
    96 : "Medium",
    128 : "Large",
    160 : "Extra Large"
}



function Size(props) {
    //for custom width and height
    const [tempLength, tempSetLength] = useState(props.length);
    const [custom, setCustom] = useState(!(props.length in defaults));

    useEffect(() => {
        tempSetLength(props.length)
    }, [props.length]);

    return <div className="selection-module">
        <h2>Mosaic Size</h2>
        <label>Custom Size: <input checked={custom} onChange={() => {setCustom(!custom)}} type="checkbox"></input></label>
        {!custom && (
            <label>
                Preset Sizes
                <select 
                    onChange={(event) => {
                        props.setLength(Number(event.target.value))
                    }} 
                    value={props.length}
                    disabled={props.disabled || custom}>
                    {
                        Object.entries(defaults).map((data, index) => {
                            const size = data[0];
                            const name = data[1];
                            return <option key={`option-${index}`} value={size}>{name}</option>
                        })
                    }
                </select>
            </label>
        )}
        {custom && (
            <div>
                <label>Long Edge: 
                    <input value={tempLength} type="number" min="16" max="256" step="16" onChange={(event) => tempSetLength(Number(event.target.value))}
                    disabled={props.disabled || !custom}>
                    </input>
                </label>
                <button className="simple-button" disabled={props.disabled || !custom} onClick={(event) => {
                    //round to the nearest multiple 
                    const rounded = clamp(round(tempLength, MULTIPLE), MIN, MAX);
                    props.setLength(rounded);
                }}>Update</button>
            </div>
        )}
        <p>Mosaic size is measured in studs. Each stud is 5/16 of an inch or roughly 7.94mm. 
            Select a preset size from the dropdown or input a number of studs into the text box to set the length of the long edge of the mosaic. 
            The other side length is calculated using the aspect ratio of the image and rounding to the nearest multiple of 16.
        </p>
    </div>
}


export default Size;