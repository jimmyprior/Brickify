import './Footer.css';
import {React} from 'react';
import {Link} from "wouter";

function Footer() {
    return <footer id="footer">
      <div className="footer-links-container">
        <div className="footer-links">
          <Link href="/about">About</Link>
          <Link href="/contact">Contact</Link>
          <Link href="/terms">Terms</Link>
        </div>
        <div className="footer-links">
          <Link href="/">Home</Link>
          <Link href="/examples">Examples</Link>
          <a href={process.env.REACT_APP_HELP_DOC}>Help</a>
          <Link href="/create">Create</Link>
        </div>
      </div>
      <div id="footer-text">
        LEGO, the LEGO logo, BrickLink and the BrickLink logo are trademarks of the LEGO Group which
        is not associated with Brickify. 
      </div>
    </footer>
}


export default Footer;
