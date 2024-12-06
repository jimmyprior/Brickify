import "./Full.css"



function BricklinkButton() {
    return <button className="export-button">
        <img src="../icons/external/bricklink-logo.png"></img>
        BrickLink
    </button>
}

function BrickOwlButton() {
    return <button className="export-button">
        <img src="../icons/external/brickowl-logo.png"></img>
        BrickLink
    </button>
}

function MosaicFull(props) {
    return <div className="mosaic-container">
        <img className="mosaic-render" src="../home/examples/example18.png"></img>
        <div className="mosaic-element">
            <h2>Export</h2>
            <BricklinkButton></BricklinkButton>
            <BrickOwlButton></BrickOwlButton>
        </div>
        <div className="mosaic-element">
            <h2>Instructions</h2>
            <button>Download</button>
        </div>
        <div className="mosaic-element">
            <h2>Price</h2>
            <p>New: $208 <br></br>Used: $208</p>
        </div>
        <div className="mosaic-element">
            <h2>Extra</h2>
            <p> ID: {props.params.uuid} <br></br>
                Created: 10/10/2023 <br></br>
                Compute: 23 seconds
            </p>
            <p></p>
        </div>
    </div>

}


export default MosaicFull;