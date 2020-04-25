import os
import re
import subprocess


class SystemInfoCollector:
    info = {}

    def _get_network_info(self):
        info = re.finditer(
            r'(\w{2,7}): flags=\d{1,4}<(.*)>',
            subprocess.run(['ifconfig'], capture_output=True).stdout.decode(),
        )
        result = {iface.group(1): iface.group(2).split(',') for iface in info}
        self.info['interfaces'] = result

    def _get_default_route(self):
        process = subprocess.Popen(['ip', 'route'], stdout=subprocess.PIPE)
        self.info['default_route'] = subprocess.check_output(
            ['grep', 'default'], stdin=process.stdout
        ).decode()

    def _get_cpu_info(self):
        process = subprocess.Popen(['mpstat'], stdout=subprocess.PIPE)
        stats = str(subprocess.check_output(['grep', 'all'], stdin=process.stdout)).split()
        self.info['processor'] = {
            'usr': stats[0],
            'nice': stats[1],
            'sys': stats[2],
            'iowait': stats[3],
            'irq': stats[4],
            'soft': stats[5],
            'steal': stats[6],
            'guest': stats[7],
            'gnice': stats[8],
            'idle': stats[9],
        }

    def _get_process_info(self, pid: str):
        process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
        stats = subprocess.check_output(['grep', pid], stdin=process.stdout).decode().split('\n')

        for line in stats:
            line = line.split()
            if line[1] != pid:
                continue
            else:
                self.info['process_info'] = {
                    'user': line[0],
                    'pid': line[1],
                    '%cpu': line[2],
                    '%mem': line[3],
                    'vsz': line[4],
                    'rss': line[5],
                    'tty': line[6],
                    'stat': line[7],
                    'start': line[8],
                    'time': line[9],
                    'command': ' '.join(line[10:]),
                }
                return

        self.info['process_info'] = None

    def _get_process_list(self):
        self.info['process_list'] = subprocess.check_output(['ps', 'aux']).decode().split('\n')

    def _get_network_interface_stats(self):
        stats = subprocess.check_output(['netstat', '-i']).decode().split('\n')[2:]
        self.info['network_interface_stats'] = []
        for line in stats:
            line = line.split()
            self.info['network_interface_stats'].append(
                {
                    'interface': line[0],
                    'mtu': line[1],
                    'rx-ok': line[2],
                    'rx-err': line[3],
                    'rx-drp': line[4],
                    'rx-ovr': line[5],
                    'tx-ok': line[6],
                    'tx-err': line[7],
                    'tx-drp': line[8],
                    'tx-ovr': line[9],
                    'flags': line[10],
                }
            )

    def _get_cron_service_status(self):
        services = subprocess.check_output(['service', '--status-all']).decode().split('\n')
        for service in services:
            service = service.split()
            if 'cron' in service:
                if '+' in service:
                    self.info['cron_running'] = True
                else:
                    self.info['cron_running'] = False
                return

    def _get_port_status(self, port: str):
        process = subprocess.Popen(['ss', '-tulpn'], stdout=subprocess.PIPE)
        port_in_use = subprocess.check_output(
            ['grep', f'"tcp.*{port} "'], stdin=process.stdout
        ).decode()

        self.info['ports_in_use'] = {port: bool(port_in_use)}

    def _get_package_version(self, package: str):
        process = subprocess.Popen(['apt', 'show', package], stdout=subprocess.PIPE)
        version = (
            subprocess.check_output(['grep', f'Version:'], stdin=process.stdout)
            .decode()
            .split()[1]
        )

        self.info['package_versions'] = {package: version}

    def _get_files_in_path(self, path: str):
        process = subprocess.Popen(['ls', '-p', path], stdout=subprocess.PIPE)
        files = subprocess.check_output(['grep', '-v', '/'], stdin=process.stdout).decode().split()

        self.info['files'] = files

    def _get_current_directory(self):
        self.info['current_directory'] = os.getcwd()

    def _get_kernel_version(self):
        self.info['kernel_version'] = os.uname().release

    def _get_os_version(self):
        self.info['os_version'] = os.uname().version

    def get_data(self, params, **kwargs) -> dict:
        if 'all' in params or 'net_interfaces' in params:
            self._get_network_info()
        if 'all' in params or 'default_route' in params:
            self._get_default_route()
        if 'all' in params or 'cpu_state' in params:
            self._get_cpu_info()
        if 'all' in params or 'process_state' in params:
            self._get_process_info(kwargs['pid'])
        if 'all' in params or 'process_list' in params:
            self._get_process_list()
        if 'all' in params or 'cron_status' in params:
            self._get_cron_service_status()
        if 'all' in params or 'port_state' in params:
            self._get_port_status(kwargs['port'])
        if 'all' in params or 'package_ver' in params:
            self._get_package_version(kwargs['package'])
        if 'all' in params or 'files_list' in params:
            self._get_files_in_path(kwargs['path'])
        if 'all' in params or 'workdir' in params:
            self._get_current_directory()
        if 'all' in params or 'kernel_ver' in params:
            self._get_kernel_version()
        if 'all' in params or 'os_ver' in params:
            self._get_os_version()

        return self.info


