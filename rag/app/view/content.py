from fake_useragent import UserAgent
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
from flask import g

from app.db import get_db
from app.rag import save_urls
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
            # current_app.config['rag'].save_content(user=str(g.user['id']), content=contents,
            #                                        content_type="user_contents")
            db.commit()

            # add urls

            urls_list = urls.split("\n")
            urls_list = [url.strip("\n\t\r ") for url in urls_list if len(url.strip("\r\t\n")) > 0]

            if len(urls_list) > 0 and urls.strip("\n\t\r ") != g.user['urls'].strip("\n\t\r "):
                current_app.logger.info(f"Need to refetch {len(urls_list)} urls")
                # change detected. need to refetch all urls
                header_template = {}
                header_template["User-Agent"] = UserAgent().random
                save_urls(current_app.config['rag'], urls=urls_list, user=str(g.user['id']), content_type="user_urls")
                # current_app.config['rag'].save_urls(urls=urls_list,  # all urls
                #                                     user=str(g.user['id']), headers=header_template,
                #                                     content_type="user_urls", max_depth=3)
            g.user['contents'] = contents
            g.user['urls'] = urls
            flash("Saved")
            return redirect(url_for("content.edit"))

    return render_template("content/edit.html", contents=contents, urls=urls)
