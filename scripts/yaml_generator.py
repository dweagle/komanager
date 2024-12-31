import os
import re
import logging
import platform
from scripts.settings import load_settings
from ruamel.yaml import YAML
from datetime import datetime, timedelta

yaml = YAML()

logger = logging.getLogger(__name__)

DEFAULTS = {
    'is_anime': False,
    'use_watch_region': True,
    'days_ahead': 30,
    'date_delimiter': '/',
    'remove_leading_zero': False,
    'font': "{config_directory}/fonts/Inter-Medium.ttf",
    'font_size': 45,
    'font_color': '"#FFFFFF"',
    'horizontal_align': 'center',
    'vertical_align': 'top',
    'horizontal_offset': 0,
    'vertical_offset': 38,
    'back_width': 475,
    'back_height': 55,
    'back_radius': 30,
    'ignore_blank_results': "true",
    'timezone': 'America/New_York',
    'with_status': 0,
    'watch_region': 'US',
    'with_original_languge': 'en',
    'limit': 500,
    'with_watch_monetization_types': 'flatrate|free|ads|rent|buy',

    'use': True,

    'upcoming_back_color': '#FC4E03',
    'upcoming_text': 'U P C O M I N G',

    'new_back_color': '#008001',
    'new_text': 'N E W  S E R I E S',

    'new_airing_back_color': '#008001',
    'new_airing_text': 'N E W - A I R S',

    'airing_back_color': '#003880',
    'airing_text': 'A I R I N G',
    'today_text': 'A I R S  T O D A Y',
    'next_text': 'A I R I N G ',

    'ended_back_color': '#000000',
    'ended_text': 'E N D E D',

    'canceled_back_color': '#CF142B',
    'canceled_text': 'C A N C E L E D',

    'returning_back_color': '#103197',
    'returning_text': 'R E T U R N I N G',
    'returns_text': 'R E T U R N S ',

    'collection_use': True,
    'collection_days_ahead': 30,
    'days_last_aired': 45,
    'poster_source': 'file',
    'poster_path':  "{config_directory}/posters/Kometa Returning Soon.jpg",
    'visible_home': True,
    'visible_shared': True,
    "summary": 'Shows returning soon!',
    "minimum_items": '1',
    "delete_below_minimum": 'true',
    "sort_title": '!010_Returning',

    'new_movie_use': True,
    'days_new': 90,
    'new_movie_back_color': '#103197',
    'new_movie_text': 'N E W '
}

timezone = os.getenv('TZ', DEFAULTS['timezone'])

def get_with_defaults(settings, primary_key, fallback_key=None, config_directory=''):
    def is_valid_color(value):
        pattern = r"^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$"
        return isinstance(value, str) and re.match(pattern, value)

    value = settings.get(primary_key)
    
    if value is None and fallback_key is not None:
        value = DEFAULTS.get(fallback_key)

    if primary_key == 'font_color' and not is_valid_color(value):
        value = DEFAULTS.get('font_color', '#FFFFFF')

    if value in ["path/to/kometa-poster", "path/to/kometa-font"]:
        value = DEFAULTS.get(primary_key)

    if isinstance(value, str) and "{config_directory}" in value:
        value = value.replace("{config_directory}", config_directory)

    return value 

############################
# Create Overlay Template  #
############################
indentlog = "   " # indent for 3 spaces in log
indentlog2 = "      " # indent for 6 spaces in log
indentlog3 = "         " # indent for 9 spaces in log
indentlog4 = "            " # indent for 12 spacees in log
indent2 = "    "  # indent 2 tabs (4 spaces) for kometa yaml spacing
indent3 = "      " # indent 3 tabs (6 spaces) for kometa yaml spacing

