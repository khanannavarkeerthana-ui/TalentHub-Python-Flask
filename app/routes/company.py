from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from . import current_user, role_required
from ..db import get_db
from .. import repositories as repo, services as svc

bp = Blueprint("company", __name__)


@bp.route("/company/dashboard")
@role_required("company")
def dashboard():
    db = get_db()
    return render_template("company_dashboard.html", jobs=repo.jobs_by_company(db, session["uid"]),
                           company=repo.get_company(db, session["uid"]))


@bp.route("/company/jobs/new", methods=["GET", "POST"])
@role_required("company")
def new_job():
    db = get_db()
    if request.method == "POST":
        try:
            svc.create_job(db, session["uid"], request.form)
            flash("Job listing published.", "ok")
            return redirect(url_for("company.dashboard"))
        except svc.ServiceError as e:
            flash(str(e), "error")
    return render_template("job_form.html", skills=repo.list_skills(db))


@bp.route("/manage/jobs/<int:job_id>/applicants")
@role_required("company", "coordinator")
def applicants(job_id):
    db = get_db()
    job = repo.get_job(db, job_id)
    if not job:
        abort(404)
    user = current_user()
    if user["role"] == "company" and job["company_id"] != user["id"]:
        abort(403)
    return render_template("applicants.html", job=job, apps=repo.applications_by_job(db, job_id))


def _load_managed(db, application_id):
    app = repo.get_application(db, application_id)
    if not app:
        abort(404)
    if not svc.can_manage(current_user(), app):
        abort(403)
    return app


@bp.route("/manage/applications/<int:application_id>")
@role_required("company", "coordinator")
def manage(application_id):
    db = get_db()
    app = _load_managed(db, application_id)
    return render_template("manage_application.html", app=app,
                           interviews=repo.interviews_by_application(db, application_id),
                           offer=repo.offer_by_application(db, application_id),
                           next_statuses=sorted(svc.TRANSITIONS[app["status"]] - {"Scheduled"}))


def _act(application_id, fn, ok_msg):
    db = get_db()
    _load_managed(db, application_id)
    try:
        fn(db)
        flash(ok_msg, "ok")
    except svc.ServiceError as e:
        flash(str(e), "error")
    return redirect(url_for("company.manage", application_id=application_id))


@bp.route("/manage/applications/<int:application_id>/status", methods=["POST"])
@role_required("company", "coordinator")
def set_status(application_id):
    return _act(application_id, lambda db: svc.change_status(db, application_id, request.form.get("status")),
                "Status updated.")


@bp.route("/manage/applications/<int:application_id>/interview", methods=["POST"])
@role_required("company", "coordinator")
def interview(application_id):
    return _act(application_id, lambda db: svc.schedule_interview(db, application_id, request.form),
                "Interview scheduled.")


@bp.route("/manage/applications/<int:application_id>/offer", methods=["POST"])
@role_required("company", "coordinator")
def offer(application_id):
    return _act(application_id, lambda db: svc.make_offer(db, application_id, request.form),
                "Offer created.")
