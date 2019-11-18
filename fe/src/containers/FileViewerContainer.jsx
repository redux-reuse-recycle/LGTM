import React from 'react';
import FileListProvider from './FileListProvider.jsx';
import FileViewer from '../components/FileViewer/FileViewer.jsx';
import Spinner from '../components/Spinner/Spinner.jsx';

const FileViewerContainer = () => (
    <FileListProvider
        Child={({ fileList, isLoaded }) => isLoaded ? <Spinner /> : <FileViewer fileList={fileList} />}
    />
);

export default FileViewerContainer;
