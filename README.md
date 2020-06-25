# Logbook Cache for Home Assistant

Custom component to speed up Home Assistant logbook viewing.

This works by keeping filtered results preloaded and updated in memory. The effect is most significant with slow hardware such as Raspberry Pi.

Caveats:
- the cache takes some time (maybe several minutes) to warm up after each restart
- watch the memory usage if you have a huge log
- requested time ranges will be extended to align with a quarter of an hour


## Installation

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

Logbook Cache is available as an Integration from [HACS](https://github.com/custom-components/hacs).

**Please install with HACS, manual installs are self-supported**


## Configuration

Enable via the Integrations page, search for "Logbook Cache".

Once enabled, you can change options such as the number of days to cache.


## Support

Please use the GitHub repository (https://github.com/amelchio/logbook_cache/issues) for support. If you suspect a bug, please include debug logs.

Debug logs are enabled like this in configuration.yaml:
```yaml
logger:
  default: warning
  logs:
    custom_components.logbook_cache: debug
```


## Donations

<a href="https://www.buymeacoffee.com/amelchio" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Beer" style="height: auto !important;width: auto !important;" ></a><br>
