## Dependencies

### Packaged software

 * python-django
 * libjs-jquery
 * ruby-compass

## Setting configuration params

### incubadora/settings.py.sample

After checking out the source code, you have to copy the
`incubadora/settings.py.sample` to `incubadora/settings.py`. In this file, you'll be able to choose
the database name that messages and static file.

### Sass Vs. Css: Generating css files

We're not using css directly in this app. All styles are being defined
in the `sass` language. So, before running the app, you have to compile
the sass files, use the following:

    $ compass compile static

If you aim to help the project sending patches, maybe it would be good
to start a watcher that will compile sass files when they change. To do
it, use it:

    $ compass watch static

## Actually running the app

Currently, you just have to issue:

    $ python manage.py syncdb
    $ python manage.py runserve 0.0.0.0:port
