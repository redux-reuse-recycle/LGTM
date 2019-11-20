import React from 'react';
import cx from 'classnames';
import './ViewToggle.scss';

const ViewToggle = ({ view, setView }) => (
    <div className="ViewToggleContainer">
        <div className={cx(
            'ViewToggleItem',
            {
                'ViewToggleItem--Selected': view === 'hits',
            }
        )} onClick={() => setView('hits')} >
            Hits
        </div>
        <div className={cx(
            'ViewToggleItem',
            {
                'ViewToggleItem--Selected': view === 'time',
            }
        )} onClick={() => setView('time')} >
            Time
        </div>
        <div className={cx(
            'ViewToggleItem',
            {
                'ViewToggleItem--Selected': view === 'none',
            }
        )} onClick={() => setView('none')} >
            None
        </div>
    </div>
);

export default ViewToggle;
