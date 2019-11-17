import React from "react";
import PropTypes from "prop-types";
import "./Home.scss";

const Home = ({ children }) => {
  return (
    <div className="HomeContainer">
      <div>{children}</div>
    </div>
  );
};

Home.propTypes = {
  children: PropTypes.node.isRequired
};

export default Home;
