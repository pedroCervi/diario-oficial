from .base_parser import BaseParser


class GoGoiania(BaseParser):

    def pages(self):
        return self.text.split('DOM Eletrônico')[1:]

    def bidding_exemption_sections(self):
        for section in self.pages():
            text = section.lower()
            if ('ato de dispensa de licitação' in text) or (
                'termo de dispensa de licitação' in text
            ):
                yield section

    def bidding_exemptions(self):
        for section in self.bidding_exemption_sections():
            yield {'data': self.bidding_exemption(section), 'source_text': section}

    def bidding_exemption(self, section):
        return {}
