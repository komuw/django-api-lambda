import os
import sys

if __name__ == "__main__":
    import logging

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    root.debug("sys_path, sys_path={sys_path}".format(sys_path=sys.path))
    root.debug("environ, environ={environ}".format(environ=os.environ))
    help("modules")

    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)
