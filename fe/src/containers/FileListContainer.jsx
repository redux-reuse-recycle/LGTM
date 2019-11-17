import React from "react";
import FileListProvider from "./FileListProvider";
import FileList from "../components/FileList/FileList";
import Spinner from "../components/Spinner/Spinner";

const FileListContainer = () => (
  <FileListProvider
    Child={({ isLoaded, fileList }) =>
      !isLoaded ? <Spinner /> : <FileList files={fileList} />
    }
  />
);

export default FileListContainer;
