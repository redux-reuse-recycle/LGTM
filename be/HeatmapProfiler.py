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
        line_level_profile_data = self._profiler.file_dict[self._file.path][0].line_dict

        test = self._profiler.file_dict[self._file.path][0].getCallListByLine()
        
        line_profile_data_to_json = {}
        profile_data_to_json = {}

        for line_num in range(1, self._file.get_line_count() + 1): # TODO: double check line count
            line_profile_data = {}

            if line_num in line_level_profile_data:
                line_times = [
                    line_time for _, line_time in line_level_profile_data[line_num].values()
                ]
                line_profile_data["time"] = sum(line_times)

            else:
                line_profile_data["time"] = 0

            line_profile_data_to_json[line_num] = line_profile_data

        profile_data_to_json[self._file.path] = line_profile_data_to_json

        with open('line_level_profile.json', 'w', encoding='utf-8') as f:
            json.dump(profile_data_to_json, f, ensure_ascii=False, indent=4)

def main():
    heatmap_profiler = HeatmapProfiler("./test/one_file.py")
    heatmap_profiler.profile()

if __name__ == '__main__':
    main()

