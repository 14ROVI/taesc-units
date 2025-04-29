from pathlib import Path

current_dir = Path(__file__).parent

DATA_DIR = current_dir / "data"
MIRRORS_DIR = DATA_DIR / "mirrors"
UNIT_ICONS_DIR = DATA_DIR / "unit_icons"
META_FILE = DATA_DIR / "meta.json"
GUIS_FILE = DATA_DIR / "guis.json"
UNITS_FILE = DATA_DIR / "units.json"
WEAPONS_FILE = DATA_DIR / "weapons.json"
ESC_GIT_DIR = current_dir / "taesc"
EXTRACT_DIR = current_dir / "extract"