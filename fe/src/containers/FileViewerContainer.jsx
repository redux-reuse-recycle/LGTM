import React, { useState } from 'react';
import FileListProvider from './FileListProvider.jsx';
import FileViewer from '../components/FileViewer/FileViewer.jsx';
import ViewToggle from '../components/ViewToggle/ViewToggle.jsx';
import Spinner from '../components/Spinner/Spinner.jsx';

const FileViewerContainer = () => {
    const [view, setView] = useState('none');

    return (
        <div>
            <ViewToggle setView={setView} view={view} />
            <FileListProvider
                Child={({fileList, isLoaded}) => !isLoaded ? <Spinner/> : <FileViewer fileList={fileList} view={view} />}
            />
        </div>
    );
};

export default FileViewerContainer;
