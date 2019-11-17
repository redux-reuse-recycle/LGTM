import React from 'react';
import PropTypes from 'prop-types';

// TODO: Make this beautiful!
const File = (file) => (
  <div>
    <ol>
      { files.map((file) => <li> { file.name } </li>) }
    </ol>
  </div>
);


File.propTypes = {
  name: PropTypes.name.isRequired,
  // TODO: More Fields.
};

export default File;
