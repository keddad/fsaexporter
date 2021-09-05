from datetime import datetime
from enum import Enum

import fsaexporter.utils as utils


class DeclarationStatus(Enum):
    Archive = 1
    Annulled = 2  # Аннулирован
    Reactivated = 3  # Возобновлен
    Issued = 4  # Выдан
    OrderIssued = 5  # Выдано предписание
    Active = 6
    RemovedFromRegistry = 7  # Исключен из реестра
    Used = 8  # Использован
    Invalid = 9  # Испорчен (Утрачен)
    IssuedDeactivationInfo = 10  # Направлено уведомление заявителю о прекращении декларации
    NotActive = 11  # Недействителен
    New = 12
    Sent = 13
    Stopped = 14  # Прекращен
    Paused = 15  # Приостановлен
    Prolonged = 16
    ReissueRequired = 17  # Сведения изменены, требуется отправка
    Removed = 18  # Удален
    PartiallyPaused = 19  # Частично приостановлен
    Draft = 20
    Canceled = 21


class Declaration:
    def __init__(self, declaration_id: int, dec_name: str, status: DeclarationStatus, reg_date: datetime,
                 end_date: datetime):
        self.declaration_id = declaration_id
        self.dec_name = dec_name
        self.status = status
        self.reg_date = reg_date
        self.end_date = end_date

    @classmethod
    async def init(cls, page_id: int, session: utils.FsaDownloader):
        data = (await session.get(f"https://pub.fsa.gov.ru/api/v1/rds/common/declarations/{page_id}", {}))

        d = Declaration(
            declaration_id=int(data["idDeclaration"]),
            dec_name=data["number"],
            status=DeclarationStatus(data["idStatus"]),
            reg_date=utils.fsa_to_datetime(data["declRegDate"]),
            end_date=utils.fsa_to_datetime(data["declEndDate"])
        )

        return d
