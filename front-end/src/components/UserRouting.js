import React from "react";
import {BrowserRouter as Router,Routes, Route } from "react-router-dom";
import Home from "./Home";
import Details,{ResultRouter} from "./Details";
import Navbar from "./Navbar";
import About from "./About";
import Cluster from "./Cluster";
// import Dashboard from "./Dashboard";
// import Skills from "./Skills";
import Filter from "./Filter";
export default function UserRouting(){
    return(
        
        <>
        <Navbar />
            <Routes>
                <Route path="/home" element={<Home />}></Route>
                <Route path="/details" element={<ResultRouter />}></Route>
                <Route path="/about" element={<About/>}></Route>
                <Route path="/cluster" element={<Cluster/>}></Route>
                {/* <Route path="/dashboard" element={<Dashboard/>}></Route> */}
                {/* <Route path='/skills' element={<Skills/>}></Route> */}
                <Route path='/filter' element={<Filter/>}></Route>
            </Routes>
        </>
    )
}