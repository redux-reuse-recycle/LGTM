import React from 'react';
import './Gradient.scss';

const Gradient = ({ file }) => (
    <div className="GradientContainer">
        <div className="GradientColour" />
        <div className="GradientTextContainer">
            <div className="GradientTextItem">0</div>
            <div className="GradientTextItem">100</div>
        </div>
    </div>
);

export default Gradient;
