import React from 'react';
import styled from 'styled-components';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import './CodeViewer.scss';

const CodeViewer = ({ file }) => {
    if (!file) return null;
    const codeString = file.lines.map(line => line.lineText).join('\n');

    const maxHits = file.lines.slice().sort((line1, line2) => line2.hits - line1.hits)[0].hits;
    const maxTime = file.lines.slice().sort((line1, line2) => line2.time - line1.time)[0].time;

    const calculateShadeValue = (lineNumber) => {
        const hits = file.lines[lineNumber - 1].hits;
        if (hits === 0) return 0;
        return Math.max( Math.round(hits * 10) / 10, maxHits * 0.05 ).toFixed(2) / maxHits;
    };

    const StyledSyntaxHighlighter = styled(SyntaxHighlighter)`
        code:nth-of-type(2) {
          ${(() => {
            let styles = '';
            for (let i = 1; i <= file.lines.length; i++) {
                styles += `
                    span:nth-of-type(${i}) {
                        background-color: rgba(255,0,0, ${calculateShadeValue(i)});
                        display: block;
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
