import {React, useState, useEffect} from 'react';
import {Link, useLocation} from "wouter";
import './Header.css';


console.log(process.env)

function Header() {
    const [hideSide, setHideSide] = useState(true);
    const [location, setLocation] = useLocation();

    useEffect(() => {
      if (hideSide == false) {
        document.body.style["overflow-y"] = "hidden";
      }
      else {
        document.body.style["overflow-y"] = "scroll";
      }
    }, [hideSide])
  
      return (
        <header className="center-row jc-space-between">
          <div className="center-row">
            <img onClick={() => setHideSide(!hideSide)}id="menu-icon" src="/icons/menu.png"></img>
            <div className="header-links">
              <Link href="/">Home</Link>
              <Link href="/examples">Examples</Link>
              <a href={process.env.REACT_APP_HELP_DOC} target="_blank">Help</a>
            </div>
          </div>
          <div className="center-row">
            {location !== "/mosaic/create" && (
              <button id="header-create-button" className="uppercase" onClick={()=> {
                setLocation("/mosaic/create")
              }}>Create</button>
            )}
            <img className="header-logo" src="/icons/logo.png"></img>
          </div>
          {!hideSide && <div id="cover" onClick={() => {
              setHideSide(true);
            }}></div> 
          }
          {!hideSide && <SideNav></SideNav>}
        </header>
    )
}


function SideNav() {
    return <div id="side-nav">
      <Link href="/">Home</Link>
      <Link href="/examples">Examples</Link>
      <a href={process.env.REACT_APP_HELP_DOC} target="_blank">Help</a>
      <Link href="/mosaic/create">Create</Link>
      <Link href="/about">About</Link>
      <Link href="/terms">Terms</Link>
    </div>
  }

// when cover is clicked undoes everything 
//     document.body.style.overflow = "hidden";
//https://stackoverflow.com/questions/46142712/access-body-from-react  

export default Header;