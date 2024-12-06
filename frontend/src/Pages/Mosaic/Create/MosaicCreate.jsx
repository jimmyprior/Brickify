/*
    handles creation from uplaod to redirection to mosaic after creation
    has all the state for the creation process
*/

import './MosaicCreate.css'

import {useState, useEffect} from "react"

//miscellaneous
import Error from "./Comps/Error"
import ProgressBar from "./Comps/Bar"

//modules for creation
import Upload from "./Modules/Upload"
import Loading from "../../../Comps/Loading/Loading"
import Editor from "./Modules/Edit/Editor"

import request from '../../../Utils/api';
import {useHistory} from '../../../Utils/routing'

/**
 * 
 * @param {Object} props 
 * @returns 
 */
function MosaicCreate(props) {
    const [location, setLocation] = useHistory();

    const [error, setError] = useState(null); //any errors 
    const [stage, setStage] = useState(0); // index of stage in the creation process

    //data releated to mosaic creation
    const [upload, setUpload] = useState(null); // uploaded image 
    //editor state (useful if error is thrown to restore state of editor)
    //const [editor, setEditor] = useState({})  not going to bother with this rn maybe in the future

    //evntually make this work correctly with an endpoint
    async function getPiecelistDefaults() {
        //for now just store as json 
        setError("Failed to get piecelist defaults")
    }
    
    async function createMosaic(mosaicData) {
        /* when the mosaic create button is clicked
            can only happen during stage 2
            send data to server and redirects to mosaic when finished
        */
        console.log(mosaicData);
        if (mosaicData == null || mosaicData == {}) {
            setStage(1); //move stage back to edit
            setError(`Failed to create mosaic: data not set`)
            return;
        }

        let status, data;

        try {
            [status, data] = await request("POST", "/mosaic", null, mosaicData);
        } catch(error) {
            setStage(1); //move stage back to edit
            setError(`Failed to create mosaic: ${error.name}`)
            return;
        }

        if (status >= 400) {
            //could not create mosaaic (parse data for more details)
            setStage(1); //move stage back to edit
            setError("Failed to create mosaic: (Need to parse)"); //show error
            return;
        }
        
        //success redirect to mosaic page
        setLocation(`/mosaic/${data.id}`, data);
    }

    //creation stage modules 
    //title: title displayed
    //name: text to be used in the progress bar 
    //component: component to be displayed for the stage
    const modules = [
        {
            title : "Image Upload",
            name : "Upload",
            component : <Upload 
                onImageUpload={(image) => {
                    setUpload(image); 
                    setStage(stage + 1);
            }} setError={setError}/>
        }, 
        {
            title : "Preview Editor",
            name : "Edit",
            //none of the presets are actually being used at the moment
            component : <Editor 
                image={upload} 
                piecelist={null} 
                length={10} 
                effects={{}}
                onSubmit={(data) => {
                    setStage(stage + 1); //increment to loading stage 
                    createMosaic(data); //send create mosaic request
                }}
                setError={setError}/>
        },
        {
            title : "Creating Mosaic",
            name : "Create",
            component : <Loading 
                topText="Creating your mosaic" 
                bottomText="This can take up to a minute"/>
        }
    ];

    const steps = modules.map((item) => item.name);

    return <div className="full-screen-page">
        <Error msg={error} setError={setError}></Error>
        <div id="create-header">
            <h2 id="create-title">{modules[stage].title}</h2>
            <ProgressBar steps={steps} index={stage}></ProgressBar>
        </div>
        {modules[stage].component}
    </div>
}


export default MosaicCreate;