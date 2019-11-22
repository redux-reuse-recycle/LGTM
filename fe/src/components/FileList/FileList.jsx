import React from "react";
import { Link } from 'react-router-dom';
import PropTypes from "prop-types";
import './FileList.scss';

const FileList = ({ files }) => (
  <div className="FileListContainer">
        <div className="FileListTitle">Project Files</div>
        <div className="FileList">
          {files.map(file => (
              <Link to={`/file/${btoa(file.name)}`}>
                 <div className="FileListItem" key={file.name}> {file.name} </div>
              </Link>
          ))}
        </div>
  </div>
);

FileList.propTypes = {
  files: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired
    })
  ).isRequired
};

export default FileList;
