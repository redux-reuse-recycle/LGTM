import React from "react";
import Heart from "../Emoji/Heart";
import "./Header.scss";

const Header = () => (
  <div className="HeaderContainer">
    <div className="HeaderTitle">LGTM</div>
    <div className="HeaderSubtitle">
      Made with <Heart />
    </div>
  </div>
);

export default Header;
