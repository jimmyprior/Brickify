import './Home.css';

import {useLocation} from 'wouter';
import Masonry, {ResponsiveMasonry} from "react-responsive-masonry"


// try rewriting using flexbox https://css-tricks.com/snippets/css/a-guide-to-flexbox/ (content align, flex wrap and flex grow)
//https://css-tricks.com/adaptive-photo-layout-with-flexbox/
//https://codepen.io/markpraschan/pen/rNNByGG
//https://freshysites.com/web-design-development/fluid-flexbox-columns/


function Image(props) {
  return <div className="image-div">
      <img src={props.src}></img>
  </div>
}

function Examples() {
    return <div id="homepage-examples"> 
      <ResponsiveMasonry columnsCountBreakPoints={{350: 2, 750: 2, 900: 3, 1000 : 4}}>
      <Masonry>
          <Image src="./home/examples/example25.png"></Image>
          <Image src="./home/examples/example1.png"></Image>
          <Image src="./home/examples/example2.png"></Image>
          <Image src="./home/examples/example3.png"></Image>
          <Image src="./home/examples/example4.png"></Image>
          <Image src="./home/examples/example5.png"></Image>
          <Image src="./home/examples/example6.png"></Image>
          <Image src="./home/examples/example7.png"></Image>
          <Image src="./home/examples/example15.png"></Image>
          <Image src="./home/examples/example24.png"></Image>
          <Image src="./home/examples/example8.png"></Image>
          <Image src="./home/examples/example9.png"></Image>
          <Image src="./home/examples/example10.png"></Image>
          <Image src="./home/examples/example11.png"></Image>
          <Image src="./home/examples/example12.png"></Image>
          <Image src="./home/examples/example13.png"></Image>
          <Image src="./home/examples/example14.png"></Image>
          <Image src="./home/examples/example0.png"></Image>
          <Image src="./home/examples/example26.png"></Image>
          <Image src="./home/examples/example16.png"></Image>
          <Image src="./home/examples/example17.png"></Image>
          <Image src="./home/examples/example18.png"></Image>
          <Image src="./home/examples/example19.png"></Image>
          <Image src="./home/examples/example20.png"></Image>
          <Image src="./home/examples/example21.png"></Image>
          <Image src="./home/examples/example22.png"></Image>
          <Image src="./home/examples/example23.png"></Image>
        </Masonry>
    </ResponsiveMasonry>
    </div>
  }
  
  function Home() {
    // https://stackoverflow.com/a/36679903
    const [location, setLocation] = useLocation();

    return <div id="home">
      <div id="initial-home-view">
        <div className="transparent-div"></div>

        <video autoPlay="autoplay" loop={true} muted={true}>
          <source src="/home/background.mp4" type="video/mp4"/>
        </video>
        <div className="full-size center-col">
          <h1 className="uppercase center-text home-page-title-text">Create A Brick Mosaic</h1>
          <div>
            <h2 className="center-text">Convert Images To Mosaics</h2>
            <h2 className="center-text">Custom Parts Lists · Bricklink Export · PDF Instructions · Price Estimates</h2>
          </div>
          <button id="create-button" className="uppercase" onClick={() => {
            setLocation("/mosaic/create");
          }}>Create</button>
        </div>
      </div>
      <Examples></Examples>
    </div>
  }
  


export default Home;