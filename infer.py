"""Public DaYu-TC inference entry point. Neural implementation is supplied as a binary wheel."""
def main():
    try:
        from dayu_tc_runtime.api import main as run
    except ImportError as exc:
        raise SystemExit('Install the matching dayu_tc_runtime binary wheel from the release assets first.') from exc
    run()

if __name__ == '__main__':
    main()
