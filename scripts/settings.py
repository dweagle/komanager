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
            "library_type": "show",
            "is_anime": False,
            "use_watch_region": True
        }),
        "4k TV Shows": CommentedMap({
            "library_type": "show",
            "is_anime": False,
            "use_watch_region": True
        }),
        "Anime": CommentedMap({
            "library_type": "show",
            "is_anime": True,
            "use_watch_region": True
        }),
        "Movies": CommentedMap({
            "library_type": "movie",
            "is_anime": False,
            "use_watch_region": True
        })
    }),

    "status_overlay": CommentedMap({
        "overlay_settings": CommentedMap({
            "days_ahead": 30,
            "overlay_save_folder": "path/to/folder",
            "date_format": "%m/%d",
            "date_delimiter": DoubleQuotedScalarString("/"),
            "remove_leading_zero": False,
            "font": "path/to/kometa-font",
            "font_size": 45,
            "font_color": DoubleQuotedScalarString("#FFFFFF"),
            "horizontal_align": "center",
            "vertical_align": "top",
            "horizontal_offset": 0,
            "vertical_offset": 38,
            "use_backdrop": True,
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
        })
    }),

    "movie_new_release": CommentedMap({
        "use": True,
        "new_movie_save_folder": "path/to/folder",
        "days_to_consider_new": 90,
        "use_backdrop": True,
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

    "streaming_overlay": CommentedMap({
        "use": True,
        "streaming_save_folder": "path/to/folder",
        "streaming_image_folder": "path/to/images",
        "vertical_align": "top",
        "horizontal_align": "left",
        "vertical_offset": 35,
        "horizontal_offset": 30,
        "use_backdrop": True,
        "back_width": 215,
        "back_height": 70,
        "back_radius": 10,
        "back_color": DoubleQuotedScalarString("#000000B3"),
        "ignore_blank_results": "true",
        "watch_region": "US",
        "with_original_language": "en",
        "with_watch_monetization_types": "flatrate|free|ads|rent|buy",
        "use_vote_count": True,
        "vote_count": 2,
        "use_extra_streaming": True
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
            "use_backdrop": True,
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

streaming_services = CommentedMap({
    "default_streaming": CommentedMap({
        "Netflix": CommentedMap({"use": True, "limit": 1500, "weight": 180}),
        "AppleTV": CommentedMap({"use": True, "limit": 1500, "weight": 170}),
        "Disney": CommentedMap({"use": True, "limit": 1500, "weight": 160}),
        "Max": CommentedMap({"use": True, "limit": 1500, "weight": 150}),
        "Prime": CommentedMap({"use": True, "limit": 1500, "weight": 140}),
        "Crunchyroll": CommentedMap({"use": True, "limit": 1500, "weight": 130}),
        "YouTube": CommentedMap({"use": True, "limit": 1500, "weight": 120}),
        "Hulu": CommentedMap({"use": True, "limit": 1500, "weight": 100}),
        "Paramount": CommentedMap({"use": True, "limit": 1500, "weight": 90}),
        "Peacock": CommentedMap({"use": True, "limit": 1500, "weight": 80}),
        "Crave": CommentedMap({"use": True, "limit": 1500, "weight": 70}),
        "Discovery+": CommentedMap({"use": True, "limit": 1500, "weight": 60}),
        "NOW": CommentedMap({"use": True, "limit": 1500, "weight": 55}),
        "All 4": CommentedMap({"use": True, "limit": 1500, "weight": 50}),
        "BritBox": CommentedMap({"use": True, "limit": 1500, "weight": 40}),
        "BET+": CommentedMap({"use": True, "limit": 1500, "weight": 30})
    }),

    "extra_streaming": CommentedMap({
        "AMC+": CommentedMap({"use": True, "limit": 1500, "weight": 25}),
        "Freevee": CommentedMap({"use": True, "limit": 1500, "weight": 20}),
        "FuboTV": CommentedMap({"use": True, "limit": 1500, "weight": 20}),
        "FXNOW": CommentedMap({"use": True, "limit": 1500, "weight": 25}),
        "Hoopla": CommentedMap({"use": True, "limit": 1500, "weight": 20}),
        "MGM+": CommentedMap({"use": True, "limit": 1500, "weight": 25}),
        "Starz": CommentedMap({"use": True, "limit": 1500, "weight": 27}),
        "TBS": CommentedMap({"use": True, "limit": 1500, "weight": 25}),
        "TNT": CommentedMap({"use": True, "limit": 1500, "weight": 25}),
        "truTV": CommentedMap({"use": True, "limit": 1500, "weight": 25}),
        "tubiTV": CommentedMap({"use": True, "limit": 1500, "weight": 20}),
        "USA": CommentedMap({"use": True, "limit": 1500, "weight": 25})
    })
})

def set_flow_style(commented_map):
    for value in commented_map.values():
        if isinstance(value, CommentedMap):
            value.fa.set_flow_style()

set_flow_style(streaming_services["default_streaming"])
set_flow_style(streaming_services["extra_streaming"])

streaming_overlay = settings["streaming_overlay"]
streaming_overlay.insert(list(streaming_overlay.keys()).index("use_extra_streaming") + 1, "streaming_services", streaming_services)

def add_comments(settings):
    # End of line comment spacing
    max_key_length = max(len(key) for key in settings.keys())

    # Schema comment
    settings.yaml_set_start_comment(
        "yaml-language-server: $schema=https://raw.githubusercontent.com/"
        "dweagle/komanager/main/json_schema/settings.json\n\n"
    )

    # Section comments and spacing
    settings.yaml_set_comment_before_after_key(
        "libraries",
        before="Plex libraries to create overlays/collections for. "
               "Library type is 'show' or 'movie'."
    )
    settings.yaml_set_comment_before_after_key(
        "status_overlay",
        before="\nSettings for Status Overlay ('show' libraries only)."
    )
    settings.yaml_set_comment_before_after_key(
        "movie_new_release",
        before="\nNew Movie Release Settings - Uses 'status_overlay: overlay_settings'."
    )
    settings.yaml_set_comment_before_after_key(
        "returning_soon_collection",
        before="\nReturning Soon Collection Settings ('show' libraries only)"
    )
    settings.yaml_set_comment_before_after_key(
        "in_history_collection",
        before="\nIn History Collection Settings"
    )
    settings.yaml_set_comment_before_after_key(
        "streaming_overlay",
        before="\nStreaming Overlay Settings ('show' and 'movie' libraries)"
    )
    settings.yaml_set_comment_before_after_key(
        "top_10",
        before="\nTop 10 Overlay and Collection Settings"
    )
    settings["streaming_overlay"]["streaming_services"].yaml_set_comment_before_after_key(
        "default_streaming",
        before="Default Streaming Overlays"
    )
    settings["streaming_overlay"]["streaming_services"].yaml_set_comment_before_after_key(
        "extra_streaming",
        before="Extra Overlays"
    )
    # End of line comments
    settings["status_overlay"].yaml_add_eol_comment(
        "Adjust overlay position, size, font, TMDB settings, save location, etc.",
        "overlay_settings",
        column=max_key_length + 20
    )
    settings["status_overlay"]["overlay_settings"].yaml_add_eol_comment(
        "Kometa must have permissions for save, font, image, and poster paths.",
        "overlay_save_folder",
        column=max_key_length + 20
    )
    settings["status_overlay"]["overlay_settings"].yaml_add_eol_comment(
        "Change status overlay date format: 1 = mm/dd, 2 = dd/mm or use custom format in quotes.  Custom format ignores 'remove_leading_zero' setting",
        "date_format",
        column=max_key_length + 20
    )
    settings["status_overlay"].yaml_add_eol_comment(
        "Turn overlays off/on, adjust font color, back color, and text.",
        "use_overlays",
        column=max_key_length + 20
    )
    settings["streaming_overlay"].yaml_add_eol_comment(
        "Kometa must have permissions for image folder path.",
        "streaming_image_folder",
        column=max_key_length + 20
    )
    settings["streaming_overlay"].yaml_add_eol_comment(
        "Use streaming overlays not found in Kometa default streaming.",
        "use_extra_streaming",
        column=max_key_length + 20
    )

def create_settings_file(main_directory, run_now=False, run_now_env=False, in_docker=False):
    settings_file_path = os.path.join(main_directory, settings_filename)

    try:
        logger.info(f"Settings file not found at '{settings_file_path}', creating a default settings file.")
        add_comments(settings)
        with open(settings_file_path, 'w') as file:
            yaml.dump(settings, file)

        logger.info(f"Created settings file at '{settings_file_path}'")
        
        if in_docker and not (run_now or run_now_env):
            logger.info("Please edit the 'settings.yml' to your liking. Overlays will be created at scheduled run.")
            logger.info("If you would like to create overlays/collections now, set RUN_NOW to True in your compose file and restart the container or complete a manual run.")

        if in_docker and (run_now or run_now_env):
            logger.info("Please edit the 'settings.yml' to your liking. Restart the container to create overlays/collections now.")

        if not in_docker:
            logger.info("Please edit the 'settings.yml' to your liking. Run the script again to create overlays/collections now.")
                    
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
            loaded_settings = yaml.load(file)
            return loaded_settings if loaded_settings is not None else CommentedMap()

    except Exception as e:
        logger.error(f"Error loading settings file: {e}")
        raise

def strip_comments(node):
    if isinstance(node, CommentedMap):
        node.ca.items.clear()
        for value in node.values():
            strip_comments(value)
            
def update_dict(existing, defaults):
    updated = CommentedMap()

    for key, value in defaults.items():
        if key == "libraries":
            if key in existing:
                libraries_without_comments = existing[key]
                strip_comments(libraries_without_comments)
                updated[key] = libraries_without_comments
            else:
                updated[key] = value
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
        strip_comments(updated_settings)
        add_comments(updated_settings)

        if "streaming_services" in updated_settings["streaming_overlay"]:
            if "default_streaming" in updated_settings["streaming_overlay"]["streaming_services"]:
                set_flow_style(updated_settings["streaming_overlay"]["streaming_services"]["default_streaming"])
            if "extra_streaming" in updated_settings["streaming_overlay"]["streaming_services"]:
                set_flow_style(updated_settings["streaming_overlay"]["streaming_services"]["extra_streaming"])

        with open(settings_file_path, 'w') as file:
            yaml.dump(updated_settings, file)

        if settings_changed:
            logger.info(f"Updated settings file at '{settings_file_path}' with missing sections and comments")
        else:
            logger.info(f"No updates were made to the settings file at '{settings_file_path}'")

    except Exception as e:
        logger.error(f"Error updating settings file: {e}")