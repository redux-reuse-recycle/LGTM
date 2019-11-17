import React from "react";
import { Link } from 'react-router-dom';
import PropTypes from "prop-types";

// TODO: Make this beautiful!
const FileList = ({ files }) => (
  <div>
    <ol>
      {files.map(file => (
          <Link to={`/file/${btoa(file.name)}`}><li key={file.name}> {file.name} </li></Link>
      ))}
    </ol>
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
