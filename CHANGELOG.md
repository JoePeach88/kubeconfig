**Full Changelog**: https://github.com/JoePeach88/kubeconfig/compare/1.0.0...1.1.0

New functions:
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

Modified existed function `store`
```
kubeconfig store --kubeconfig /path/to/kubeconfig --use
```
