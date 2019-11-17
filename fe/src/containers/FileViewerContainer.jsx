import React from 'react';
import FileListProvider from './FileListProvider.jsx';
import FileViewer from '../components/FileViewer/FileViewer.jsx';

const FileViewerContainer = () => (
    <FileListProvider
        Child={FileViewer}
    />
);

export default FileViewerContainer;
