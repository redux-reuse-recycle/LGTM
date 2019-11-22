import { Data } from "../../data";

const fetchData = async () => {
  if (window.line_level_profile) return JSON.parse(window.line_level_profile);

  return Data;
};

export { fetchData };
