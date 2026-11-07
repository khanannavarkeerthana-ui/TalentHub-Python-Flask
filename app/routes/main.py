from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from ..db import get_db
from .. import repositories as repo, services as svc

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    return render_template("jobs.html", jobs=repo.list_jobs(get_db(), q), q=q)


@bp.route("/jobs/<int:job_id>")
def job_detail(job_id):
    db = get_db()
    job = repo.get_job(db, job_id)
    if not job:
        return render_template("error.html", msg="Job not found"), 404
    eligibility = None
    if session.get("role") == "student":
        student = repo.get_student(db, session["uid"])
        eligibility = svc.check_eligibility(student, job)
    return render_template("job_detail.html", job=job, eligibility=eligibility)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role", "student")
        uid = svc.authenticate(get_db(), __import__("flask").current_app.config, role,
                               request.form.get("email"), request.form.get("password", ""))
        if uid is None:
            flash("Invalid email or password.", "error")
        else:
            session.clear()
            session["role"], session["uid"] = role, uid
            return redirect(url_for({"student": "student.dashboard", "company": "company.dashboard",
                                     "coordinator": "coordinator.dashboard"}[role]))
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@bp.route("/register/student", methods=["GET", "POST"])
def register_student():
    db = get_db()
    if request.method == "POST":
        try:
            svc.register_student(db, request.form)
            flash("Account created. Please log in.", "ok")
            return redirect(url_for("main.login"))
        except svc.ServiceError as e:
            flash(str(e), "error")
    return render_template("register_student.html", skills=repo.list_skills(db))


@bp.route("/register/company", methods=["GET", "POST"])
def register_company():
    if request.method == "POST":
        try:
            svc.register_company(get_db(), request.form)
            flash("Company account created. Please log in.", "ok")
            return redirect(url_for("main.login"))
        except svc.ServiceError as e:
            flash(str(e), "error")
    return render_template("register_company.html")
