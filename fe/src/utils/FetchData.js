import { Data } from "../../data";

const fetchData = async () => {
  if (process.env.NODE_ENV === "development") {
    return Promise.resolve(Data);
  }

  return fetch("static/data/line_level_profile.json").then(result =>
    result.json()
  );
};

export { fetchData };
