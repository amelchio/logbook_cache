# Logbook Cache for Home Assistant

Custom component to speed up Home Assistant logbook viewing.

It works by keeping filtered results preloaded and updated in memory.

This only affects the logbook, not any history view.

## Installation

**Please install with HACS, manual installs are self-supported**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

## Configuration

The custom component must be enabled in `configuration.yaml`:

```yaml
logbook_cache:
```

By default, two days (always the current day and the day before) of logbook entries are kept. Cache filling starts two minutes after startup and will by default load two days.

```yaml
logbook_cache:
  preload_days: 2
  preload_delay:
    minutes: 2
  keep_days: 2
```

## Donations

<a href="https://www.buymeacoffee.com/amelchio" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Beer" style="height: auto !important;width: auto !important;" ></a><br>
