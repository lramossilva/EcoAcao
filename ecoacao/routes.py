from flask import Blueprint, flash, redirect, render_template, request, url_for

from ecoacao.db import get_db


bp = Blueprint("actions", __name__)
TITLE_MAX_LENGTH = 80
DESCRIPTION_MAX_LENGTH = 240


@bp.get("/")
def index():
    db = get_db()
    actions = db.execute(
        "SELECT id, title, description, completed FROM actions ORDER BY id DESC"
    ).fetchall()
    total = len(actions)
    completed = sum(action["completed"] for action in actions)
    progress = round(completed / total * 100) if total else 0

    return render_template(
        "index.html",
        actions=actions,
        total=total,
        completed=completed,
        progress=progress,
    )


@bp.post("/actions")
def create_action():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("Informe um nome para a ação.", "error")
    elif len(title) > TITLE_MAX_LENGTH:
        flash(f"O nome deve ter até {TITLE_MAX_LENGTH} caracteres.", "error")
    elif len(description) > DESCRIPTION_MAX_LENGTH:
        flash(
            f"A descrição deve ter até {DESCRIPTION_MAX_LENGTH} caracteres.",
            "error",
        )
    else:
        db = get_db()
        db.execute(
            "INSERT INTO actions (title, description) VALUES (?, ?)",
            (title, description),
        )
        db.commit()
        flash("Ação ecológica cadastrada!", "success")

    return redirect(url_for("actions.index"))


@bp.post("/actions/<int:action_id>/complete")
def complete_action(action_id):
    db = get_db()
    cursor = db.execute(
        "UPDATE actions SET completed = 1 WHERE id = ? AND completed = 0",
        (action_id,),
    )
    db.commit()

    if cursor.rowcount:
        flash("Ação concluída. Mandou bem!", "success")
    else:
        flash("Ação não encontrada ou já concluída.", "error")

    return redirect(url_for("actions.index"))
