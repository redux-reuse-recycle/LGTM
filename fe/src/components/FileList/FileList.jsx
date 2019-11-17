import React from "react";
import PropTypes from "prop-types";

// TODO: Make this beautiful!
const FileList = ({ files }) => (
  <div>
    <ol>
      {files.map(file => (
        <li key={file.name}> {file.name} </li>
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
