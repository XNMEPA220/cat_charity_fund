from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


def completion_of_investment(
        obj: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    """Функция для закрытия проекта, после его полного инвестирования."""
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


def investment_process(
        sources: Union[List[CharityProject], List[Donation]],
        target: Union[CharityProject, Donation]
) -> Union[List[CharityProject], List[Donation]]:
    """Функция для проведения процесса инвестирования."""
    modified_sources = []
    for source in sources:
        exists_amount = source.full_amount - source.invested_amount
        new_item_amount = target.full_amount - target.invested_amount

        if exists_amount == new_item_amount:
            modified_sources.append(completion_of_investment(source))
            completion_of_investment(target)

        if exists_amount > new_item_amount:
            source.invested_amount += new_item_amount
            completion_of_investment(target)

        if exists_amount < new_item_amount:
            target.invested_amount += exists_amount
            modified_sources.append(completion_of_investment(source))

    return modified_sources
