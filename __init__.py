import shutil
import os
import glob
import yaml
from pathlib import Path
from helpers import print_message, print_choices, ERROR, SUCCESS
from helpers.kubeconfig.utils import set_env_variable


# Module global settings
__module_disabled_methods__ = []
__module_name__ = 'KubeConfigHelper'
__module_author__ = 'JoePeach88'
__module_version__ = '1.1.1'
__module_link__ = 'https://github.com/JoePeach88/kubeconfig'
__module_category__ = ['development', 'devops', 'k8s']
__module_compatibility__ = ['all']
__module_dependencies__ = [{}]
__module_status__ = 'stable'
__methods_static_aliases__ = {
    'ls': ['ll', 'list'],
    'store': ['save'],
    'rm': ['remove', 'delete', 'drop'],
    'use': ['set'],
    'validate': ['check', 'syntax'],
    'show': ['print']
}


class kubeconfigHelper:
    """
    Module to work with kubeconfigs.
    """
    def __init__(self, settings: dict):
        self.settings = settings.get('kubeconfig')

    def store(self, kubeconfig: str, dest: str = None, use: bool = False):
        """
        Method stores kubeconfig to specified location `dest` or to default kubeconfigs location from config file.
        Usage:
            1. Without specified location (to default kubeconfigs location):
                kubeconfig store --kubeconfig /path/to/kubeconfig
            2. With specified location
                kubeconfig store --kubeconfig /path/to/kubeconfig --dest /path/to/save/kubeconfig
            3. Store and use stored kubeconfig.
                kubeconfig store --kubeconfig /path/to/kubeconfig --use
        """
        try:
            dest_path = Path(self.settings.get('kubeconfigs_locations', ''))
            if not dest_path:
                dest_path = Path.home() / '.kube'
            dest_path = Path(dest) if dest else dest_path
            dest_path = Path(dest_path / Path(kubeconfig).name)
            shutil.copy2(kubeconfig, dest_path)
            print_message(f"kubeconfig '{kubeconfig}' copied to '{dest_path}' successfully.", SUCCESS)
            if use:
                self.use(str(dest_path))
        except FileNotFoundError:
            print_message(f"The source file '{kubeconfig}' was not found.", ERROR)
        except PermissionError:
            print_message(f"Permission denied. Cannot copy file to '{dest_path}'.", ERROR)
        except Exception as e:
            print_message(f"An unexpected error occurred: {e}", ERROR)

    def ls(self, pretty: bool = True, location: str = 'all'):
        """
        Method displays all available kubeconfigs from all known kubeconfigs locations.
        Usage:
            kubeconfig ls
        """
        kubeconfig_list = []
        locations = location.split(',')
        if 'env' in locations or 'all' in locations:
            # Check KUBECONFIG environment variable
            kubeconfig_env = os.getenv('KUBECONFIG')
            if kubeconfig_env:
                print_message("Found kubeconfigs in env variable KUBECONFIG.")
                separator = ';' if os.name == 'nt' else ':'
                paths = kubeconfig_env.split(separator)

                for path_str in paths:
                    path = Path(path_str.strip().strip(separator)).expanduser().resolve()
                    if path.exists() and path.is_file() and str(path) not in kubeconfig_list:
                        kubeconfig_list.append(str(path))

        if 'default' in locations or 'all' in locations:
            # Check default location
            default_config = Path.home() / '.kube' / 'config'
            if default_config.exists() and default_config.is_file():
                print_message(f"Found kubeconfigs in default location: '{str(default_config)}'.")
                if str(default_config) not in kubeconfig_list:
                    kubeconfig_list.append(str(default_config))

        if 'kubeconfigs_locations' in locations or 'all' in locations:
            # Check settings location
            if self.settings and self.settings.get('kubeconfigs_locations'):
                kubeconfigs_locations = self.settings.get('kubeconfigs_locations')
                kubeconfigs = set()
                for kubeconfigs_location in kubeconfigs_locations.split(','):
                    kubeconfigs.update(glob.glob(os.path.join(Path(kubeconfigs_location), "*.yaml")))
                if kubeconfigs:
                    print_message(f"Found kubeconfigs in settings kubeconfigs locations: '{str(kubeconfigs_locations)}'.")
                    for kubeconfig in kubeconfigs:
                        if kubeconfig not in kubeconfig_list:
                            kubeconfig_list.append(kubeconfig)

        return f'Available kubeconfigs ({len(kubeconfig_list)}):\n' + '\n'.join(kubeconfig_list) if pretty else kubeconfig_list

    def use(self, kubeconfig: str = None):
        """
        Method sets kubeconfig which will be used in future in kubectl, it sets selected kubeconfig to env variable.
        NOTE: This command restarts all parent process to refresh env variables (Windows only).
        Usage:
            1. With prompt to select available kubeconfigs.
                kubeconfig use
            2. With specified kubeconfig.
                kubeconfig use --kubeconfig /path/to/kubeconfig
        """
        if not kubeconfig:
            kubeconfig_list = self.ls(pretty=False)
            kubeconfig = print_choices(kubeconfig_list, exit_btn=True)
        if kubeconfig:
            separator = ';' if os.name == 'nt' else ':'
            current_kubeconfig = os.environ.get('KUBECONFIG', '').split(separator)
            if kubeconfig not in current_kubeconfig:
                current_kubeconfig.append(kubeconfig)
            kubeconfigs = current_kubeconfig
            for kubeconfig in kubeconfigs:
                if not kubeconfig:
                    kubeconfigs.remove(kubeconfig)
            set_env_variable('KUBECONFIG', separator.join(kubeconfigs))
            print_message(f"KUBECONFIG variable successfully set to '{separator.join(kubeconfigs)}'", SUCCESS)

    def rm(self, kubeconfig: str = None, location: str = 'env', force: str = False):
        """
        Method removes kubeconfig from env variable KUBECONFIG.
        NOTE: This command restarts all parent process to refresh env variables (Windows only).
        Usage:
            1. With prompt to select available kubeconfigs.
                kubeconfig rm
            2. With specified kubeconfig.
                kubeconfig rm --kubeconfig /path/to/kubeconfig
            3. Remove kubeconfig file.
                kubeconfig rm --force
        """
        if not kubeconfig:
            kubeconfig_list = self.ls(pretty=False, location=location)
            kubeconfig = print_choices(kubeconfig_list, exit_btn=True)
        if kubeconfig:
            if force:
                os.unlink(kubeconfig)
                print_message(f"kubeconfig file '{kubeconfig}' deleted.", SUCCESS)
            separator = ';' if os.name == 'nt' else ':'
            current_kubeconfig = os.environ.get('KUBECONFIG', '').split(separator)
            if kubeconfig in current_kubeconfig:
                current_kubeconfig.remove(kubeconfig)
                kubeconfigs = current_kubeconfig
                for kubeconfig in kubeconfigs:
                    if not kubeconfig:
                        kubeconfigs.remove(kubeconfig)
                set_env_variable('KUBECONFIG', separator.join(kubeconfigs))
                print_message(f"KUBECONFIG variable successfully set to '{separator.join(kubeconfigs)}'", SUCCESS)
            else:
                print_message(f"kubeconfig '{kubeconfig}' not found in KUBECONFIG variable.", force=True)

    def validate(self, kubeconfig: str = None, location: str = 'env', return_value: bool = False):
        """
        Method validates kubeconfig.
        Usage:
            kubeconfig validate --kubeconfig /path/to/kubeconfig
        """
        if not kubeconfig:
            kubeconfig_list = self.ls(pretty=False, location=location)
            kubeconfig = print_choices(kubeconfig_list, exit_btn=True)
        if kubeconfig:
            try:
                with open(kubeconfig, 'r', encoding='utf-8') as stream:
                    data = yaml.safe_load(stream)
                    if return_value:
                        return yaml.dump(data)
                return f"kubeconfig '{kubeconfig}' is valid."
            except yaml.YAMLError:
                return f"kubeconfig '{kubeconfig}' is invalid."

    def show(self, *args, kubeconfig: str = None):
        """
        Method displays kubeconfig content.
        Usage:
            1. With prompt to select available kubeconfigs.
                kubeconfig show
            2. With specified kubeconfig.
                kubeconfig show --kubeconfig /path/to/kubeconfig
            3. With specified kubeconfig and data to return.
                kubeconfig show --kubeconfig /path/to/kubeconfig clusters users
        """
        if not kubeconfig and not args:
            kubeconfig_list = self.ls(pretty=False)
            kubeconfig = print_choices(kubeconfig_list, exit_btn=True)
        elif not kubeconfig and args:
            kubeconfig = args[0]
            args = list(args)
            args.pop(0)
            args = tuple(args)
        if kubeconfig:
            kubeconfig_data = self.validate(kubeconfig, return_value=True)
            if not args:
                return kubeconfig_data
            else:
                kubeconfig_data = yaml.safe_load(kubeconfig_data)
                kubeconfig_return_data = {}
                for arg in args:
                    if kubeconfig_data.get(arg):
                        kubeconfig_return_data.update({arg: kubeconfig_data.get(arg)})
                if kubeconfig_return_data:
                    return yaml.dump(kubeconfig_return_data)
