'''Создаём модель для валидации имени файла '''


from pydantic import BaseModel, constr

class FileInputModel(BaseModel):
    filename: constr(min_length=1, max_length=255, pattern = r"^[^<>:;,?\"*|/\\]+$")  # Имя файла без запрещённых символов







