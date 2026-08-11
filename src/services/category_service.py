from fastapi import HTTPException
from src.models.category import Category


def create_category(request, db):
    category_exist = (
        db.query(Category)
        .filter(Category.name == request.name, Category.parent_id == request.parent_id)
        .first()
    )

    if category_exist:
        raise HTTPException(status_code=400, detail="Category already exists")

    if request.parent_id:
        parent = db.query(Category).filter(Category.id == request.parent_id).first()

        if not parent:
            raise HTTPException(status_code=400, detail="Parent category not found")

    new_category = Category(
        name=request.name, description=request.description, parent_id=request.parent_id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def get_categories(db):
    return db.query(Category).filter(Category.is_active == True).all()


def update_category(id, request, db):
    category_exist = db.query(Category).filter(Category.id == id).first()

    if not category_exist:
        raise HTTPException(status_code=400, detail="Category not found")

    if request.name is not None:
        category_exist.name = request.name

    if request.description is not None:
        category_exist.description = request.description

    if request.parent_id is not None:
        if request.parent_id == category_exist.id:
            raise HTTPException(
                status_code=400, detail="Category cannot be its own parent"
            )
        category_exist.parent_id = request.parent_id

    if request.is_active is not None:
        category_exist.is_active = request.is_active

    db.commit()
    db.refresh(category_exist)

    return category_exist


def delete_category(id, db):
    category_exist = db.query(Category).filter(Category.id == id).first()

    if not category_exist:
        raise HTTPException(status_code=400, detail="Category not found!")

    category_exist.is_active = False

    db.commit()
    return {"message": "Category deleted successfully!"}
