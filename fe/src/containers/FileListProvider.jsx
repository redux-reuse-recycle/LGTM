import React from "react";
import { fetchData } from "../utils/FetchData";
import { mapDataToFiles } from "../utils/MapData";

// Retrieves the data dumped from the JSON asynchronously.
const FileListProvider = ({ Child }) => {
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [fileList, setFileList] = React.useState([]);

  React.useEffect(() => {
    fetchData()
      .then(data => mapDataToFiles(data))
      .then(data => setFileList(mapDataToFiles(data)))
      .then(() => setIsLoaded(true));
  }, []);

  return <Child isLoaded={isLoaded} fileList={fileList} />;
};

export default FileListProvider;
