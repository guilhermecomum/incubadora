# Incubadora - Versão final

INCUBADORA é um simulador de sociedade. Os “interatores” usam seus
próprios portáteis com wi-fi (celulares, tablets ou computadores) para
criar uma narrativa. Que sociedade é possível construir com estas
regras?


## Dependencies

### Packaged software

 * python-django ( >= 1.4 )
 * python-imaging ( >= 1.1.7 )
 * libjs-jquery ( >= 1.7.2 )
 * libjs-jquery-ui (>= 1.8.23 )
 * ruby-compass ( >= 0.12.2 )

## Setting configuration params

### incubadora/settings.py.sample

After checking out the source code, you have to copy the
`incubadora/settings.py.sample` to `incubadora/settings.py`. In this file,
you'll be able to choose the database name that messages and static files
(STATICFILES_DIRS and MEDIA_ROOT).

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
    $ python manage.py runserver 0.0.0.0:port
