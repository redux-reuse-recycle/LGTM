import { Data } from "../../data";

const fetchData = async () => {
<<<<<<< HEAD
  // TODO: Refactor to stream this data rather than importing directly.
  return window.line_level_profile || Data;
=======
  if (process.env.NODE_ENV === "development") {
    return Promise.resolve(Data);
  }

  return fetch("static/data/line_level_profile.json").then(result =>
    result.json()
  );
>>>>>>> db2a3e137e61963a51d2a9debd39d6096be3d6ef
};

export { fetchData };
