# Logbook Cache for Home Assistant

Custom component to speed up Home Assistant logbook viewing.

This works by keeping filtered results preloaded and updated in memory. The
effect is most significant with slow hardware such as Raspberry Pi.

Caveats:
- the cache takes some time (maybe several minutes) to warm up after each restart
- watch the memory usage if you have a huge log


## Installation

**Please install with HACS, manual installs are self-supported**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

For now, you first need to add this URL (`https://github.com/amelchio/logbook_cache`) as a custom repository in HACS settings.


## Configuration

Enable via the Integrations page, search for "Logbook Cache".

Once enabled, you can select "Logbook Cache" and use the cogwheel to set the number of days to cache.


## Donations

<a href="https://www.buymeacoffee.com/amelchio" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Beer" style="height: auto !important;width: auto !important;" ></a><br>