def create_library_yaml(config_directory):
    try:
        settings = load_settings(config_directory, log_message=False)

        current_date = datetime.now()

        date_21_days_prior = (current_date - timedelta(days=21)).strftime('%m/%d/%Y')

        date_15_days_prior = (current_date - timedelta(days=15)).strftime('%m/%d/%Y')

        air_date_today= (current_date).strftime('%m/%d/%Y')

        date_14_days_prior = (current_date - timedelta(days=14)).strftime('%m/%d/%Y')

        libraries = settings.get('libraries', {})

        overlay_settings = settings.get('overlay_settings', {})

        use_overlays = settings.get('use_overlays', {})

        date_delimiter = get_with_defaults(overlay_settings, 'date_delimiter', '/')
        
        remove_leading_zero = get_with_defaults(overlay_settings, 'remove_leading_zero', False)

        if remove_leading_zero:
            if platform.system() == "Windows":
                month_format_code = "%#m"
                day_format_code = "%#d"
            elif platform.system() in ["Linux", "Darwin"]:
                month_format_code = "%-m"
                day_format_code = "%-d"
        else:
            month_format_code = "%m"
            day_format_code = "%d"

        for library_name, library_settings in libraries.items():
            is_anime = get_with_defaults(library_settings, 'is_anime', 'is_anime')
            use_watch_region = get_with_defaults(library_settings, 'use_watch_region', 'use_watch_region')
            logger.info(f"{indentlog}Creating main template yaml for {library_name}.")

            template_string = f"""# {library_name} Template
templates:
  {library_name} Status TMDB Discover:
    sync_mode: sync
    builder_level: show
    overlay:
      group: status
      weight: <<weight>>
      name: text(<<text>>)
      font: "{get_with_defaults(overlay_settings, 'font', 'font', config_directory)}"
      font_size: {get_with_defaults(overlay_settings, 'font_size', 'font_size')}
      font_color: <<font_color>>
      horizontal_align: {get_with_defaults(overlay_settings, 'horizontal_align', 'horizontal_align')}
      vertical_align: {get_with_defaults(overlay_settings, 'vertical_align', 'veritcal_align')}
      horizontal_offset: {get_with_defaults(overlay_settings, 'horizontal_offset', 'horizontal_offset')}
      vertical_offset: {get_with_defaults(overlay_settings, 'vertical_offset', 'vertical_offset')}
      back_color: <<back_color>>
      back_width: {get_with_defaults(overlay_settings, 'back_width', 'back_width')}
      back_height: {get_with_defaults(overlay_settings, 'back_height', 'back_height')}
      back_radius: {get_with_defaults(overlay_settings, 'back_radius', 'back_radius')}
    ignore_blank_results: {get_with_defaults(overlay_settings, 'ignore_blank_results', 'ignore_blank_results').lower()}
    tmdb_discover:
      air_date.gte: <<date>>
      air_date.lte: <<date>>
      timezone: {timezone}
      with_status: <<status>>
"""
            if use_watch_region:
                logger.info(f"{indentlog2}'watch_region' set to 'true'")
                logger.info(f"{indentlog3}Adding 'watch_region: {get_with_defaults(overlay_settings, 'watch_region', 'watch_region')}'.")
                logger.info(f"{indentlog3}Adding 'with_watch_monetization_type: {get_with_defaults(overlay_settings, 'with_watch_monetization_types', 'with_watch_monetization_types')}'.")
                template_string += f"{indent3}watch_region: {get_with_defaults(overlay_settings, 'watch_region')}\n"
                template_string += f"{indent3}with_watch_monetization_types: {get_with_defaults(overlay_settings, 'with_watch_monetization_types', 'with_watch_monetization_types')}\n"

            else:
                logger.info(f"{indentlog2}'watch_region' set to 'false'")
                logger.info(f"{indentlog3}Removing 'watch_region'.")
                logger.info(f"{indentlog3}Removing 'with_watch_monetizaion_types'.")
            
            if not is_anime:
                logger.info(f"{indentlog2}'is_anime' set to 'false'")
                logger.info(f"{indentlog3}Adding 'with_original_language: {get_with_defaults(overlay_settings, 'with_original_language', 'with_original_language')}'.")
                template_string += f"{indent3}with_original_language: {get_with_defaults(overlay_settings, 'with_original_language', 'with_original_language')}\n"

            else:
                logger.info(f"{indentlog2}'is_anime' set to 'true'")
                logger.info(f"{indentlog3}Removing 'with_original_language'.")

            template_string += f"{indent3}limit: {get_with_defaults(overlay_settings, 'limit', 'limit')}\n"

            plex_all = f"""
  {library_name} Status Plex All:
    sync_mode: sync
    builder_level: show
    overlay:
      group: status
      weight: <<weight>>
      name: text(<<text>>)
      font: "{get_with_defaults(overlay_settings, 'font', 'font', config_directory)}"
      font_size: {get_with_defaults(overlay_settings, 'font_size', 'font_size')}
      font_color: <<font_color>>
      horizontal_align: {get_with_defaults(overlay_settings, 'horizontal_align', 'horizontal_align')}
      vertical_align: {get_with_defaults(overlay_settings, 'vertical_align', 'veritcal_align')}
      horizontal_offset: {get_with_defaults(overlay_settings, 'horizontal_offset', 'horizontal_offset')}
      vertical_offset: {get_with_defaults(overlay_settings, 'vertical_offset', 'vertical_offset')}
      back_color: <<back_color>>
      back_width: {get_with_defaults(overlay_settings, 'back_width', 'back_width')}
      back_height: {get_with_defaults(overlay_settings, 'back_height', 'back_height')}
      back_radius: {get_with_defaults(overlay_settings, 'back_radius', 'back_radius')}
    ignore_blank_results: {get_with_defaults(overlay_settings, 'ignore_blank_results', 'ignore_blank_results').lower()}
"""
            template_string += plex_all

            template_string += "\noverlays:"

            logger.info(f"{indentlog}Main template created")
            logger.info("")
            logger.info(f"{indentlog}Creating optional overlays")

