class Color {
    /**  
        * @constructor
        * @param {number[]} rgb - [Number, Number, Number]
        * @param {number[]} [lab] - [Number, Number, Number]
    */
    constructor(rgb, lab) {
        this.rgb = rgb;
        if (lab === undefined) {
            //convert rgb go lab
            lab = Color.RGBtoLAB(rgb);
        }
        this.lab = lab;
    }

    /**
     * converts rgb to cielab
     * @param {number[]} rgb rgb color representation
     * @returns {number[]} cielab color representation
     */
    static RGBtoLAB(rgb) {
        if (rgb in Color.LOOKUP) {
            return Color.LOOKUP[rgb];
        }
    
        let lab = Color.XYZtoLAB(Color.RGBtoXYZ(rgb));
        Color.LOOKUP[rgb] = lab;
        return lab;
    }


    /**
     * 
     * @param {number[]} rgb rgb color representation
     * @returns {number[]} xyz color representation
     */
    static RGBtoXYZ(rgb) {
        //http://www.easyrgb.com/en/math.php
        const [var_R, var_G, var_B] = rgb
            .map(x => x / 255)
            .map(x => x > 0.04045
                ? Math.pow(((x + 0.055) / 1.055), 2.4)
                : x / 12.92)
            .map(x => x * 100)

        // Observer. = 2°, Illuminant = D65
        return [
            var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805,
            var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722,
            var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
        ]
    }


    /**
     * 
     * @param {number[]} xyz xyz color representation
     * @returns {number} cielab color representation
     */
    static XYZtoLAB([x,y,z]) {
        const [ var_X, var_Y, var_Z ] = [ x / Color.REF_X, y / Color.REF_Y, z / Color.REF_Z ]
            .map(a => a > 0.008856
                ? Math.pow(a, 1 / 3)
                : (7.787 * a) + (16 / 116))

        return [
            (116 * var_Y) - 16,
            500 * (var_X - var_Y),
            200 * (var_Y - var_Z)
        ]
    }


   /**
    * Calculates distance squared between two colors uses cielab colors for accuracy
    * @param {Color} color another color object
    * @returns {Number} distance squared
    */
    getEuclideanDistance(color) {
        return Math.hypot(
            color.lab[0] - this.lab[0],
            color.lab[1] - this.lab[1],
            color.lab[2] - this.lab[2],
        );
    }
}
Color.REF_X = 95.047;
Color.REF_Y = 100.000;
Color.REF_Z = 108.883;
Color.LOOKUP = {} //used for rgb to cielab conversion lookups 

export default Color;