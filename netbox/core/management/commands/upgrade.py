"""Run the NetBox application tasks required after installing or upgrading NetBox.

The command runs the NetBox application-level tasks that prepare the database and
static assets after the package and configuration are already in place - for both a
fresh installation and an upgrade. It does not perform host or bootstrap work
(creating the virtual environment, installing packages, configuring services); that
stays in upgrade.sh and the documented pip steps.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run the NetBox application tasks required after installing or upgrading NetBox."

    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true', dest='no_input',
                            help="Do not prompt for user input.")
        parser.add_argument('--readonly', action='store_true', dest='readonly',
                            help="Skip all tasks that modify the database or filesystem "
                                 "(no migrations, no static collection).")
        parser.add_argument('--skip-migrations', action='store_true', dest='skip_migrations',
                            help="Skip applying database migrations.")
        parser.add_argument('--skip-static', action='store_true', dest='skip_static',
                            help="Skip collecting static files.")
        parser.add_argument('--skip-reindex', action='store_true', dest='skip_reindex',
                            help="Skip rebuilding the search index.")

    def handle(self, *args, **options):
        out, style = self.stdout, self.style
        out.write(style.SUCCESS("Running NetBox upgrade tasks..."))

        # Database migrations (writes to the database)
        if options['skip_migrations'] or options['readonly']:
            out.write("Skipping database migrations.")
        else:
            out.write("Applying database migrations...")
            call_command('migrate', interactive=not options['no_input'], stdout=out)

        # Missing cable paths (writes to the database)
        if options['readonly']:
            out.write("Skipping cable path check.")
        else:
            out.write("Checking for missing cable paths...")
            call_command('trace_paths', no_input=options['no_input'], stdout=out)

        # Static files (filesystem)
        if options['skip_static'] or options['readonly']:
            out.write("Skipping static file collection.")
        else:
            out.write("Collecting static files...")
            call_command('collectstatic', interactive=not options['no_input'], stdout=out)

        # Stale content types (writes to the database)
        if options['readonly']:
            out.write("Skipping stale content type removal.")
        else:
            out.write("Removing stale content types...")
            call_command('remove_stale_contenttypes', interactive=not options['no_input'], stdout=out)

        # Search index (writes to the database)
        if options['skip_reindex'] or options['readonly']:
            out.write("Skipping search index rebuild.")
        else:
            out.write("Rebuilding the search index (lazily)...")
            call_command('reindex', lazy=True, stdout=out)

        # Expired sessions (writes to the database)
        if options['readonly']:
            out.write("Skipping expired session cleanup.")
        else:
            out.write("Clearing expired sessions...")
            call_command('clearsessions', stdout=out)

        out.write(style.SUCCESS("Finished NetBox upgrade tasks."))