##########################
#### UPCOMING SERIES #####
##########################

            upcoming_series_settings = use_overlays.get("upcoming_series", {})
            if get_with_defaults(upcoming_series_settings, "use", "use"):
                logger.info(f"{indentlog2}'Upcoming' set to true. Creating 'Upcoming' overlay.")

                upcoming_section = f"""
# UPCOMING SERIES OVERLAY
  {library_name} Upcoming Series:
    variables: {{text: {get_with_defaults(upcoming_series_settings, 'text', 'upcoming_text')}, weight: 100, font_color: "{get_with_defaults(upcoming_series_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(upcoming_series_settings, 'back_color', 'upcoming_back_color')}"}}
    template: {{name: {library_name} Status Plex All}}
    plex_all: true
    filters:
      tmdb_status:
        - returning
        - planned
        - production
      release.after: today
"""
                template_string += upcoming_section
            else:
                logger.info(f"{indentlog2}'Upcoming' set to false. 'Upcoming' overlay not created.")

##########################
####    NEW SERIES   #####
##########################

            new_series_settings = use_overlays.get("new_series", {})
            if get_with_defaults(new_series_settings, "use", "use"):
                logger.info(f"{indentlog2}'New Series' set to true. Creating 'New Series' overlay.")

                new_series_section = f"""
# NEW SERIES BANNER/TEXT
  {library_name} New Series:
    variables: {{text: {get_with_defaults(new_series_settings, 'text', 'new_text')}, weight: 76, font_color: "{get_with_defaults(new_series_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(new_series_settings, 'back_color', 'new_back_color')}"}}
    template: {{name: {library_name} Status Plex All}}
    plex_all: true
    filters:
      tmdb_status:
        - returning
        - planned
        - production
        - ended
        - canceled
      first_episode_aired.after: {date_21_days_prior}
"""
                template_string += new_series_section
            else:
                logger.info(f"{indentlog2}'New Series' set to false. Creating 'New Series' overaly.")


##########################
###  NEW AIRING NEXT   ###
##########################

            new_airing_next_settings = use_overlays.get('new_airing_next', {})

            new_airing_next_dates = [(current_date + timedelta(days=i)).strftime('%m/%d/%Y') for i in range(1, 15)]

            if get_with_defaults(new_airing_next_settings, "use", "use"):
                logger.info(f"{indentlog2}'New Airing Next' set to true. Creating 'New Airing Next' overlay.")
                
                for i, next_day_date_str in enumerate(new_airing_next_dates, start=1):
                    next_day_date = datetime.strptime(next_day_date_str, '%m/%d/%Y')
                    mmddyyyy = next_day_date.strftime('%m/%d/%Y')

                    mmdd_custom = next_day_date.strftime(f'{month_format_code}{date_delimiter}{day_format_code}')
                    mmddyyyy_custom = next_day_date.strftime(f'{month_format_code}{date_delimiter}{day_format_code}{date_delimiter}%Y')

                    weight = 90 - i + 1 
                    
                    new_airing_next_section = f"""
# NEW AIRING NEXT BANNER/TEXT DAY {i}
  {library_name} New Airing Next {mmddyyyy_custom}: 
    variables: {{text: {get_with_defaults(new_airing_next_settings, 'text', 'new_airing_text')} {mmdd_custom}, weight: {weight}, font_color: "{get_with_defaults(new_airing_next_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(new_airing_next_settings, 'back_color', 'new_airing_back_color')}", date: {mmddyyyy}, status: 0}}
    template: {{name: {library_name} Status TMDB Discover}}
    filters:
      first_episode_aired.after: {date_21_days_prior}
"""
                    template_string += new_airing_next_section
            else:
                logger.info(f"{indentlog2}'New Airing Next' set to false. 'New Airing Next' Overlay not created")
                
