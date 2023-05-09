"""Постоянные для API проекта."""

MODEL_EXCLUDE_FIELDS = (
    'user_id',
    'invested_amount',
    'fully_invested',
    'close_date'
)

ERROR_MESSAGES = {
    "not_found": "Проект не найден!",
    "name_dublicate": "Проект с таким именем уже существует!",
    "project_was_closed": "Закрытый проект нельзя редактировать!",
    "project_was_invested": "В проект были внесены средства, не подлежит удалению!",
    "incorrect_required_summ": "Новая требуемая сумма должна быть больше уже внесенной!",
}
