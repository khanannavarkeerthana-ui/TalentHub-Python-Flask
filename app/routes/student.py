from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from . import role_required
from ..db import get_db
from .. import repositories as repo, services as svc

bp = Blueprint("student", __name__, url_prefix="/student")


@bp.route("/dashboard")
@role_required("student")
def dashboard():
    db, sid = get_db(), session["uid"]
    apps = repo.applications_by_student(db, sid)
    interviews = {a["application_id"]: repo.interviews_by_application(db, a["application_id"]) for a in apps}
    return render_template("student_dashboard.html", apps=apps, interviews=interviews,
                           offers=repo.offers_by_student(db, sid),
                           notes=repo.notifications_by_student(db, sid))


@bp.route("/profile", methods=["GET", "POST"])
@role_required("student")
def profile():
    db, sid = get_db(), session["uid"]
    if request.method == "POST":
        try:
            svc.update_profile(db, sid, request.form)
            flash("Profile updated.", "ok")
            return redirect(url_for("student.profile"))
        except svc.ServiceError as e:
            flash(str(e), "error")
    # password_hash is never passed to the template
    s = dict(repo.get_student(db, sid))
    s.pop("password_hash", None)
    return render_template("profile.html", s=s, skills=repo.list_skills(db))


@bp.route("/apply/<int:job_id>", methods=["POST"])
@role_required("student")
def apply(job_id):
    try:
        svc.apply_to_job(get_db(), session["uid"], job_id)
        flash("Application submitted.", "ok")
        return redirect(url_for("student.dashboard"))
    except svc.ServiceError as e:
        flash(str(e), "error")
        return redirect(url_for("main.job_detail", job_id=job_id))


@bp.route("/offers/<int:offer_id>/respond", methods=["POST"])
@role_required("student")
def respond(offer_id):
    try:
        svc.respond_offer(get_db(), session["uid"], offer_id, request.form.get("decision"))
        flash("Response recorded.", "ok")
    except svc.ServiceError as e:
        flash(str(e), "error")
    return redirect(url_for("student.dashboard"))


@bp.route("/notifications/read", methods=["POST"])
@role_required("student")
def read_notifications():
    db = get_db()
    with db:
        repo.mark_notifications_read(db, session["uid"])
    return redirect(url_for("student.dashboard"))
