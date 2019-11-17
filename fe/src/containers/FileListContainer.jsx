import React from "react";
import FileListProvider from "./FileListProvider";
import FileList from "../components/FileList/FileList";
import Spinner from "../components/Spinner/Spinner";

const FileListContainer = () => (
  <FileListProvider
    child={({ isLoaded, fileList }) =>
      !isLoaded ? <Spinner /> : <FileList files={fileList} />
    }
  />
);

export default FileListContainer;