##########################
####  AIRING SERIES  #####
##########################

            airing_series_settings = use_overlays.get("airing_series", {})
            if get_with_defaults(airing_series_settings, "use", "use"):
                logger.info(f"{indentlog2}'Airing Series' set to true. Creating 'Airing' overlay")

                airing_series_section = f"""
# AIRING SERIES BANNER/TEXT
  {library_name} Airing Series:
    variables: {{text: {get_with_defaults(airing_series_settings, 'text', 'airing_text')}, weight: 43, font_color: "{get_with_defaults(airing_series_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(airing_series_settings, 'back_color', 'airing_back_color')}"}}
    template: {{name: {library_name} Status Plex All}}
    plex_all: true
    filters:
      tmdb_status:
        - returning
        - planned
        - production
      last_episode_aired.after: {date_15_days_prior}
    """
                template_string += airing_series_section

            else:
                logger.info(f"{indentlog2}'Airing Series' set to false. 'Airing' Overlay not created.")

##########################
####  AIRING TODAY   #####
##########################

            airing_today_settings = use_overlays.get("airing_today", {})
            if get_with_defaults(airing_today_settings, "use", "use"):
                logger.info(f"{indentlog2}'Airing Today' set to true. Creating 'Airing Today' overlay.")

                airing_today_section = f"""
# AIRING TODAY BANNER/TEXT
  {library_name} Airing Today:
    variables: {{text: {get_with_defaults(airing_today_settings, 'text', 'today_text')}, weight: 75, font_color: "{get_with_defaults(airing_today_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(airing_today_settings, 'back_color', 'airing_back_color')}", date: {air_date_today}, status: 0}}
    template: {{name: {library_name} Status TMDB Discover}}
"""
                template_string += airing_today_section

            else:
                logger.info(f"{indentlog2}Airing Today set to false. 'Airing Today' overlay not created")

##########################
####   AIRING NEXT   #####
##########################

            airing_next_settings = use_overlays.get('airing_next', {})

            days_ahead = min(get_with_defaults(overlay_settings, 'days_ahead', 'days_ahead'), 30)
            airing_next_dates = [(current_date + timedelta(days=i)).strftime('%m/%d/%Y') for i in range(1, days_ahead + 1)]

            if get_with_defaults(airing_next_settings, "use", "use"):
                logger.info(f"{indentlog2}'Airing Next' set to true. 'days_ahead:' set to {days_ahead}. Creating {days_ahead} 'Airing Next' overlay/s")
                
                for i, next_day_date_str in enumerate(airing_next_dates, start=1):
                    next_day_date = datetime.strptime(next_day_date_str, '%m/%d/%Y')
                    mmddyyyy = next_day_date.strftime('%m/%d/%Y')

                    mmdd_custom = next_day_date.strftime(f'{month_format_code}{date_delimiter}{day_format_code}')
                    mmddyyyy_custom = next_day_date.strftime(f'{month_format_code}{date_delimiter}{day_format_code}{date_delimiter}%Y')

                    weight = 74 - i + 1
                    
                    airing_next_section = f"""
# AIRING NEXT BANNER/TEXT DAY {i}
  {library_name} Airing Next {mmddyyyy_custom}:
    variables: {{text: {get_with_defaults(airing_next_settings, 'text', 'next_text')} {mmdd_custom}, weight: {weight}, font_color: "{get_with_defaults(airing_next_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(airing_next_settings, 'back_color', 'airing_back_color')}", date: {mmddyyyy}, status: 0}}
    template: {{name: {library_name} Status TMDB Discover}}
    filters:
      last_episode_aired.after: {date_15_days_prior}
"""
                    template_string += airing_next_section

            else:
                logger.info(f"{indentlog2}'Airing Next' set to false. 'Airing Next' overlay not created.")

