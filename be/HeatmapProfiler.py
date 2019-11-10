#!/usr/bin/env python3
import pprofile
import json


class HeatmapProfiler:
    class FileMetadata:

        def get_line_count(self):
            with open(self.path) as f:
                for i, l in enumerate(f):
                    pass
            return i + 1

        """
        @param path: The file path
        """
        def __init__(self, path):
            self.path = path
            self.length = self.get_line_count()
            self.data = None

    def __init__(self, path):
        """
        @param path: The file path to be profiled
        """
        self._file = HeatmapProfiler.FileMetadata(path)
        self._profiler = pprofile.Profile()

    def profile(self):
        self._profile_file()
        self._profile_data_to_json()

    def _profile_file(self):
        self._profiler.runfile(open(self._file.path, mode="r"), {}, self._file.path)

    def _profile_data_to_json(self):
        profile_data_to_json = {}

        file_dict = self._profiler._mergeFileTiming()
        total_time = self._profiler.total_time
        profile_data_to_json["total_time"] = total_time

        if not total_time:
            return

        def percent(value, scale):
            if scale == 0:
                return 0
            return value * 100 / scale

        for name in self._profiler._getFileNameList(None):
            profile_data_to_json = {}

            file_timing = file_dict[name]
            file_total_time = file_timing.getTotalTime()
            profile_data_to_json[name] = {"file_total_time": file_total_time,
                                          "file_total_time_percent": percent(file_total_time, total_time)}

            last_line = file_timing.getLastLine()
            for lineno, line in pprofile.LineIterator(
                    self._profiler._getline,
                    file_timing.filename,
                    file_timing.global_dict,
            ):
                if not line and lineno > last_line:
                    break
                hits, duration = file_timing.getHitStatsFor(lineno)
                profile_data_to_json[name][lineno] = {
                    'hits': hits,
                    'time': duration,
                    'time_per_hit': duration / hits if hits else 0,
                    'percent': percent(duration, total_time),
                    'line': (line or '').rstrip(),
                }

        with open('line_level_profile.json', 'w', encoding='utf-8') as f:
            json.dump(profile_data_to_json, f, ensure_ascii=False, indent=4)

def main():
    heatmap_profiler = HeatmapProfiler("./test/one_file.py")
    heatmap_profiler.profile()

if __name__ == '__main__':
    main()

