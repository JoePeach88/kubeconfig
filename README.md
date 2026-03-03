# kubeconfig

Module for work with kubeconfigs.

## Methods

### store

```
Method stores kubeconfig to specified location `dest` or to default kubeconfigs location from config file.
Usage:
    1. Without specified location (to default kubeconfigs location):
        kubeconfig store --kubeconfig /path/to/kubeconfig
    2. With specified location
        kubeconfig store --kubeconfig /path/to/kubeconfig --dest /path/to/save/kubeconfig
    3. Store and use stored kubeconfig.
        kubeconfig store --kubeconfig /path/to/kubeconfig --use
```

### ls

```
Method displays all available kubeconfigs from all known kubeconfigs locations.
Usage:
    kubeconfig ls
```

### use

```
Method sets kubeconfig which will be used in future in kubectl, it sets selected kubeconfig to env variable.
NOTE: This command restarts all parent process to refresh env variables (Windows only).
Usage:
    1. With prompt to select available kubeconfigs.
        kubeconfig use
    2. With specified kubeconfig.
        kubeconfig use --kubeconfig /path/to/kubeconfig
```

### rm

```
Method removes kubeconfig from env variable KUBECONFIG.
NOTE: This command restarts all parent process to refresh env variables (Windows only).
Usage:
    1. With prompt to select available kubeconfigs.
        kubeconfig rm
    2. With specified kubeconfig.
        kubeconfig rm --kubeconfig /path/to/kubeconfig
    3. Remove kubeconfig file.
        kubeconfig rm --force
```

### validate

```
Method validates kubeconfig.
Usage:
    kubeconfig validate --kubeconfig /path/to/kubeconfig
```

### show

```
Method displays kubeconfig content.
Usage:
    1. With prompt to select available kubeconfigs.
        kubeconfig show
    2. With specified kubeconfig.
        kubeconfig show --kubeconfig /path/to/kubeconfig
    3. With specified kubeconfig and data to return.
        kubeconfig show --kubeconfig /path/to/kubeconfig clusters users
```
