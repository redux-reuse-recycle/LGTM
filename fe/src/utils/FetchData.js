import { Data } from "../../data";

const fetchData = async () => {
  if (window.line_level_profile) return window.line_level_profile;

  if (process.env.NODE_ENV === "development") {
    return Promise.resolve(Data);
  }

  return fetch("static/data/line_level_profile.json").then(result =>
    result.json()
  );
};

export { fetchData };
