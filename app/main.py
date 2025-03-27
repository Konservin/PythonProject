from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.models import Filter
from app.db import SessionLocal

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models import Filter, Criteria, FilterType, FilterSubtype, TypeSubtypeAssoc, FilterValueType
from app.db import get_db
import logging

from fastapi.staticfiles import StaticFiles



logger = logging.getLogger(__name__)
logger.warning("Something happened!")


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

@app.get("/filters-table", response_class=HTMLResponse)
def filters_table(request: Request, db: Session = Depends(get_db)):
    filters = db.query(Filter).all()
    return templates.TemplateResponse("filters.html", {"request": request, "filters": filters})

@app.get("/filters/{filter_id}/edit", response_class=HTMLResponse)
def edit_filter(filter_id: int, request: Request, db: Session = Depends(get_db)):
    filter = db.query(Filter).filter(Filter.id == filter_id).first()

    if not filter:
        return templates.TemplateResponse("not_found.html", {"request": request}, status_code=404)

    context = get_filter_form_context(request, db, filter)
    return templates.TemplateResponse("edit_filter.html", context)

@app.get("/filters/new", response_class=HTMLResponse)
def new_filter_form(request: Request, db: Session = Depends(get_db)):
    context = get_filter_form_context(request, db)
    return templates.TemplateResponse("edit_filter.html", context)

@app.post("/filters/new")
async def create_filter(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    name = form.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Filter name is required")

    new_filter = Filter(name=name)
    db.add(new_filter)
    db.commit()
    db.refresh(new_filter)

    new_types = form.getlist("new_type[]")
    new_subtypes = form.getlist("new_subtype[]")
    new_values = form.getlist("new_value[]")

    for type_id, subtype_id, value in zip(new_types, new_subtypes, new_values):
        if not value:
            continue
        new_criteria = Criteria(
            filter_id=new_filter.id,
            type_id=type_id,
            subtype_id=subtype_id,
            value=value
        )
        db.add(new_criteria)

    db.commit()
    return RedirectResponse("/filters-table", status_code=303)

@app.post("/filters/{filter_id}/edit")
async def update_filter(filter_id: int, request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    filter = db.query(Filter).filter(Filter.id == filter_id).first()
    print('filter:', filter)
    if not filter:
        raise HTTPException(status_code=404, detail="Filter not found")

    filter.name = form.get("name")
    logger.warning("name: " + filter.name)

    # --- Handle existing criteria ---
    criteria_ids_in_form = form.getlist("criteria_ids")
    updated_criteria_ids = set()
    #breakpoint()

    for cid in criteria_ids_in_form:
        cid = int(cid)
        #logger.warning("cid: " + cid)
        criteria = next((c for c in filter.criteria if c.id == cid), None)
        if not criteria:
            continue
        criteria.type_id = int(form.get(f"type_{cid}"))
        criteria.subtype_id = int(form.get(f"subtype_{cid}"))
        criteria.value = form.get(f"value_{cid}")
        # Not resolving type/subtype for now
        updated_criteria_ids.add(cid)

    # --- Remove deleted criteria ---
    for c in list(filter.criteria):
        if c.id not in updated_criteria_ids:
            db.delete(c)

    # --- Add new criteria ---
    new_types = form.getlist("new_type[]")
    new_subtypes = form.getlist("new_subtype[]")
    new_values = form.getlist("new_value[]")

    for type_id, subtype_id, value in zip(new_types, new_subtypes, new_values):
        if not value:
            continue
        new_criteria = Criteria(
            filter=filter,
            type_id=type_id,  # TODO: Replace with logic to resolve or create type/subtype IDs
            subtype_id=subtype_id,
            value=value
        )
        db.add(new_criteria)

    db.commit()
    return RedirectResponse("/filters-table", status_code=302)

@app.post("/filters/{filter_id}/delete")
def delete_filter(filter_id: int, db: Session = Depends(get_db)):
    filter = db.query(Filter).filter(Filter.id == filter_id).first()
    if not filter:
        raise HTTPException(status_code=404, detail="Filter not found")

    db.delete(filter)
    db.commit()
    return RedirectResponse("/filters-table", status_code=303)

@app.get("/filters")
def list_filters(db: Session = Depends(get_db)):
    filters_assoc = []

    filters = db.query(Filter).all()

    for f in filters:
        criteria_strings = [
            f"{c.filter_type.name} {c.filter_subtype.name} {c.value}" for c in f.criteria
        ]
        criteria_combined = ", ".join(criteria_strings)

        filters_assoc.append({
            "id": f.id,
            "name": f.name,
            "criteria": criteria_combined
        })

    return filters_assoc

@app.get("/subtypes/{type_id}")
def get_subtypes(type_id: int, db: Session = Depends(get_db)):
    associations = db.query(TypeSubtypeAssoc).filter(TypeSubtypeAssoc.type_id == type_id).all()
    subtypes = [assoc.subtype for assoc in associations]
    return JSONResponse(content=[{"id": s.id, "name": s.name} for s in subtypes])

def get_filter_form_context(request: Request, db: Session, filter: Filter = None):
    types = db.query(FilterType).all()
    subtypes = db.query(FilterSubtype).all()
    value_types = db.query(FilterValueType).all()

    subtypes_by_type = {}
    for s in subtypes:
        subtypes_by_type.setdefault(s.type_id, []).append({"id": s.id, "name": s.name})

    value_types_dict = {v.type_id: v.value_type for v in value_types}

    return {
        "request": request,
        "filter": filter,
        "types": types,
        "subtypes": subtypes,
        "subtypes_by_type_json": subtypes_by_type,
        "value_types_dict": value_types_dict
    }