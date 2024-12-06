import Color from "./Color"


/**
 * takes ctx as input and yields coordinate of pixel and rgb value at that pixel 
 * @param {CanvasRenderingContext2D} ctx 
 * @yields {{coordinate : Number[], color : Color}}
 */
function* yieldPixelData(ctx) {
    const width = ctx.canvas.width;
    const height = ctx.canvas.height;

    //needed to access pixel data of the canvas (original image pixel data)
    const imageBuffer = ctx.getImageData(0, 0, width, height).data;
    
    for (let x = 0; x < width; x++) {
        for (let y = 0; y < height; y++) {
            let location = (x * 4) + (y * width * 4);
            //get rgb value from the original image as array buffer
            let r = imageBuffer[location + 0];
            let g = imageBuffer[location + 1];
            let b = imageBuffer[location + 2];

            yield {coordinate : [x, y], color : new Color([r,g,b])};
        }
    }
}


class Piecelist {
    /**
    * for now linear search, eventually will do nearest neighbor with k-d tree or similar data structure
    * @param {Color[]} colors 
    */
    constructor(colors) {
        //dont include other metadata (name, desc, id) in here (lets keep the function limited to the serach)
        this.colors = colors
    }

    /**
    * currently linear search but eventually use k-d tree or similar data structure
    * @param {Color} color Another color object. Will convert the image rgb 
    * @return {Color} returns nearest color
    */
    getNearestColor(color) {
        /*

            implement k-d structure
            implment nearest neighbor search
        */
        let smallestColor = this.colors[0];
        let smallestDistance = color.getEuclideanDistance(this.colors[0]);

        for (let compare of this.colors.slice(1)) {
            const distance = color.getEuclideanDistance(compare);
            if (distance < smallestDistance) {
                smallestColor = compare;
                smallestDistance = distance;
            }
        }
        return smallestColor;
    }

    /**
     * modifies canvas passed as param and recolor it using colors in the list
     * @param {HTMLCanvasElement} canvas 
    */
    recolorImage(canvas) {
        const ctx = canvas.getContext("2d");

        for (let pixelData of yieldPixelData(ctx)) {
            const [x, y] = pixelData.coordinate;
            let nearestColor = this.getNearestColor(pixelData.color);
            let [r, g, b] = nearestColor.rgb;
            ctx.fillStyle = `rgb(${r}, ${g}, ${b})`
            ctx.fillRect(x, y, 1, 1);
        }
    }
}


export default Piecelist;
