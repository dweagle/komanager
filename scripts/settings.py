import os
import logging
from collections import OrderedDict
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from ruamel.yaml.representer import RoundTripRepresenter

yaml = YAML()
yaml.default_flow_style = False
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.allow_unicode = True
yaml.preserve_quotes = True

yaml.Representer = RoundTripRepresenter
yaml.Representer.add_representer(OrderedDict, RoundTripRepresenter.represent_dict)

logger = logging.getLogger(__name__)

settings_filename = "overlay-settings.yml"
comment = "# yaml-language-server: $schema=https://raw.githubusercontent.com/dweagle/komanager/main/json_schema/overlay-settings.json\n"

def add_blank_lines(yaml_output):
    lines = yaml_output.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        new_lines.append(line)
        if i + 1 < len(lines) and lines[i + 1] and lines[i + 1][0].isalnum() and line and lines[i + 1][0] != '-':
            new_lines.append('')
    return '\n'.join(new_lines)

settings = OrderedDict({
    "libraries": OrderedDict({
        "TV Shows": {
            "is_anime": False,
            "use_watch_region": True
        },
        "4k TV Shows": {
            "is_anime": False,
            "use_watch_region": True
        },
        "Anime": {
            "is_anime": True,
            "use_watch_region": True
        }
    }),

    "overlay_settings": OrderedDict({
        "days_ahead": 30,
        "overlay_save_folder": "path/to/folder",
        "date_delimiter": DoubleQuotedScalarString("/"),
        "remove_leading_zero": False,
        "font": "path/to/kometa-font",
        "font_size": 45,
        "font_color": DoubleQuotedScalarString("#FFFFFF"),
        "horizontal_align": "center",
        "vertical_align": "top",
        "horizontal_offset": 0,
        "vertical_offset": 38,
        "back_width": 475,
        "back_height": 55,
        "back_radius": 30,
        "ignore_blank_results": "true",
        "with_status": 0,
        "watch_region": "US",
        "with_original_language": "en",
        "limit": 500,
        "with_watch_monetization_types": "flatrate|free|ads|rent|buy"
    }),

    "use_overlays": OrderedDict({
        "upcoming_series": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#FC4E03"),
            "text": DoubleQuotedScalarString("U P C O M I N G"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "new_series": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#008001"),
            "text": DoubleQuotedScalarString("N E W  S E R I E S"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "new_airing_next": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#008001"),
            "text": DoubleQuotedScalarString("N E W - A I R S "),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "airing_series": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#003880"),
            "text": DoubleQuotedScalarString("A I R I N G"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "airing_today": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#003880"),
            "text": DoubleQuotedScalarString("A I R S  T O D A Y"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "airing_next": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#003880"),
            "text": DoubleQuotedScalarString("A I R I N G "),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "ended_series": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#000000"),
            "text": DoubleQuotedScalarString("E N D E D"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "canceled_series": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#CF142B"),
            "text": DoubleQuotedScalarString("C A N C E L E D"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "returning_series": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#103197"),
            "text": DoubleQuotedScalarString("R E T U R N I N G"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        },
        "returns_next": {
            "use": True,
            "back_color": DoubleQuotedScalarString("#103197"),
            "text": DoubleQuotedScalarString("R E T U R N S "),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }
    }),

    "returning_soon_collection": OrderedDict({
        "use": True,
        "collection_save_folder": "path/to/folder",
        "collection_days_ahead": 30,
        "days_last_aired": 45,
        "use_poster": False,
        "poster_source": "file",
        "poster_path": "path/to/kometa-poster",
        "visible_home": "true",
        "visible_shared": "true",
        "visible_library": "false",
        "summary": DoubleQuotedScalarString("Shows returning soon!"),
        "minimum_items": 1,
        "delete_below_minimum": "true",
        "sort_title": DoubleQuotedScalarString("!010_Returning")
    }),

    "in_history_collection": OrderedDict({
        "use": True,
        "in_history_save_folder": "path/to/folder",
        "in_history_range": "weeks",
        "starting_year": 1980,
        "ending_year": 2024,
        "use_poster": False,
        "poster_source": "file",
        "poster_path": "path/to/kometa-poster",
        "visible_home": "false",
        "visible_shared": "false",
        "visible_library": "true",
        "minimum_items": 1,
        "delete_below_minimum": "true",
        "sort_title": DoubleQuotedScalarString("!012_In_History")
    }),

    "movie_new_release": OrderedDict({
        "use": True,
        "new_movie_save_folder": "path/to/folder",
        "days_to_consider_new": 90,
        "back_color": DoubleQuotedScalarString("#008001"),
        "text": DoubleQuotedScalarString("N E W  R E L E A S E"),
        "font_color": DoubleQuotedScalarString("#FFFFFF")
    })
})

def create_settings_file(main_directory, run_now, run_now_env, in_docker):
    settings_file_path = os.path.join(main_directory, settings_filename)

    try:
        logger.info(f"Settings file not found at '{settings_file_path}', creating a default settings file.")
        with open(settings_file_path, 'w') as file:
            file.write(comment)
            yaml.dump(settings, file)

        with open(settings_file_path, 'r+') as file:
            yaml_output = file.read()
            formatted_output = add_blank_lines(yaml_output)
            file.seek(0)
            file.write(formatted_output)
            file.truncate()
        logger.info(f"Created settings file at '{settings_file_path}'")
        
        if in_docker and not (run_now or run_now_env):
            logger.info("Please edit the 'overlay-settings.yml' to your liking. Overlays will be created at scheduled run.")
            logger.info("If you would like to create overlays now, set RUN_NOW to True in your compose file and restart the container or complete a manual run.")

        if in_docker and (run_now or run_now_env):
            logger.info("Please edit the 'overlay-settings.yml' to your liking. Restart the container to create overlays now.")

        if not in_docker:
            logger.info("Please edit the 'overlay-settings.yml' to your liking. Run the script again to create overlays.")
                    
    except Exception as e:
        logger.error(f"Error creating settings file: {e}")

def load_settings(main_directory, log_message=True):
    settings_file_path = os.path.join(main_directory, settings_filename)

    if not os.path.exists(settings_file_path):
        logger.info(f"Settings file not found at '{settings_file_path}', creating a new one.")
        create_settings_file(main_directory)

    try:
        with open(settings_file_path, 'r') as file:
            if log_message:
                logger.info(f"Loading settings from '{settings_file_path}'")
            return yaml.load(file)
    
    except Exception as e:
        logger.error(f"Error loading settings file: {e}")
        raise

def update_dict(existing, defaults):
    updated = OrderedDict()

    for key, value in defaults.items():
        if key == "libraries":
            if key in existing:
                updated[key] = existing[key]
            continue

        if key in existing:
            if isinstance(value, dict):
                updated[key] = update_dict(existing[key], value)
            else:
                updated[key] = existing[key]
        else:
            updated[key] = value

    for key, value in existing.items():
        if key not in updated:
            updated[key] = value

    return updated

def update_settings_file(main_directory):
    settings_file_path = os.path.join(main_directory, settings_filename)
    
    try:
        logger.info("Checking settings file for missing or new updated sections...")
        existing_settings = load_settings(main_directory, log_message=False)

        updated_settings = update_dict(existing_settings, settings)

        if existing_settings != updated_settings:
            with open(settings_file_path, 'w') as file:
                file.write(comment)
                yaml.dump(updated_settings, file)

            with open(settings_file_path, 'r+') as file:
                yaml_output = file.read()
                formatted_output = add_blank_lines(yaml_output)
                file.seek(0)
                file.write(formatted_output)
                file.truncate()
                
            logger.info(f"Updated settings file at '{settings_file_path}' with missing sections")
        else:
            logger.info(f"No updates were made to the settings file at '{settings_file_path}'")
            
    except Exception as e:
        logger.error(f"Error updating settings file: {e}")
