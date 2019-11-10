import FileSystem from 'utils/FileSystem';
import { path as Path } from 'path';

const dataPath = Path.join(__dirname, "data.json");
const mockDataPath = Path.join(__dirname, "mockData.json");

const fetchData = async () => {
  const fileToRead = (await FileSystem.fileExists()) ? dataPath : mockDataPath;
  const fileJSON = await FileSystem.readFile(fileToRead);
  return JSON.parse(fileJSON.toString());
}

export { fetchData };