##########################
####   ENDED SERIES   ####
##########################

            ended_series_settings = use_overlays.get("ended_series", {})

            if get_with_defaults(ended_series_settings, "use", "use"):
                logger.info(f"{indentlog2}'Ended Series' set to true. Creating 'Ended Series' overlay.")

                ended_series_section = f"""
# ENDED SERIES BANNER/TEXT
  {library_name} Ended Series:
    variables: {{text: {get_with_defaults(ended_series_settings, 'text', 'ended_text')}, weight: 9, font_color: "{get_with_defaults(ended_series_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(ended_series_settings, 'back_color', 'ended_back_color')}"}}
    template: {{name: {library_name} Status Plex All}}
    plex_all: true
    filters:
      tmdb_status:
        - ended
    """
                template_string += ended_series_section
            else:
                logger.info(f"{indentlog2}'Ended Sereies' set to false. 'Ended Series' overlay not created")
            
##########################
#### CANCELED SERIES  ####
##########################

            canceled_series_settings = use_overlays.get("canceled_series", {})

            if get_with_defaults(canceled_series_settings, "use", "use"):
                logger.info(f"{indentlog2}'Canceled Series' set to true. Creating 'Canceled Series' overlay.")
                
                canceled_series_section = f"""
# CANCELED SERIES BANNER/TEXT
  {library_name} Canceled Series:
    variables: {{text: {get_with_defaults(canceled_series_settings, 'text', 'canceled_text')}, weight: 10, font_color: "{get_with_defaults(canceled_series_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(canceled_series_settings, 'back_color', 'canceled_back_color')}"}}
    template: {{name: {library_name} Status Plex All}}
    plex_all: true
    filters:
      tmdb_status:
        - canceled
    """
                template_string += canceled_series_section
            else:
                logger.info(f"{indentlog2}'Canceled Series' set to false. 'Canceled Series' overlay not created.")
            
##########################
#### RETURNING SERIES ####
##########################

            returning_series_settings = use_overlays.get("returning_series", {})

            if get_with_defaults(returning_series_settings, "use", "use"):
                logger.info(f"{indentlog2}'Returning Series' set to true. Creating 'Returning' overlay.")
                
                returning_series_section = f"""
# RETURNING SERIES BANNER/TEXT
  {library_name} Returning Series:
    variables: {{text: {get_with_defaults(returning_series_settings, 'text', 'returning_text')}, weight: 13, font_color: "{get_with_defaults(returning_series_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(returning_series_settings, 'back_color', 'returning_back_color')}"}}
    template: {{name: {library_name} Status Plex All}}
    plex_all: true
    filters:
      tmdb_status:
        - returning
        - planned
        - production
    """
                template_string += returning_series_section
            else:
                logger.info(f"{indentlog2}'Returning' set to false. 'Returning' overlay not created")

##########################
####   RETURNS NEXT  #####
##########################

            returns_next_settings = use_overlays.get('returns_next', {})

            days_ahead = min(get_with_defaults(overlay_settings, 'days_ahead', 'days_ahead'), 30)
            returns_next_dates = [(current_date + timedelta(days=i)).strftime('%m/%d/%Y') for i in range(1, days_ahead + 1)]

            if get_with_defaults(returns_next_settings, "use", "use"):
                logger.info(f"{indentlog2}'Returns Next' set to true. 'days_ahead:' set to {days_ahead}. Creating {days_ahead} 'Returns Next' overlay/s")
                
                for i, next_day_date_str in enumerate(returns_next_dates, start=1):
                    next_day_date = datetime.strptime(next_day_date_str, '%m/%d/%Y')
                    mmddyyyy = next_day_date.strftime('%m/%d/%Y')

                    mmdd_custom = next_day_date.strftime(f'{month_format_code}{date_delimiter}{day_format_code}')
                    mmddyyyy_custom = next_day_date.strftime(f'{month_format_code}{date_delimiter}{day_format_code}{date_delimiter}%Y')

                    weight = 43 - i + 1
                    
                    returns_next_section = f"""
# RETURNS NEXT BANNER/TEXT DAY {i}
  {library_name} Returns Next {mmddyyyy_custom}:
    variables: {{text: {get_with_defaults(returns_next_settings, 'text', 'returns_text')} {mmdd_custom}, weight: {weight}, font_color: "{get_with_defaults(returns_next_settings, 'font_color', 'font_color')}", back_color: "{get_with_defaults(returns_next_settings, 'back_color', 'returning_back_color')}", date: {mmddyyyy}, status: 0}}
    template: {{name: {library_name} Status TMDB Discover}}
    filters:
      last_episode_aired.before: {date_14_days_prior}
"""
                    template_string += returns_next_section
            else:
                logger.info(f"{indentlog2}'Returns Next' set to false. 'Returns Next' overlay/s not created")

