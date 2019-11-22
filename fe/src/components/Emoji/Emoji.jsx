import React from "react";
import PropTypes from "prop-types";

const Emoji = ({ symbol, name }) => (
  <span role="img" aria-label={`${name} Emoji`}>
    {symbol}
  </span>
);

Emoji.propTypes = {
  symbol: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired
};

export default Emoji;
