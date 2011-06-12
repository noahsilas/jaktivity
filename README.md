# Jaktivity
Jaktivity is a django app to log activity on a django powered website.

## Dependencies
* Django 1.3+

## Installing Jaktivity
* Put `jaktivity` on your python path
* Add `jaktivity` to `INSTALLED_APPS` in your settings
* syncdb (or run migrations if you are using 
  [south](http://south.aeracode.org/))
* Add `jaktivity.middleware.ActivityLogMiddleware` to `MIDDLEWARE_CLASSES` in
  your settings

### Adding a web view for the activity logs
* Add `jaktivity` to your urls
        patterns += ('', (r'^activity/', include('jaktivity.urls', namespace='jaktivity')),)
Sample templates are available in the sample_templates directory.

## Using Jaktivity
### What gets logged
For HTTP requests that are 'unsafe' (not having HTTP method `GET` or `HEAD`):
* date
* remote IP Address
* django auth username (if logged in with django.contrib.auth)
* request method
* request host
* request path
* python path of the view resolved to
* args passed to the view
* response status code (if not 500)
* exception type (if 500)

### Human Readable Messages
A view can set a human readable message onto its log entry:
        def view(request):
            if request.method == 'POST':
                request.log.message = 'Edited a widget'

If you want to add messages to views from third party apps, you can simply
add a log_message attribute to the view.
        from django.contrib.auth.views import login
        login.log_message = 'Logged In'

You can also specify a callable object instead of a string; Jaktivity will
call it with the same arguments as the view and assign the result of the
callable to the message.

### Log Notes
Log entries may have multiple notes attached to them. You can add a note to a
log anytime:
        def view(request):
            for item in request.POST.getlist('values'):
                request.log.note("Adding item %s" % item)


## Customizing Jaktivity
### Safe Methods
By default Jaktivity will not log requests with an HTTP method of `GET` or 
`HEAD`. You can adjust what methods jactivity considers 'safe' (meaning they
will not be logged) by setting `ACTIVITY_SAFE_METHODS` in your settings. For
instance, if you do not want to log requests with a `DELETE` method, set the
following:
        JAKTIVITY_SAFE_METHODS = ('GET', 'HEAD', 'DELETE')

### Per-View overrides
You may override the SAFE_METHODS by marking individual views as `always_log`
or `never_log`:
        def view(request):
            return HttpResponse()
        view.always_log = True

### Saving HTTP Headers
By default, Jaktivity does not save any of the HTTP Headers. You may specify
which headers you would like to save with the `ACTIVITY_SAVE_HEADERS` setting.

Example: to save User-Agent strings, add the following to your settings:
        JAKTIVITY_SAVE_HEADERS = ('HTTP_USER_AGENT',)

### Saving HTTP Parameters
Jaktivity records all HTTP parameters, unless they are named any of the
following:
* csrfmiddlewaretoken
* password

You may override this list with the `JAKTIVITY_IGNORE_PARAMS` setting.

## Author
Noah Silas (noah@mahalo.com)