############################
# WRITE TEMPLATE YAML FILE #
############################

            overlay_save_folder = overlay_settings.get('overlay_save_folder')

            if overlay_save_folder and isinstance(overlay_save_folder, str):
                overlay_save_folder = overlay_save_folder.strip()
                if overlay_save_folder == "path/to/folder":
                    overlay_save_folder = ''
            else:
                overlay_save_folder = ''

            if overlay_save_folder:
                logger.info(f"{indentlog2}Using custom overlay save folder: {overlay_save_folder}")
            else:
                logger.debug(f"{indentlog2}No custom overlay save folder provided.  Using '{config_directory}' folder.")
                overlay_save_folder = config_directory

            if not os.path.exists(overlay_save_folder):
                logger.error(f"{indentlog3}Overlay folder doesn't exist or permissions not set.  Exiting main script")
                logger.error(f"{indentlog3}If using path outside of mounted container config volume, you need to mount a volume to this.")
                return

            normalized_library_name = library_name.lower().replace(' ', '-')

            output_file_path = os.path.join(overlay_save_folder, f"overlay-status-{normalized_library_name}.yml")
            
            try:
                with open(output_file_path, 'w') as file:
                    file.write(template_string)
                logger.info(f"{indentlog}Generated overlay for {library_name} at '{output_file_path}'")
                logger.info("")
            except Exception as e:
                logger.error(f"{indentlog}Error generating overlay for {library_name}: {e}")
                logger.info("")

    except Exception as e:
        logger.error(f"An error occurred while generating overlay files: {e}")

#############################
# RETURNING SOON COLLECTION #
#############################

