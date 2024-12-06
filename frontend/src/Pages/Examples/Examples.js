import Masonry, {ResponsiveMasonry} from "react-responsive-masonry"


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

export default Examples;