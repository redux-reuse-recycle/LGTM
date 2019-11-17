import React from "react";
import Heart from "../Emoji/Heart";
import "./Footer.scss";

const Footer = () => (
  <div className="FooterContainer">
    <div className="FooterTitle">LGTM</div>
    <div className="FooterSubtitle">
      Made with <Heart />
    </div>
  </div>
);

export default Footer;
