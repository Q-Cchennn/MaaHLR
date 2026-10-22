"""Save an original Android screenshot without sending game input."""
import argparse
from datetime import datetime
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--adb', default='adb')
    parser.add_argument('--serial', required=True)
    parser.add_argument('--name', default='screen')
    args = parser.parse_args()
    if not args.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.name):
        parser.error('--name accepts letters, numbers, underscores and hyphens only')
    try:
        result = subprocess.run([args.adb, '-s', args.serial, 'exec-out', 'screencap', '-p'], capture_output=True, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, f'ADB capture failed: {exc}\n')
    if not result.stdout.startswith(b'\x89PNG\r\n\x1a\n'):
        parser.exit(1, 'ADB did not return a PNG. Check the device connection.\n')
    folder = Path(__file__).resolve().parents[1] / 'screenshots'
    folder.mkdir(exist_ok=True)
    target = folder / f'{datetime.now():%Y%m%d_%H%M%S_%f}_{args.name}.png'
    target.write_bytes(result.stdout)
    print(target)


if __name__ == '__main__':
    main()
