import React from "react";
import Spinner from "../components/Spinner/Spinner";
import FileList from "../components/FileList/FileList";
import { fetchData } from "../utils/FetchData";
import { mapDataToFiles } from "../utils/MapData";

// Retrieves the data dumped from the JSON asynchronously.
const FileListContainer = () => {
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [fileList, setFileList] = React.useState([]);

  React.useEffect(() => {
    fetchData()
      .then(data => mapDataToFiles(data))
      .then(data => setFileList(mapDataToFiles(data)))
      .then(() => setIsLoaded(true));
  }, []);

  return !isLoaded ? <Spinner /> : <FileList files={fileList} />;
};

export default FileListContainer;
