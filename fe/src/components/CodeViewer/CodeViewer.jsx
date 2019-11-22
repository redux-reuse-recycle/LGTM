import React from 'react';
import styled from 'styled-components';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import './CodeViewer.scss';

const CodeViewer = ({ file, view }) => {
    if (!file) return null;
    const codeString = file.lines.map(line => line.lineText).join('\n');

    const linesSortedByHits = file.lines.slice().sort((line1, line2) => line2.hits - line1.hits);
    const linesSortedByTime = file.lines.slice().sort((line1, line2) => line2.time - line1.time);

    const maxHits = (linesSortedByHits && linesSortedByHits[0] && linesSortedByHits[0].hits) || 0;
    const maxTime = (linesSortedByTime && linesSortedByTime[0] && linesSortedByTime[0].time) || 0;

    const calculateShadeValue = (lineNumber) => {
        if (view === 'hits') {
            const hits = (file.lines && file.lines[lineNumber - 1] && file.lines[lineNumber - 1].hits) || 0;
            if (hits === 0) return 0;
            return hits / maxHits;
        } else if (view === 'time') {
            const time = (file.lines && file.lines[lineNumber - 1] && file.lines[lineNumber - 1].time) || 0;
            if (time === 0) return 0;
            return time / maxTime;
        } else {
            return 0;
        }
    };

    const StyledSyntaxHighlighter = styled(SyntaxHighlighter)`
        code:nth-of-type(2) {
          ${(() => {
            let styles = '';
            for (let i = 1; i <= file.lines.length; i++) {
                styles += `
                    span:nth-of-type(${i}) {
                        background-color: ${view === "hits" ? `rgba(255,0,0, ${calculateShadeValue(i)})` : `rgba(0,0,255, ${calculateShadeValue(i)})`};
                        display: block;
                        text-shadow: none !important;
                        span {
                            display: initial;
                            background-color: initial;
                        }
                    }
                `;
            }
            return styles
            })()}
        }
   `;

    return (
        <div className="CodeViewerContainer">
            <StyledSyntaxHighlighter
                language="python"
                showLineNumbers
                wrapLines
            >
                {codeString}
            </StyledSyntaxHighlighter>
        </div>
    );
};

export default CodeViewer;
