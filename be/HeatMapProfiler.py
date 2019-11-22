#!/usr/bin/env python3.6
import argparse
import datetime
import json
import os
import sys
import http.server
import socketserver
import webbrowser
from shutil import copyfile

import pprofile

PORT = 8000
SERVER_DIRECTORY = '../fe/'
DEFAULT_DIRECTORY = SERVER_DIRECTORY + '/build/static/data/'
DEFAULT_FILEPATH = DEFAULT_DIRECTORY + 'line_level_profile.json'

def _open_in_browser(port = PORT):
    webbrowser.open_new_tab(f'http://localhost:{port}/build/index.html')

def _start_server(port = PORT):
    os.chdir(SERVER_DIRECTORY)
    Handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            _open_in_browser(port)
            httpd.serve_forever()
    except OSError:
        _start_server(port + 1)
    except KeyboardInterrupt:
        httpd.server_close()

class HeatMapProfiler:
    def __init__(self, sample_mode=False, thread_mode=False, period=0.01):
        self._sample_mode = sample_mode

        if sample_mode:
            self._profiler = pprofile.StatisticThread(
                single=not thread_mode, period=period)
        elif thread_mode:
            self._profiler = pprofile.ThreadProfile()
        else:
            self._profiler = pprofile.Profile()

    def __call__(self):
        return self

    def __enter__(self):
        self._profiler.__enter__()

    def __exit__(self, *args, **kwargs):
        self._profiler.__exit__(*args, **kwargs)
        self._profile_data_to_json()
        _open_in_browser()

    def enable(self):
        if self._sample_mode:
            self._profiler.start()
        else:
            self._profiler.enable()

    def disable(self):
        if self._sample_mode:
            self._profiler.stop()
        else:
            self._profiler.disable()
        self._profile_data_to_json()
        _open_in_browser()

    def run_file(self, file_path, argv=None):
        sys.path.append(file_path.rpartition('/')[0])
        self._profiler.runfile(open(file_path, "r"), argv or [], file_path)
        self._profile_data_to_json()
        _open_in_browser()

    def _profile_data_to_json(self):
        if self._sample_mode:
            self._profiler = self._profiler.profiler

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
        cur_path = os.path.dirname(__file__)

        for name in self._profiler._getFileNameList(None):
            if name and name[0] != '<' and name != __file__:
                file_timing = file_dict[name]
                name = os.path.relpath(name, cur_path)
                if name[:2] == '..':
                    continue

                file_total_time = file_timing.getTotalTime()
                profile_data_to_json[name] = {"file_total_time": file_total_time,
                                              "file_total_time_percent": percent(file_total_time, total_time)}

                last_line = file_timing.getLastLine()
                first_hit = 0
                last_hit = 0
                for lineno, line in pprofile.LineIterator(
                        self._profiler._getline,
                        file_timing.filename,
                        file_timing.global_dict,
                ):
                    if not line and lineno > last_line:
                        break
                    hits, duration = file_timing.getHitStatsFor(lineno)
                    if not first_hit and hits:
                        first_hit = last_hit = lineno
                    elif hits:
                        last_hit = lineno
                    profile_data_to_json[name][lineno] = {
                        'hits': hits,
                        'time': duration,
                        'time_per_hit': duration / hits if hits else 0,
                        'percent': percent(duration, total_time),
                        'line': (line or '').rstrip(),
                    }

                profile_data_to_json[name] = {
                    key: value for key, value in profile_data_to_json[name].items()
                    if type(key) == str or first_hit <= int(key) <= last_hit
                }

        os.makedirs(DEFAULT_DIRECTORY, exist_ok=True)
        with open(DEFAULT_FILEPATH, 'w', encoding='utf-8') as f:
            json.dump(profile_data_to_json, f, ensure_ascii=False, indent=4)


def heat_map(sample_mode=False, thread_mode=False, period=0.01):
    def wrap(func):
        def wrapper(*args, **kwargs):
            with HeatMapProfiler(sample_mode, thread_mode, period):
                return func(*args, **kwargs)
        return wrapper
    return wrap


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs='?',
                        help='Path to the target python script to run with the profiler.')
    parser.add_argument('-d', '--display', type=str, default='',
                        help='Path to existing json profiler data file to display.'
                             ' The profiler will not be run, and any existing profiler data'
                             ' (from a previous run without the export flag) will be overwritten.')
    parser.add_argument('-e', '--export', type=str, default='',
                        help='Output path for json profiler data file.')
    parser.add_argument('-p', '--period', type=float, default=0.001,
                        help='Only has an effect in sample mode. Number of seconds to wait between'
                             ' consecutive samples.')
    parser.add_argument('-s', '--sample', action='store_true', default=False,
                        help='Run profiler in sample mode. This will drastically improve'
                             ' performance, but no timing information will be generated.')
    parser.add_argument('-t', '--thread', action='store_true', default=False,
                        help='Run profiler in thread-aware mode. Any threading.Thread threads'
                             ' created will be included in the profiler data.')
    parser.add_argument('-v', '--view', action='store_true', default=False,
                        help='View only flag. The profiler will not be run and the results'
                             'from the last profiler run will be displayed.')
    args, argv = parser.parse_known_args()

    if args.display:
        print(f'Displaying {args.display}')
        if not args.display.endswith(".json"):
            print(f"Warning: displaying a non-JSON file: {args.display}")
        copyfile(args.display, DEFAULT_FILEPATH)
    elif not args.view and args.target:
        profiler = HeatMapProfiler(
            sample_mode=args.sample, thread_mode=args.thread, period=args.period)
        profiler.run_file(args.target, [args.target] + argv)

    if args.export:
        print(f'Exporting to {args.export}')
        if os.path.isdir(args.export):
            copyfile(DEFAULT_FILEPATH, args.export + f'line_level_profile{datetime.datetime.now().isoformat()}.json')
        else:
            if os.path.exists(args.export):
                print(f"Warning: overwriting existing file: {args.export}")
            if not args.export.endswith(".json"):
                print(f"Warning: writing to a non-JSON file: {args.export.split('.')[-1]}")
            copyfile(DEFAULT_FILEPATH, args.export)

    _start_server()
