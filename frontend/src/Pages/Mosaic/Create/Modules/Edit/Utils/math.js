function getDivisibleSize(width, height, divisor) {
    /*
    width: width of the image to be resized
    height: height of the image to be reszieds
    divisor: number that both the width and height should become multiples of
  
    makes the width and height divisible by the divisor parameter and returns 
    the new width and height as a list
  
    THIS CAN ROUND UP BUT AS LONG AS THE LONG EDGE IS 
    DIVISBLE BY DIVISOR IT SHOULD NEVER EXCEED THE LONG EDGE 
    */
    const adjusted = []
    for (const edge of [width, height]) {
      let remainder = edge % divisor;
      if (remainder > Math.ceil(divisor / 2)) 
        adjusted.push(edge + divisor - remainder)
      else {
        adjusted.push(edge - remainder)
      }
    }
    return adjusted
}

function getReducedSize(width, height, longEdge) {
    /*
    width: width of the image to be reduced 
    height: height of the image to be reduced 
    longEdge: the new length of the long edge 
  
    reduces the image size while preserving the aspect ratio
    returns the new image size with the preserved asepect ratio
    */
  
    let ratio = width / height;
  
    if (ratio > 1) {
      return [longEdge, Math.floor(longEdge / ratio)]
    }
  
    return [Math.floor(longEdge * ratio), longEdge];
}

export {getDivisibleSize, getReducedSize};
