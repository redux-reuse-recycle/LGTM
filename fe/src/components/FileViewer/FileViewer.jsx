import React from 'react';
import { useParams } from "react-router";
import { Redirect } from 'react-router-dom';
import CodeViewer from '../CodeViewer/CodeViewer.jsx';
import './FileViewer.scss';

const FileViewer = ({ fileList, isLoaded }) => {
    let { fileName } = useParams();
    fileName = atob(fileName);
    const file = fileList.find((file) => file.name === fileName);

    if ((!fileName || !file) && isLoaded) return <Redirect to="/" />;
    return <CodeViewer file={file} />;
};

export default FileViewer;
