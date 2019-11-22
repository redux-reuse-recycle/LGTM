import React from 'react';
import { Link } from 'react-router-dom';
import { useParams } from "react-router";
import cx from 'classnames';
import './ViewToggle.scss';

const ViewToggle = ({ view, setView, fileList }) => {
    let { fileName } = useParams();
    fileName = atob(fileName);
    const file = fileList.find((file) => file.name === fileName);

    return (
        <>
            <div className="ViewToggleTop">
                <div>
                    {file && file.name}
                </div>
                <Link to="/">
                    <div className="ViewAllFiles">View All Files</div>
                </Link>
            </div>
            <div className="ViewToggleContainer">
                <div className={cx(
                    'ViewToggleItem',
                    {
                        'ViewToggleItem--Selected': view === 'hits',
                    }
                )} onClick={() => setView('hits')}>
                    Hits
                </div>
                <div className={cx(
                    'ViewToggleItem',
                    {
                        'ViewToggleItem--Selected': view === 'time',
                    }
                )} onClick={() => setView('time')}>
                    Time
                </div>
                <div className={cx(
                    'ViewToggleItem',
                    {
                        'ViewToggleItem--Selected': view === 'none',
                    }
                )} onClick={() => setView('none')}>
                    None
                </div>
            </div>
        </>
    );
};

export default ViewToggle;
