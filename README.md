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
Usage:
    1. With prompt to select available kubeconfigs.
        kubeconfig use
    2. With specified kubeconfig.
        kubeconfig use --kubeconfig /path/to/kubeconfig
```

### rm

```
Method removes kubeconfig from env variable KUBECONFIG.
Usage:
    kubeconfig rm --kubeconfig /path/to/kubeconfig
```
