import asyncio
import datetime
import logging

import voluptuous as vol

import homeassistant.components.logbook as lb
import homeassistant.helpers.config_validation as cv
import homeassistant.util.dt as dt_util

_LOGGER = logging.getLogger(__name__)

DOMAIN = "logbook_cache"

CONF_PRELOAD_DAYS = "preload_days"
CONF_PRELOAD_DELAY = "preload_delay"
CONF_KEEP_DAYS = "keep_days"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(
                    CONF_PRELOAD_DELAY, default={"minutes": 2}
                ): cv.positive_time_period_dict,
                vol.Optional(CONF_PRELOAD_DAYS, default=2): vol.All(
                    vol.Coerce(int), vol.Range(min=0)
                ),
                vol.Optional(CONF_KEEP_DAYS, default=2): vol.All(
                    vol.Coerce(int), vol.Range(min=1)
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

cache = {}
original_get_events = None


async def async_setup(hass, global_config):
    config = global_config.get(DOMAIN, {})
    _LOGGER.debug(f"config={config}")

    global original_get_events
    original_get_events = lb._get_events
    lb._get_events = wrap_get_events

    preload_days = config[CONF_PRELOAD_DAYS]
    if preload_days:
        preload_delay = config[CONF_PRELOAD_DELAY].total_seconds()
        start = dt_util.as_utc(
            dt_util.start_of_local_day() - datetime.timedelta(days=preload_days - 1)
        )
        hass.helpers.event.async_call_later(
            preload_delay, refresh_cache(hass, global_config, start)
        )

    return True


def wrap_get_events(hass, logbook_config, start_day, end_day, entity_id=None):
    if entity_id is not None:
        return original_get_events(hass, logbook_config, start_day, end_day, entity_id)

    events = []

    timestamp = start_day
    while timestamp < end_day:
        if timestamp in cache:
            chunk = cache[timestamp]
        elif dt_util.utcnow() < timestamp:
            chunk = []
        else:
            chunk = load_chunk(hass, logbook_config, timestamp)

        events.extend(chunk)
        timestamp = step_timestamp(timestamp)

    return events


async def refresh_cache(hass, global_config, timestamp):
    config = global_config.get(DOMAIN, {})
    logbook_config = global_config.get(lb.DOMAIN, {})

    def refresh(timestamp):
        _LOGGER.debug(f"Caching from {timestamp}")
        while step_timestamp(timestamp) < dt_util.utcnow():
            load_chunk(hass, logbook_config, timestamp)
            timestamp = step_timestamp(timestamp)

        keep_days = config[CONF_KEEP_DAYS]
        purge_limit = dt_util.as_utc(
            dt_util.start_of_local_day() - datetime.timedelta(days=keep_days - 1)
        )
        _LOGGER.debug(f"Purging until {purge_limit}")
        for key in list(cache.keys()):
            if key < purge_limit:
                _LOGGER.debug(f"Removing {key}")
                del cache[key]

        _LOGGER.debug(f"Scheduling fill of {timestamp}")
        hass.helpers.event.async_track_point_in_utc_time(
            refresh_cache(hass, global_config, timestamp), step_timestamp(timestamp)
        )

    hass.async_add_job(refresh, timestamp)


def load_chunk(hass, logbook_config, timestamp):
    next_timestamp = step_timestamp(timestamp)

    chunk = original_get_events(hass, logbook_config, timestamp, next_timestamp)

    if dt_util.utcnow() > next_timestamp:
        _LOGGER.debug(f"Storing {timestamp}")
        cache[timestamp] = chunk

    return chunk


def step_timestamp(timestamp):
    return timestamp + datetime.timedelta(minutes=lb.GROUP_BY_MINUTES)
