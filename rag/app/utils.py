import functools
import logging

from flask import (
    g
)
from flask import (
    redirect, url_for
)

logger = logging.getLogger(__name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
