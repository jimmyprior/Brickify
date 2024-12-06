import "./Bar.css"

function ProgressBar(props) {
    //i should have documented this :/

    const CIRCLE_RADIUS = 20;
    const LINE_LENGTH = 100;
    const NUM_STEPS = props.steps.length;
    const Y_MARGIN = 40;
    const X_MARGIN = 20;
    const HEIGHT = CIRCLE_RADIUS + 30 + Y_MARGIN * 2;
    const WIDTH = (CIRCLE_RADIUS * 2) * NUM_STEPS + (NUM_STEPS - 1) * LINE_LENGTH + X_MARGIN * 2;

    return <svg className="step-bar" preserveAspectRatio="xMidYMid meet" viewBox={`0 0 ${WIDTH} ${HEIGHT}`} height={HEIGHT} width={WIDTH}>
            {props.steps.map((value, index) => {

                let returnArray = [];
                if (index !== (props.steps.length - 1)) {
                    let color = "#ffffff";
                    if (index <= props.index - 1) {
                        color = "#e8b92b";
                    }
                    let x1 = X_MARGIN + (CIRCLE_RADIUS * 2) + LINE_LENGTH * index + (CIRCLE_RADIUS * 2) * index;
                    let x2 = x1 + LINE_LENGTH;
                    returnArray.push(
                        <line key={`line-${index}`} x1={x1} y1={Y_MARGIN + CIRCLE_RADIUS} x2={x2} y2={Y_MARGIN + CIRCLE_RADIUS} style={{
                            stroke:color,
                            strokeWidth:8
                        }}/>
                    )
                }
                let color = "#ffffff";
                if (index <= props.index) {
                    color = "#e8b92b";
                }
                let x1 = X_MARGIN + CIRCLE_RADIUS + (CIRCLE_RADIUS * 2) * index + LINE_LENGTH * index;
                returnArray.push(
                    <circle key={`circle-${index}`} cx={x1} cy={Y_MARGIN + CIRCLE_RADIUS} r={CIRCLE_RADIUS} fill={color} />
                )
                returnArray.push(
                    <text key={`text-${index}`} textAnchor="middle" x={x1} y={Y_MARGIN + CIRCLE_RADIUS * 2 + 30}>{value}</text>
                )
                return returnArray;
            })}
    </svg> 
}

export default ProgressBar;