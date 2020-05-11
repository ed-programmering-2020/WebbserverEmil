from django.core.management import execute_from_command_line
import sys, os


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Orpose.settings'
    execute_from_command_line(sys.argv)

