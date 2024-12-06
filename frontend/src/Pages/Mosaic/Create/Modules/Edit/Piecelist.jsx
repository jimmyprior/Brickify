import {useState, useEffect, useRef} from "react";
import request from '../../../../../Utils/api';
import Piecelist from './Utils/Piecelist'
import Color from "./Utils/Color"

//default piecelists
//prerequest these and cache them so that when it requests them here it's quick af


/**
 * @param {string} piecelistID 
 * 
 */
async function getPiecelist(piecelistID) {
    /*
    seperate function because this functionality is used elsewhere as well
    */
    let error = false;
    //const piecelists = window.sessionStorage.getItem("piecelists");

    let status, data;
    if (true) {
        //not cached in session so request it
        [status, data] = await request(
            "GET", 
            `/piecelist`,
            [["ids", piecelistID], ["colors", true]]
        );
        if (status >= 200 && status < 300) {
            //add the new data
            //piecelists[piecelistID] = data
            //window.sessionStorage.setItem("piecelists", piecelists);
        }
        else {
            error = true;
            //invalid piecelist
        }
    }

    return [data, error];
}

/*
piecelist data is stored as follows: 
{
    metadata : {
        name : ""
        desc : ""
        default : bool (this allows for lazy loading and state preservation)
    },
    id : "uuid",
    object : Piecelist()
}

do not lazy load, instead hide these elements (that way state is preserved)
piecelist selector: 
needs a state that contains the data of the active piecelist 
also needs state that represents uuid input for custom 

whether default or not alaways display the uuid in the custom field

need a local state for the content of the uuid text input field before 
is set to the value of the current piecelist with a useState but can be updated 
with custom text 

when the submit button is clicked (take the value in the text field)
ensure it's not the one that is currently selected 
send the get request to get the piecelist or check the defaults if it is a default 
set parent state to match the new data when it is recieved 

have the parent have a state initially set

*/

/** 
 * used by the preview editor for selecting the piecelist 
 * (color palette to apply to the preview)
 * @param {*} props 
 * @returns 
 */
function PiecelistSelect(props) {
    //load state of selected initially.
    const [textInput, setTextInput] = useState("");

    async function updatePiecelist(pieceListID) {
        /*
            convert the api object to the obejct 
            the funciton exponenets expect to 
            work with 
            {
                metadata : {
                    name : ""
                    desc : ""
                    default : bool 
                },
                id : "uuid",
                object : Piecelist()
            }
        */
        
        //make an api request if not default 
        const [data, error] = await getPiecelist(pieceListID);

        if (!error) {
            const colors = data[0].colors.map((colorData) => {
                return new Color(colorData.rgb, colorData.lab);
            });
            props.setPiecelist({
                metadata : {
                    name : data[0].name,
                    desc : data[0].description,
                    default : false 
                },
                id : pieceListID,
                object : new Piecelist(colors)
            });
            setTextInput("")
        }
        else {
            props.setError("Error getting piecelist");
            //reset the 
        }
    }

    
    return (
        <div>
            <h2>Piecelist</h2>
            <label>Pre-made
                <select value={props.piecelist.id} onChange={async (event) => {
                    //on change update the piecelist 
                    const id = event.target.value;
                    //make sure it is not already the set piecelist
                    //make sure the id is a valid default (should alaways be)
                    if (id != props.piecelist.id && props.defaults.hasOwnProperty(id)) {
                        //set the current piecelist to the default
                        props.setPiecelist(props.defaults[id]);
                    }
                }}>
                    {
                        //display the defaults as select options
                        //is an object of (id, piecelist) pairs so loop trhough values only
                        Object.values(props.defaults).map((piecelist, index) => 
                            <option key={`piecelist-${index}`}value={piecelist.id}>{piecelist.metadata.name}</option>
                        )
                    }
                </select>
            </label>
            <hr></hr>
            <div className="side-to-side">
                <div>
                    <label>Piecelist ID
                        <input 
                            value={textInput} 
                            onChange={(event) => setTextInput(event.target.value)} 
                            type="text">
                        </input>
                    </label>
                </div>
                <button onClick={async () => {
                    //if the piecelist id does not match with what is already set 
                    //update the piecelist 
                    //will make an ajax request to the server to get the data
                    //and update the parent componenet when finished.
                    //if successful, nothing should change, 
                    //if not, error appears.
                    if (textInput !== props.piecelist.metadata.id) {
                        await updatePiecelist(textInput);
                    }
                }}>Add</button>
            </div>
            <p> Piecelists tell the program what pieces can be used in the mosaic and how many times. 
                Select a pre-made list from the dropdown or enter a custom list ID into the text box. 
                To create a piece list and obtain a custom ID, go <a href="/unimplemented">here</a>. 
            </p>
        </div>
    )
}


export {PiecelistSelect, getPiecelist}