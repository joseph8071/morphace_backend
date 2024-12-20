from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.products import SkincareProducts, SkincareIngredients
from app.schemas.products import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductResponse)
def create_or_update_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    # Check if product exists
    product = db.query(SkincareProducts).filter(SkincareProducts.identifier == product_data.identifier).first()
    if not product:
        product = SkincareProducts(
            identifier=product_data.identifier,
            brand=product_data.brand,
            name=product_data.name,
            type=product_data.type
        )
        db.add(product)
        db.flush()  # Get product.id

        # Add ingredients
        if product_data.ingredients:
            for ing in product_data.ingredients:
                db.add(SkincareIngredients(product_id=product.id, ingredient=ing))
        db.commit()
    else:
        # Update existing product fields if provided
        if product_data.brand is not None: product.brand = product_data.brand
        if product_data.name is not None: product.name = product_data.name
        if product_data.type is not None: product.type = product_data.type
        db.query(SkincareIngredients).filter(SkincareIngredients.product_id == product.id).delete()
        if product_data.ingredients:
            for ing in product_data.ingredients:
                db.add(SkincareIngredients(product_id=product.id, ingredient=ing))
        db.commit()
        db.refresh(product)

    # Return product details including ingredients
    ingredients = db.query(SkincareIngredients).filter_by(product_id=product.id).all()
    ing_list = [i.ingredient for i in ingredients]

    return ProductResponse(
        id=product.id,
        identifier=product.identifier,
        brand=product.brand,
        name=product.name,
        type=product.type,
        ingredients=ing_list
    )

@router.get("/{identifier}", response_model=ProductResponse)
def get_product(identifier: str, db: Session = Depends(get_db)):
    product = db.query(SkincareProducts).filter(SkincareProducts.identifier == identifier).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    ingredients = db.query(SkincareIngredients).filter_by(product_id=product.id).all()
    ing_list = [i.ingredient for i in ingredients]
    return ProductResponse(
        id=product.id,
        identifier=product.identifier,
        brand=product.brand,
        name=product.name,
        type=product.type,
        ingredients=ing_list
    )
