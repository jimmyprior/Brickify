import './index.css';

import {React} from 'react';
import ReactDOM from 'react-dom/client';

import { Route, Switch} from "wouter";

import Home from './Pages/Home/Home'
import About from './Pages/About/About'
// import Create from './CreateOld/Create.js'
import MosaicCreate from './Pages/Mosaic/Create/MosaicCreate'

import NotFound from './Pages/404/404.js'
import Header from './Comps/Header/Header'
import Footer from './Comps/Footer/Footer'
import Examples from './Pages/Examples/Examples.js'
import MosaicFull from './Pages/Mosaic/View/Full.js'
import PiecelistCreate from './Pages/Piecelist/Create/PiecelistCreate'

import {ScrollToTop} from './Utils/routing.js'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <div>
    <ScrollToTop></ScrollToTop>
    <Header></Header>
    <Switch>
      <Route path="/" component={Home}></Route>
      <Route path="/about" component={About}></Route>
      <Route path="/examples" component={Examples}></Route>
      <Route path="/mosaic/create" component={MosaicCreate}></Route>
      <Route path="/mosaic/:uuid" component={MosaicFull}></Route>
      <Route path="/piecelist/create" component={PiecelistCreate}></Route>
      <Route code="404" component={NotFound}></Route>
    </Switch>
    <Footer></Footer>
  </div>
);




//https://css-tricks.com/piecing-together-approaches-for-a-css-masonry-layout/
