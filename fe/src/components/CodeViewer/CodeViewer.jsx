import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import './CodeViewer.scss';

const CodeViewer = () => {

    const codeString = '(num) => num + 1';

    return (
        <SyntaxHighlighter language="python">
            {codeString}
        </SyntaxHighlighter>
    );

};

export default CodeViewer;
