import React from "react";
import { Link } from 'react-router-dom';
import Heart from "../Emoji/Heart";
import "./Header.scss";

const Header = () => (
  <div className="HeaderContainer">
      <Link to="/"><div className="HeaderTitle">LGTM Python Profiler</div></Link>
      <div className="HeaderSubtitle">
        Made with <Heart />
      </div>
  </div>
);

export default Header;
