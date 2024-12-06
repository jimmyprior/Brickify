import "./Piece.css";

function Piece(props) {
    return <tr className="piece">
        <td>Img?</td>
        <td>ID: {props.piece.uuid}</td>
        <td>Name: {props.piece.part.name}</td>
        <td>Price: 
            <div>Used PPS Avg: {`$${props.piece.price.used.pps}`}</div>
            <div>New PPS Avg: {`$${props.piece.price.new.pps}`}</div>
        </td>
        <td>Color: {props.piece.color.name}</td>
        <td>
            QTY: <input onChange={() => {}} value={props.qty} type="number"></input>
            <button>Update</button>
        </td>
        <td>
            <button>Delete</button>
        </td>
    </tr>
}

export default Piece;