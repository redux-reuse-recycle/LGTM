import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import './CodeViewer.scss';

const CodeViewer = ({ file }) => {
    if (!file) return null;
    const codeString = file.lines.map(line => line.lineText).join('\n');

    return (
        <div className="CodeViewerContainer">
            <SyntaxHighlighter
                language="python"
                showLineNumbers
            >
                {codeString}
            </SyntaxHighlighter>
        </div>
    );
};

export default CodeViewer;
