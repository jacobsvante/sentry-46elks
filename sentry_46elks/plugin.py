"""
sentry_46elks.models
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 by Matt Robenolt.
:license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals
import re
import requests
import sentry_46elks
from django import forms
from django.utils.translation import ugettext_lazy as _
from sentry.plugins.bases.notify import NotificationPlugin


class Sentry46ElksConfigurationForm(forms.Form):
    api_endpoint = forms.CharField(label=_('API Endpoint'), required=True,
                             help_text=_('API URL used for sending the texts'),
                             initial='https://api.46elks.com/a1/SMS')
    api_username = forms.CharField(label=_('API username'), required=True,
        widget=forms.TextInput(attrs={'class': 'span6'}))
    api_password = forms.CharField(label=_('API password'), required=True,
        widget=forms.PasswordInput(render_value=True,
                                   attrs={'class': 'span6'}))
    sender = forms.CharField(label=_('SMS Sender'), required=True,
        help_text=_('The number/name of the sender'),
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +46701234567'}))
    receivers = forms.CharField(label=_('SMS Receivers'), required=True,
        help_text=_('Recipient(s) phone numbers separated by commas ' \
                    'or line breaks'),
        widget=forms.Textarea(attrs={'placeholder': 'e.g. +46701234567, ' \
                                     '+46709876543'}))

    def clean_receivers(self):
        data = self.cleaned_data['receivers']
        phones = set(filter(bool, re.split(r'\s*,\s*|\s+', data)))
        msg_tmpl = '{0} is not a valid phone number.'
        for phone in phones:
            if not re.match(r'^\+\d{10,}$', phone):
                raise forms.ValidationError(msg_tmpl.format(phone))
        return ','.join(phones)

    def clean(self):
        # TODO: Ping Twilio and check credentials (?)
        return self.cleaned_data


class Sentry46ElksPlugin(NotificationPlugin):
    author = 'Jacob Magnusson'
    author_url = 'https://github.com/jmagnusson'
    version = sentry_46elks.__version__
    description = 'A plugin for Sentry which sends SMS notifications via ' \
                  '46elks SMS API'
    resource_links = (
        ('Documentation',
         'https://github.com/jmagnusson/sentry-46elks/blob/master/README.md'),
        ('Bug Tracker',
         'https://github.com/jmagnusson/sentry-46elks/issues'),
        ('Source',
         'https://github.com/jmagnusson/sentry-46elks'),
        ('46elks',
         'http://www.46elks.com/'),
    )
    slug = '46elks'
    title = _('46elks (SMS)')
    conf_title = title
    conf_key = '46elks'
    project_conf_form = Sentry46ElksConfigurationForm

    def is_configured(self, request, project, **kwargs):
        fields = ('api_baseurl', 'api_username', 'api_password', 'sender',
                  'receivers')
        return all([self.get_option(o, project) for o in fields])

    def get_send_to(self, *args, **kwargs):
        # This doesn't depend on email permission... stuff.
        return True

    def notify_users(self, group, event):
        project = group.project
        error_level = event.get_level_display()
        error = event.error().splitlines()
        error = error[0] if len(error) else ''
        body = 'Sentry [{0}] {1}: {2}'.format(project.name, error_level, error)
        body = body[:160]  # Truncate to 160 characters
        endpoint = self.get_option('api_endpoint', project)
        auth = (self.get_option('api_username', project),
                self.get_option('api_password', project))
        sender = self.get_option('sender', project)
        receivers = self.get_option('receivers', project).split(',')

        for receiver in receivers:
            try:
                requests.post(endpoint, auth=auth, data={
                    'from': sender,
                    'to': receiver,
                    'message': body,
                })
            except Exception as e:
                # TODO: Handle
                raise e
