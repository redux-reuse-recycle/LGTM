// Provides a known unified schema for the front-end
// So prop values can be decoupled from the BE output.


// Maps the given data to line objects with a known schema.
const mapDataToLines = (entries) => entries.map(([key, value]) => {
  const { hits, time, percent } = value;
  return {
    lineNumber: key,
    hits,
    time,
    timePerHit: value.time_per_hits,
    percent,
    lineText: value.line
  }
});

// Maps the given data to file objects with a known schema.
const mapDataToFiles = (data) => Object.entries(data).map(([key, value]) => {
  const { file_total_time, file_total_time_percent, ...lines } = value;
  return {
    name: key,
    totalTime: file_total_time,
    totalTimePercent: file_total_time_percent,
    lines: mapDataToLines(Object.entries(lines))
  }
});

export { mapDataToFiles, mapDataToLines };
