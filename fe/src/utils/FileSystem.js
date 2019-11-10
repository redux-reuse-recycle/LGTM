// A promisified interface for the Node FileSystem library.
import * as FS from 'fs';

// Returns true if the file exists at the file path, false otherwise.
const fileExists = (filePath) => new Promise((resolve) => FS.exists(filePath, resolve));

// Reads the contents of a file asynchronously into a buffer.
const readFile = (filePath) => new Promise((resolve, reject) =>
  FS.readFile(filePath, (error, buffer) => {
    return (error) ? reject(buffer) : resolve(buffer);
  })
);

const FileSystem = {
  fileExists,
  readFile
};

export default FileSystem;
