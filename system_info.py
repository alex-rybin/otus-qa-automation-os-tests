import argparse

from info_collector import SystemInfoCollector

parser = argparse.ArgumentParser()

parser.add_argument('--pid', required=True, help='PID to show info about')
parser.add_argument('--port', default='8000', help='Port to show state of or test')
parser.add_argument('--package', required=True, help='Package name to show version of.')
parser.add_argument(
    '--path',
    required=True,
    help='Path to show files from. Necessary if files_list or all params selected',
)

args = parser.parse_args()

data = SystemInfoCollector().get_data(
    pid=args.pid, package=args.package, path=args.path, port=args.port
)

for data_field in data:
    if isinstance(data[data_field], dict):
        print(f'{data_field}:')
        for key, value in data[data_field].items():
            print(f'{key}: {value}')
        print()

    elif isinstance(data[data_field], list):
        print(f'{data_field}:')
        for value in data[data_field]:
            print(value)
        print()

    else:
        print(f'{data_field}: {data[data_field]}\n')
