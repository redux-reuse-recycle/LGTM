import { Data } from "../../data";

const fetchData = async () => {
  // TODO: Refactor to stream this data rather than importing directly.
  return Data;
};

export { fetchData };
