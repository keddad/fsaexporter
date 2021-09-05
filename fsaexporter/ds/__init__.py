import fsaexporter.utils as utils
from fsaexporter.ds.page import DeclarationPage

BASE_DECLARATION_PAYLOAD = {"size": 100, "page": 0,
                            "filter": {"status": [], "idDeclType": [], "idCertObjectType": [], "idProductType": [],
                                       "idGroupRU": [], "idGroupEEU": [], "idTechReg": [], "idApplicantType": [],
                                       "regDate": {"minDate": None, "maxDate": None},
                                       "endDate": {"minDate": None, "maxDate": None}, "columnsSearch": [
                                    {"name": "number", "search": "", "type": 0, "translated": False}],
                                       "idProductOrigin": [], "idProductEEU": [], "idProductRU": [], "idDeclScheme": [],
                                       "awaitForApprove": None, "awaitOperatorCheck": None, "editApp": None,
                                       "violationSendDate": None},
                            "columnsSort": [{"column": "declDate", "sort": "DESC"}]}


class DeclarationDownloader:

    def __init__(self, dec_name="", reg_min_date=None, reg_max_date=None, end_min_date=None, end_max_date=None):
        """

        :param dec_name: Номер декларации о соответствии
        :param reg_min_date: Минимаьлная дата регистрации декларации
        :param reg_max_date: Максимальная дата регистрации декларации
        :param end_min_date: Минимальная дата окончания действия декларации
        :param end_max_date: Максимальная дата окончания действия декларации
        """
        self.client = utils.FsaDownloader()

        self.payload = BASE_DECLARATION_PAYLOAD.copy()

        self.payload["filter"]["columnsSearch"][0]["search"] = dec_name
        self.payload["filter"]["regDate"]["minDate"] = utils.datetime_to_fsa(reg_min_date)
        self.payload["filter"]["regDate"]["maxDate"] = utils.datetime_to_fsa(reg_max_date)
        self.payload["filter"]["endDate"]["minDate"] = utils.datetime_to_fsa(end_min_date)
        self.payload["filter"]["endDate"]["minDate"] = utils.datetime_to_fsa(end_max_date)

        self.current_page = 0
        self.current_declaration = 0
        self.next_page = DeclarationPage.init(self.payload, self.current_page, self.client)
        self.p = None

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.p is None:
            self.p: DeclarationPage = await self.next_page
            self.next_page = DeclarationPage.init(self.payload, self.current_page, self.client)

        if self.p.empty():
            raise StopAsyncIteration

        if self.current_declaration >= len(self.p.declarations):
            self.p: DeclarationPage = await self.next_page
            self.current_page += 1
            self.current_declaration = 0
            self.next_page = DeclarationPage.init(self.payload, self.current_page, self.client)

        self.current_declaration += 1
        return self.p.declarations[self.current_declaration - 1]
