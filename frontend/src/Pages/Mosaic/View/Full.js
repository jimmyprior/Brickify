import "./Full.css"

import {useEffect, useState} from "react"
import {useLocation} from "wouter"

import request from '../../../Utils/api'

function BricklinkButton() {
    return <button className="export-button">
        BrickLink
        <img src="../icons/external/bricklink-logo.png"></img>
    </button>
}

function BrickOwlButton() {
    return <button className="export-button">
        BrickOwl
        <img src="../icons/external/brickowl-logo.png"></img>
    </button>
}


/*
{
    "id": "a8d2a922-a7e0-4ece-90d1-1a7ea8270fd1",
    "time": {
        "initialized": 1706554586,
        "completed": 1706554590
    },
    "price": {
        "used": 661.679,
        "new": 1424.3074
    },
    "media": {
        "render": "presigned url",
        "instructions": "optional presigned url"
    },
    "owner": {
        "id": null
    }
}
*/


/**
 * @param {Object} props 
 * @param {String} props.id 
 * @param {Object} props.time 
 * @param {Number} props.time.initialized 
 * @param {Number} props.time.completed 
 * @param {Object} props.price 
 * @param {Number} props.price.new 
 * @param {Number} props.price.used 
 * @param {Object} props.media 
 * @param {String} props.media.render
 * @param {String} props.media.instructions
 * @param {Object} props.owner 
 * @param {String} props.owner.id
*/
function MosaicFull(props) {
    const [data, setData] = useState(window.history.state);
    const [location, setLocation] = useLocation();


    useEffect(() => {
        async function getData() {
            //if no histroy with mosaic data need to retrieve from the server

            const [status, data] = await request("GET", `/mosaic/${props.params.uuid}`)
            
            if (status >= 400) {
                if (status == 404) {
                    //show 404 
                    //unknown error (show error message)
                }
                //mosaic not found
                //rediredct ot mosaic not found page
            }      
            else {
                setData(data);
            }
        }
        if (data == null) {
            getData();
        }
    }, [])

    function getDateString(unix) {
        const date = new Date(unix * 1000);
        return date.toLocaleDateString("en-US");
    }

    if (data == null) {
        return <div>
            <p>404 Mosaic Not Found</p>
        </div>
    }
    else {
        return <div className="mosaic-view">
            <div className="mosaic-info">
                <h1>Brickify Mosaic</h1>
                <div className="mosaic-modules">
                    <div className="module export-min-width">
                        <h2>Export</h2>
                        <BricklinkButton></BricklinkButton>
                        <BrickOwlButton></BrickOwlButton>
                    </div>
                    <div className="module">
                        <h2>Instructions</h2>
                        <a target="_blank" href={data.media.instructions}>Link</a>
                        <button>Download</button>
                    </div>
                    <div className="module">
                        <h2>Price</h2>
                        <p>New: ${data.price.new.toFixed(2)} <br></br>Used: ${data.price.used.toFixed(2)}</p>
                    </div>
                    <div className="module">
                        <h2>Extra</h2>
                        <p> ID: {props.params.uuid.toUpperCase()} <br></br>
                            Created: Need to add <br></br>
                            Compute: {data.time.completed - data.time.initialized} seconds
                        </p>
                        <p></p>
                    </div>
                </div>
            </div>
            <img className="mosaic-render" src={data.media.render}></img>
        </div>
    }
}


export default MosaicFull;