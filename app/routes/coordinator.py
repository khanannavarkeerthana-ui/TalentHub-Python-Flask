from flask import Blueprint, flash, redirect, render_template, request, url_for
from . import role_required
from ..db import get_db
from .. import repositories as repo, services as svc

bp = Blueprint("coordinator", __name__, url_prefix="/coordinator")


@bp.route("/dashboard")
@role_required("coordinator")
def dashboard():
    db = get_db()
    return render_template("coordinator_dashboard.html", apps=repo.all_applications(db),
                           skills=repo.list_skills(db), jobs=repo.list_jobs(db))


@bp.route("/skills", methods=["POST"])
@role_required("coordinator")
def add_skill():
    try:
        svc.add_skill(get_db(), request.form.get("skill_name"), request.form.get("skill_type"))
        flash("Skill added.", "ok")
    except svc.ServiceError as e:
        flash(str(e), "error")
    return redirect(url_for("coordinator.dashboard"))