def create_collection_yaml(config_directory):
    try:
        settings = load_settings(config_directory, log_message=False)
        
        libraries = settings.get('libraries', {})

        overlay_settings = settings.get('overlay_settings', {})

        collection_settings = settings.get('returning_soon_collection', {})

        current_date = datetime.now()

        days_last_aired = get_with_defaults(collection_settings, 'days_last_aired', 'days_last_aired')

        date_last_aired = (current_date - timedelta(days=days_last_aired)).strftime('%m/%d/%Y')

        air_date = (current_date).strftime('%m/%d/%Y')

        collection_days_ahead = get_with_defaults(collection_settings, 'collection_days_ahead', 'collection_days_ahead')

        collection_days_past = (current_date + timedelta(days=collection_days_ahead)).strftime('%m/%d/%Y')

        for library_name, library_settings in libraries.items():
            is_anime = get_with_defaults(library_settings, 'is_anime', 'is_anime')
            use_watch_region = get_with_defaults(library_settings, 'use_watch_region', 'use_watch_region')
            
            if get_with_defaults(collection_settings, "use", "collection_use"):
                logger.info(f"{indentlog}Returning Soon Collection 'use:' set to true. Creating Returning Soon Collection yaml for {library_name}.")

                use_poster = get_with_defaults(collection_settings, 'use_poster', 'use_poster')
            
                if not use_poster:
                    logger.info(f"{indentlog2}'use_poster' set to {use_poster}. Excluding poster setting from collection YAML")

                template_string = f"""# {library_name} Returning Soon Collection
collections:
  {library_name} Returning Soon:
"""
                if use_poster:
                    poster_source = get_with_defaults(collection_settings, 'poster_source', 'poster_source')
                    poster_path = get_with_defaults(collection_settings, 'poster_path', 'poster_path', config_directory)
                    template_string += f"{indent2}{poster_source}_poster: \"{poster_path}\"\n"

                template_string += f"""{indent2}collection_order: custom
    visible_home: {get_with_defaults(collection_settings, 'visible_home', 'visible_home').lower()}
    visible_shared: {get_with_defaults(collection_settings, 'visible_shared', 'visible_shared').lower()}
    sync_mode: sync
    summary: "{get_with_defaults(collection_settings, 'summary', 'summary')}"
    minimum_items: {get_with_defaults(collection_settings, 'minimum_items', 'minimum_items')}
    delete_below_minimum: {get_with_defaults(collection_settings, 'delete_below_minimum', 'delete_below_minimum').lower()}
    sort_title: "{get_with_defaults(collection_settings, 'sort_title', 'sort_title')}"
    tmdb_discover:
      air_date.gte: {air_date}
      air_date.lte: {collection_days_past}
      timezone: {timezone}
      with_status: 0
"""
                if use_watch_region:
                    logger.info(f"{indentlog2}'watch_region' set to 'true'")
                    logger.info(f"{indentlog3}Adding 'watch_region: {get_with_defaults(overlay_settings, 'watch_region', 'watch_region')}'.")
                    logger.info(f"{indentlog3}Adding 'with_watch_monetization_type: {get_with_defaults(overlay_settings, 'with_watch_monetization_types', 'with_watch_monetization_types')}'.")
                    template_string += f"{indent3}watch_region: {get_with_defaults(overlay_settings, 'watch_region', 'watch_region')}\n"
                    template_string += f"{indent3}with_watch_monetization_types: {get_with_defaults(overlay_settings, 'with_watch_monetization_types', 'with_watch_monetization_types')}\n"

                else:
                    logger.info(f"{indentlog2}'watch_region' set to 'false'")
                    logger.info(f"{indentlog3}Removing 'watch_region'.")
                    logger.info(f"{indentlog3}Removing 'with_watch_monetizaion_types'.")

                if not is_anime:
                    logger.info(f"{indentlog2}'is_anime' set to 'false'")
                    logger.info(f"{indentlog3}Adding 'with_original_language: {get_with_defaults(overlay_settings, 'with_original_language', 'with_original_language')}'.")
                    template_string += f"{indent3}with_original_language: {get_with_defaults(overlay_settings, 'with_original_language', 'with_original_language')}\n"

                else:
                    logger.info(f"{indentlog2}'is_anime' set to 'true'")
                    logger.info(f"{indentlog3}Removing 'with_original_language'.")

                template_string += f"{indent3}limit: {get_with_defaults(overlay_settings, 'limit', 'limit')}\n"
                
                template_string += f"{indent2}filters:\n"
                template_string += f"{indent3}last_episode_aired.before: {date_last_aired}\n"

############################
#  WRITE COLLECTION YAML   #
############################

                collection_save_folder = collection_settings.get('collection_save_folder')

                if collection_save_folder and isinstance(collection_save_folder, str):
                    collection_save_folder = collection_save_folder.strip()
                    if collection_save_folder == "path/to/folder":
                        collection_save_folder = ''
                else:
                    collection_save_folder = ''

                if collection_save_folder:
                    logger.info(f"{indentlog2}Using custom collection save folder: {collection_save_folder}")
                else:
                    logger.debug(f"{indentlog2}No custom collection save folder provided.  Using '{config_directory}' folder.")
                    collection_save_folder = config_directory

                if not os.path.exists(collection_save_folder):
                    logger.error(f"{indentlog}Collection folder doesn't exist or permissions not set.  Exiting main script")
                    logger.error(f"{indentlog}If using path outside of mounted container config volume, you need to mount a volume to this.")
                    return

                normalized_library_name = library_name.lower().replace(' ', '-')

                output_file_path = os.path.join(collection_save_folder, f"collection-returning-soon-{normalized_library_name}.yml")
                
                try:
                    with open(output_file_path, 'w') as file:
                        file.write(template_string)
                    logger.info(f"{indentlog}Generated Returning Soon Collection for {library_name} at '{output_file_path}'")
                    logger.info("")
                except Exception as e:
                    logger.error(f"{indentlog}Error generating collection for {library_name}: {e}")
                    logger.info("")


            else:
                logger.info(f"{indentlog2}'Returning Soon' collection 'use:' set to false. 'Returning Soon' collection not created")
                logger.info("")

    except Exception as e:
        logger.error(f"An error occurred while generating collection files: {e}")
        
