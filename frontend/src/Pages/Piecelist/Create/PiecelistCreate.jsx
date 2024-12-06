import { useEffect, useState } from "react"
import request from "../../../Utils/api";

import Piece from "../Utils/Piece";



function PiecelistDisplay() {
    //get piecelist 

}


/*
updated format for storing pieces: 
{
    id : {
        data : {...piece data}
        qty : number of qty
    }
}
*/


//on submit redirect to another tab that displays the piecelist info

function PiecelistCreate() {
    //piecelistcreator
    const [state, setState] = useState({
        ppsUsedLessThan : "",
        ppsNewLessThan : "",
        yrsProducedGreaterThan : "",
        numSetsGreaterThan : "",
        totalInSetsGreaterThan :"",
        areaLessThan : "",
    });

    const [qty, setQty] = useState(-1);

    const [pieces, setPieces] = useState({});
    const [id, setID] = useState("None");
    const [name, setName] = useState("Unnamed List")

    useEffect(() => {
        console.log(`Length of pieces: ${Object.keys(pieces).length}`)
    }, [pieces])

    return <div>
        <div>
            <h2>Price Filters</h2>
            <label>
                Max PPS New
                <input 
                    type="number"
                    min={0}
                    step={.01}
                    max={30}
                    value={state.ppsNewLessThan}
                    onChange={(event) => setState({...state, ppsNewLessThan : event.target.value})}
                ></input>
            </label>
            <label>
                Max PPS Used
                <input 
                    type="number"
                    min={0}
                    step={.01}
                    max={30}
                    value={state.ppsUsedLessThan}
                    onChange={(event) => setState({...state, ppsUsedLessThan : event.target.value})}
                ></input>
            </label>
        </div>
        <div>
            <h2>Production Filters</h2>
            <label>
                Years produced greater than
                <input 
                    type="number"
                    min={1}
                    max={80}
                    value={state.yrsProducedGreaterThan}
                    onChange={(event) => setState({...state, yrsProducedGreaterThan : event.target.value})}
                ></input>
            </label>
            <label>
                Min Set occurances
                <input 
                    type="number"
                    min={1}
                    max={1000}
                    value={state.numSetsGreaterThan}
                    onChange={(event) => setState({...state, numSetsGreaterThan: event.target.value})}
                ></input>
            </label>
            <label>
                Min Total number produced
                <input 
                    type="number"
                    min={1}
                    max={1000}
                    value={state.totalInSetsGreaterThan}
                    onChange={(event) => setState({...state, totalInSetsGreaterThan : event.target.value})}
                ></input>
            </label>
            <label>
                Area less than
                <input 
                    type="number"
                    min={1}
                    max={200}
                    value={state.areaLessThan}
                    onChange={(event) => setState({...state, areaLessThan : event.target.value})}
                ></input>
            </label>
            <label>
                Quantity
                <input 
                    type="number"
                    min={-1}
                    max={10000}
                    value={qty}
                    onChange={(event) => setQty(event.target.value)}
                ></input>
            </label>
        </div>
        <button onClick={async () => {
            /*
            get pieces
            */
            const query = {}
        
            //add the query to list if they're not nothing
            //also cast them to integers
            for (const [key, value] of Object.entries(state)) {
                let v = Number(value)
                if (v !== 0) {
                    query[key] = v;
                } 
            }

            const [status, data] = await request("GET", "/piece", query);

            const newPieces = {...pieces}; //rewrite any old pieces with old qty
            for (let p of data) {
                newPieces[p.uuid] = {
                    qty : qty,
                    data : p
                };
            }
            setPieces(newPieces);

        }}>Add to list</button>

        <div>
            <h2>Other</h2>
            <label>
                Name:
                <input 
                    type="text"
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                ></input>
            </label>
        </div>

        <button onClick={async () => {                        
            let formattedPieces = [];

            for (let key of Object.keys(pieces)) {
                formattedPieces.push({
                    piece_uuid : key,
                    qty : pieces[key].qty
                })
            }
            
            const body = {
                pieces : formattedPieces, 
                name : name,
                description : JSON.stringify(state)
            };

            const [status, data] = await request("POST", "/piecelist", {}, body)

            setID(data.uuid);

        }}>Create</button>
        <button onClick={() => {setPieces({})}}>Clear List</button>
        <p>ID: {id}</p>
        <p>Pieces Variations: {Object.keys(pieces).length}</p>
        
        <div className="table-container">
            <table className="table">
                <tr>
                    <th>Image</th>
                    <th>UUID</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Color</th>
                    <th>QTY</th>
                    <th>Remote</th>
                </tr>
                {Object.values(pieces).map((data, index) => {
                    return <Piece piece={data.data} qty={data.qty} key={index}></Piece>
                })}
            </table>
        </div>
    </div>
}




export default PiecelistCreate