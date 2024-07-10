from fastapi import Depends, HTTPException
from typing import List
import contextlib
from sqlalchemy.future import select
from database.database import engine, Base, get_async_session
import schemas
import models
from fastapi import APIRouter

router = APIRouter()


@contextlib.asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


@router.post(path='/login/')
def auth_user(db=Depends(get_async_session)):
    return {"message": "login"}


@router.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get(path='/recipes', response_model=List[schemas.RecipesOut],
#          summary="Получить список рецептов",
#          description="Возвращает список всех рецептов, отсортированных по популярности (количеству просмотров) "
#                      "и времени приготовления."
#          )
# async def recipes(db=Depends(get_async_session)) -> List[models.Recipes] | models.Recipe:
#     """
#     Функция гет запроса, которая возвращает список рецептов
#     """
#
#     result = await db.execute(select(models.Recipes).order_by(models.Recipes.views.desc(),
#                                                                    models.Recipes.cooking_time.asc()))
#
#     return result.scalars().all()
#
#
# @app.get(path='/recipes/{recipe_id}', response_model=schemas.RecipeOut,
#          summary="Получить рецепт по ID",
#          description="Возвращает информацию о рецепте по его ID."
#          )
# async def recipes(recipe_id: int, db=Depends(get_async_session)) -> models.Recipe:
#     """
#     Функция гет запроса, которая возвращает рецепт по id
#     """
#
#     recipes = await db.get(models.Recipes, recipe_id)
#     if recipes is None:
#         raise HTTPException(status_code=404, detail='Recipe not found')
#
#     else:
#         # up_views = recipe.one()
#         recipes.views += 1
#         return recipes.recipe
#
#
#
# @app.post(path='/recipes', response_model=schemas.RecipeOut,
#           summary="Добавить рецепт",
#           description="Добавляет рецепт и возвращает добавленный рецепт при успешном запросе"
#           )
# async def recipes(recipe: schemas.RecipeIn, db=Depends(get_async_session)) -> models.Recipe:
#     """
#     Функция пост запроса, добавляет рецепт
#     """
#
#     new_recipe = models.Recipe(**recipe.dict())
#
#     db.add(new_recipe)
#     await db.flush()
#
#     new_recipes = models.Recipes(
#         name=new_recipe.name,
#         cooking_time=new_recipe.cooking_time,
#         recipe_id=new_recipe.id
#     )
#     db.add(new_recipes)
#     await db.commit()
#     return new_recipe
