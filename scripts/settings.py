import os
import logging
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from ruamel.yaml.representer import RoundTripRepresenter
from ruamel.yaml.comments import CommentedMap

yaml = YAML()
yaml.default_flow_style = False
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.allow_unicode = True
yaml.preserve_quotes = True

yaml.Representer = RoundTripRepresenter
yaml.Representer.add_representer(CommentedMap, RoundTripRepresenter.represent_dict)

logger = logging.getLogger(__name__)

settings_filename = "settings.yml"

settings = CommentedMap({
    "libraries": CommentedMap({
        "TV Shows": CommentedMap({
            "is_anime": False,
            "use_watch_region": True
        }),
        "4k TV Shows": CommentedMap({
            "is_anime": False,
            "use_watch_region": True
        }),
        "Anime": CommentedMap({
            "is_anime": True,
            "use_watch_region": True
        })
    }),

    "overlay_settings": CommentedMap({
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

    "use_overlays": CommentedMap({
        "upcoming_series": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#FC4E03"),
            "text": DoubleQuotedScalarString("U P C O M I N G"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "new_series": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#008001"),
            "text": DoubleQuotedScalarString("N E W  S E R I E S"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "new_airing_next": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#008001"),
            "text": DoubleQuotedScalarString("N E W - A I R S "),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "airing_series": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#003880"),
            "text": DoubleQuotedScalarString("A I R I N G"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "airing_today": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#003880"),
            "text": DoubleQuotedScalarString("A I R S  T O D A Y"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "airing_next": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#003880"),
            "text": DoubleQuotedScalarString("A I R I N G "),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "ended_series": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#000000"),
            "text": DoubleQuotedScalarString("E N D E D"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "canceled_series": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#CF142B"),
            "text": DoubleQuotedScalarString("C A N C E L E D"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "returning_series": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#103197"),
            "text": DoubleQuotedScalarString("R E T U R N I N G"),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        }),
        "returns_next": CommentedMap({
            "use": True,
            "back_color": DoubleQuotedScalarString("#103197"),
            "text": DoubleQuotedScalarString("R E T U R N S "),
            "font_color": DoubleQuotedScalarString("#FFFFFF")
        })
    }),

    "movie_new_release": CommentedMap({
        "use": True,
        "new_movie_save_folder": "path/to/folder",
        "days_to_consider_new": 90,
        "back_color": DoubleQuotedScalarString("#008001"),
        "text": DoubleQuotedScalarString("N E W  R E L E A S E"),
        "font_color": DoubleQuotedScalarString("#FFFFFF")
    }),
    
    "returning_soon_collection": CommentedMap({
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

    "in_history_collection": CommentedMap({
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

    "top_10": CommentedMap({
        "top_10_overlay": CommentedMap({
            "use": True,
            "overlay_save_folder": "path/to/folder",
            "vertical_align": "top",
            "horizontal_align": "left",
            "vertical_offset": 105,
            "horizontal_offset": 30,
            "font": "path/to/kometa-font",
            "font_size": 45,
            "font_color": DoubleQuotedScalarString("#80FF40"),
            "back_width": 215,
            "back_height": 70,
            "back_radius": 10,
            "back_color": DoubleQuotedScalarString("#000000B3")
        }),
        "top_10_collection": CommentedMap({
            "use": True,
            "collection_save_folder": "path/to/folder",
            "visible_home": "false",
            "visible_library": "true",
            "visible_shared": "false",
            "minimum_items": 1,
            "delete_below_minimum": 'true',
            "sort_title_prefix": DoubleQuotedScalarString("!020")
        })
    })
})

def add_comments(settings):
    max_key_length = max(len(key) for key in settings.keys())

    # Schema comment
    settings.yaml_set_comment_before_after_key("libraries", before=" yaml-language-server: $schema=https://raw.githubusercontent.com/dweagle/komanager/main/json_schema/settings.json\n\n")

    # Section comments and spacing
    settings.yaml_set_comment_before_after_key("libraries", before="Status Overlay Settings")
    settings.yaml_set_comment_before_after_key("overlay_settings", before="\n\n")
    settings.yaml_set_comment_before_after_key("use_overlays", before="\n\n")
    settings.yaml_set_comment_before_after_key("movie_new_release", before="\nNew Movie Release Settings - Uses 'status overlay' settings.")
    settings.yaml_set_comment_before_after_key("returning_soon_collection", before="\nReturning Soon Collection Settings")
    settings.yaml_set_comment_before_after_key("in_history_collection", before="\nIn History Collection Settings")
    settings.yaml_set_comment_before_after_key("top_10", before="\nTop 10 Overlay and Collection Settings")

    # End of line comments
    settings.yaml_add_eol_comment("# Plex library (SHOWS ONLY) names to create Kometa overlays for.", "libraries", column=max_key_length + 5)

def create_settings_file(main_directory, run_now, run_now_env, in_docker):
    settings_file_path = os.path.join(main_directory, settings_filename)

    try:
        logger.info(f"Settings file not found at '{settings_file_path}', creating a default settings file.")
        add_comments(settings)
        with open(settings_file_path, 'w') as file:
            yaml.dump(settings, file)

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
    updated = CommentedMap()

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
        settings_changed = existing_settings != updated_settings

        with open(settings_file_path, 'w') as file:
            yaml.dump(updated_settings, file)

        with open(settings_file_path, 'r') as file:
            updated_settings_with_comments = yaml.load(file)

        add_comments(updated_settings_with_comments)

        with open(settings_file_path, 'w') as file:
            yaml.dump(updated_settings_with_comments, file)

        if settings_changed:
            logger.info(f"Updated settings file at '{settings_file_path}' with missing sections and comments")
        else:
            logger.info(f"No updates were made to the settings file at '{settings_file_path}'")

    except Exception as e:
        logger.error(f"Error updating settings file: {e}")