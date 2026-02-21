import sys
from pathlib import Path
from PIL import Image


def strip_metadata(image_path: Path, backup: bool = True):
    try:
        with Image.open(image_path) as img:
            data = list(img.getdata())

            # Maak nieuwe image zonder EXIF
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(data)

            if backup:
                backup_path = image_path.with_suffix(image_path.suffix + ".backup")
                image_path.rename(backup_path)

            # Opslaan zonder metadata
            clean_img.save(image_path)

        print(f"[OK] Metadata verwijderd: {image_path}")

    except Exception as e:
        print(f"[ERROR] {image_path}: {e}")


def main(folder_path: str):
    folder = Path(folder_path)

    if not folder.exists():
        print("Map bestaat niet.")
        sys.exit(1)

    for file in folder.rglob("*"):
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            strip_metadata(file, backup=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Gebruik: python strip_metadata.py <map_met_fotos>")
        sys.exit(1)

    main(sys.argv[1])