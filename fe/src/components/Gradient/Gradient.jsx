import React from 'react';
import { useParams } from "react-router";
import cx from 'classnames';
import './Gradient.scss';

const Gradient = ({ fileList, view }) => {
    let { fileName } = useParams();
    fileName = atob(fileName);
    const file = fileList.find((file) => file.name === fileName);

    const maxHits = file.lines.slice().sort((line1, line2) => line2.hits - line1.hits)[0].hits;
    const maxTime = file.lines.slice().sort((line1, line2) => line2.time - line1.time)[0].time;

    let maxCount = 0;
    if (view === "hits") maxCount = maxHits;
    if (view === "time") maxCount = maxTime;

    if (view === "none") return null;
    return (
        <div className="GradientContainer">
            <div className={cx(
                "GradientColour",
                {
                    "GradientColour--blue": view === 'time',
                    "GradientColour--red": view === 'hits',
                }
            )}/>
            <div className="GradientTextContainer">
                <div className="GradientTextItem">0</div>
                <div className="GradientTextItem">{maxCount}</div>
            </div>
        </div>
    );
};

export default Gradient;
