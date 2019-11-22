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
                const shadeValue = calculateShadeValue(i);
                styles += `
                    span:nth-of-type(${i}) {
                        background-color: ${view === "hits" ?
                    `rgba(0,0,180, ${shadeValue ? Math.max(shadeValue/2.5, 0.05) : 0})` :
                    `rgba(255,${(1 - shadeValue) * 255},0, ${shadeValue > 0.5 ? 0.5 : shadeValue})`};
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
                startingLineNumber={parseInt(file.lines[0].lineNumber)}
            >
                {codeString}
            </StyledSyntaxHighlighter>
        </div>
    );
};

export default CodeViewer;
