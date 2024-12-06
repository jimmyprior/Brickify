import './Effects.css'

import {useState, useEffect} from "react"


/*
    props: min, max, step, value, onChange, disabled

    effects slider. Only calls back when it has been dropped.
    ontouchend is for mobile up 
*/
function EffectSlider(props) {
    const [value, setValue] = useState(props.value); // 

    useEffect(() => {
        //if the props value doesn't match, update the value to match
        //this allows for the parent to reset the value and the slider will match accordingly
        if (props.value !== value) {
            //only runs when parent changes the slider value
            setValue(props.value); 
        }
    }, [props.value]);

    return (
        <input 
            type="range"
            min={props.min}
            max={props.max}
            step={props.step}
            value={value}
            onChange={(event) => setValue(Number(event.target.value))}
            onMouseUp={() => props.onChange(value)}
            onTouchEnd={() => props.onChange(value)}
            disabled={props.disabled}>
        </input>
    )
}


/**
 * @callback setEffects
 * @param {Object} effects
 * @param {Number} effects.vibrance
 * @param {Number} effects.contrast
 * @param {Number} effects.brightness
 */

/**
 * 
 * @param {Object} props 
 * @param {Object} props.effects
 * @param {Number} props.effects.vibrance
 * @param {Number} props.effects.contrast
 * @param {Number} props.effects.brightness
 * @param {setEffects} props.setEffects
 * @param {boolean} props.disabled
 * @returns 
 */
function Effects(props) {
    return (
        <div className="">
            <h2>Image Effects</h2>
            <div id="effect-content">
                <div id="editor-sliders-parent">
                    <label>Contrast
                        <EffectSlider 
                            min={-1} 
                            max={1}
                            value={props.effects.contrast}
                            onChange={(value) => props.setEffects({...props.effects, contrast : value})}
                            step={.1}
                            disabled={props.disabled}
                        />
                    </label>
                    <label>Vibrance
                        <EffectSlider 
                            min={-1} 
                            max={1}
                            value={props.effects.vibrance}
                            onChange={(value) => props.setEffects({...props.effects, vibrance : value})}
                            step={.1}
                            disabled={props.disabled}
                        />
                    </label>
                    <label>Brightness
                        <EffectSlider 
                            min={-1} 
                            max={1}
                            value={props.effects.brightness}
                            onChange={(value) => props.setEffects({...props.effects, brightness : value})}
                            step={.1}
                            disabled={props.disabled}
                        />
                    </label>
                </div>
                <button id="effects-reset-button"
                    onClick={() => props.setEffects({contrast : 0, brightness : 0, vibrance : 0})}
                    disabled={props.disabled} 
                >Reset</button>
            </div>
            <p>Effects are added to the original image which is then resized and recolored according to the pieces in the selected piece list. 
                Adjusting certain aspects of the image before mosaic creation can help preserve detail that would 
                have otherwise been lost due to downsizing and a limited color palette.
                </p>
        </div>
    )
}

export default Effects;