#!/usr/bin/env python3.6
import json
import os
import sys

import pprofile


class HeatMapProfiler:
    def __init__(self):
        self._profiler = pprofile.Profile()

    def __enter__(self):
        self._profiler.__enter__()

    def __exit__(self, *args, **kwargs):
        self._profiler.__exit__(*args, **kwargs)
        self._profile_data_to_json()

    def enable(self):
        self._profiler.enable()

    def disable(self):
        self._profiler.disable()
        self._profile_data_to_json()

    def run_file(self, file_path, argv=None):
        sys.path.append(file_path.rpartition('/')[0])
        self._profiler.runfile(open(file_path, "r"), argv or [], file_path)
        self._profile_data_to_json()

    def _profile_data_to_json(self):
        total_time = self._profiler.total_time

        if not total_time:
            return

        def percent(value, scale):
            if scale == 0:
                return 0
            return value * 100 / scale

        profile_data_to_json = {
            'total_time': total_time
        }

        file_dict = self._profiler._mergeFileTiming()

        for name in self._profiler._getFileNameList(None):
            if name[0] != '<' and os.path.dirname(os.__file__) not in name:
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


def heat_map(func):
    def wrapper():
        with HeatMapProfiler():
            func()
    return wrapper


if __name__ == '__main__':
    if len(sys.argv) > 1:
        profiler = HeatMapProfiler()
        profiler.run_file(sys.argv[1], sys.argv[1:])
    else:
        print('No target script specified.')
