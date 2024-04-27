from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
from flask import g

from app.db import get_db

from app.utils import login_required

bp = Blueprint('content', __name__, url_prefix='/content')


@bp.route('/edit', methods=('GET', 'POST'))
@login_required
def edit():
    dict_ = get_db().execute(
        'SELECT contents, urls FROM user WHERE id = ?', (g.user['id'],)
    ).fetchone()
    contents = dict_['contents']
    urls = dict_['urls']
    if request.method == "POST":
        contents = request.form["contents"]
        urls = request.form["urls"]
        error = None
        if not contents:
            error = "content is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE user SET contents = ?, urls = ? WHERE id = ?", (contents, urls, g.user['id'])
            )
            current_app.config['rag'].save_content(user=str(g.user['id']), content=contents, content_type="user_contents")
            db.commit()

            # add urls
            current_urls = set([u.strip("\r\t\n ") for u in g.user['urls'].split("\n") if "http" in u.strip("\r\t\n ") and u.strip("\r\t\n ").index("http") == 0])
            new_urls = []
            urls_list = urls.split("\n")
            for u in urls_list:
                u_ = u.strip("\r\t\n ")
                if "http" in u_ and u_.index("http") == 0 and u_ not in current_urls:
                    new_urls.append(u)
            current_app.logger.info(f"Need to load {len(new_urls)} urls")
            if len(new_urls) > 0:
                # change detected. need to refetch all urls
                current_app.config['rag'].save_urls(urls=urls_list, # all urls
                                                    user=str(g.user['id']), content_type="user_urls", max_depth=3)
            flash("Saved")
            return redirect(url_for("content.edit"))

    return render_template("content/edit.html", contents=contents, urls=urls)