#############################
# NEW MOVIE RELEASE OVERLAY #
#############################

def create_new_movie_yaml(config_directory):
    try:
        settings = load_settings(config_directory, log_message=False)
        
        overlay_settings = settings.get('overlay_settings', {})

        new_release_settings = settings.get('movie_new_release', {})

        if get_with_defaults(new_release_settings, "use", "new_movie_use"):
            logger.info(f"{indentlog}'movie_new_release' 'use:' set to true. Creating 'movie_new_release' overlay.")

            new_movie_string = f"""# New Release Overlay
overlays:
  Movie New Release:
    sync_mode: sync
    builder_level: movie
    overlay:
      name: text({get_with_defaults(new_release_settings, 'text', 'new_movie_text')})
      font: "{get_with_defaults(overlay_settings, 'font', 'font', config_directory)}"
      font_size: {get_with_defaults(overlay_settings, 'font_size', 'font_size')}
      font_color: "{get_with_defaults(new_release_settings, 'font_color', 'font_color')}"
      horizontal_align: {get_with_defaults(overlay_settings, 'horizontal_align', 'horizontal_align')}
      vertical_align: {get_with_defaults(overlay_settings, 'vertical_align', 'veritcal_align')}
      horizontal_offset: {get_with_defaults(overlay_settings, 'horizontal_offset', 'horizontal_offset')}
      vertical_offset: {get_with_defaults(overlay_settings, 'vertical_offset', 'vertical_offset')}
      back_color: "{get_with_defaults(new_release_settings, 'back_color', 'new_movie_back_color')}"
      back_width: {get_with_defaults(overlay_settings, 'back_width', 'back_width')}
      back_height: {get_with_defaults(overlay_settings, 'back_height', 'back_height')}
      back_radius: {get_with_defaults(overlay_settings, 'back_radius', 'back_radius')}
    ignore_blank_results: {get_with_defaults(overlay_settings, 'ignore_blank_results', 'ignore_blank_results').lower()}
    plex_search:
      all:
        release: {get_with_defaults(new_release_settings, 'days_to_consider_new', 'days_new')}
"""

################################
# WRITE MOVIE NEW RELEASE YAML #
################################

            new_movie_save_folder = new_release_settings.get('new_movie_save_folder')

            if new_movie_save_folder and isinstance(new_movie_save_folder, str):
                new_movie_save_folder = new_movie_save_folder.strip()
                if new_movie_save_folder == "path/to/folder":
                    new_movie_save_folder = ''
            else:
                new_movie_save_folder = ''

            if new_movie_save_folder:
                logger.info(f"{indentlog2}Using 'movie_new_release' save folder: {new_movie_save_folder}")
            else:
                logger.debug(f"{indentlog2}No 'movie_new_release' save folder provided.  Using '{config_directory}' folder.")
                new_movie_save_folder = config_directory

            if not os.path.exists(new_movie_save_folder):
                logger.error(f"{indentlog}'movie_new_release' folder doesn't exist or permissions not set.  Exiting main script")
                logger.error(f"{indentlog}If using path outside of mounted container config volume, you need to mount a volume to this.")
                return

            output_file_path = os.path.join(new_movie_save_folder, f"overlay-movie-new-release.yml")
            
            try:
                with open(output_file_path, 'w') as file:
                    file.write(new_movie_string)
                logger.info(f"{indentlog}Generated 'movie_new_release' overlay for at '{output_file_path}'")
                logger.info("")
            except Exception as e:
                logger.error(f"{indentlog}Error generating 'movie_new_release' overlay: {e}")
                logger.info("")
        else:
            logger.info(f"{indentlog2}'movie_new_release' set to false. 'new_movie_relase_date' overlay not created")
            logger.info("")
            
    except Exception as e:
        logger.error(f"An error occurred while 'movie_new_release' overlay file: {e}")
