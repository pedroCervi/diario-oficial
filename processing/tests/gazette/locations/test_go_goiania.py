from unittest import TestCase, skip

from gazette.locations.go_goiania import GoGoiania


class TestGoGoiania(TestCase):

    def setUp(self):
        path = 'tests/gazette/fixtures/go_goiania.txt'
        with open(path) as file:
            self.text = file.read()
        self.subject = GoGoiania(self.text)

    def test_pages(self):
        pages = self.subject.pages()
        self.assertEqual(241, len(pages))
        expected_expressions = (
            'Criado pela Lei nº 1.552, de 21/08/1959',
            'Versão digital instituída pelo Decreto nº 3.987, de 14/08/2013',
            'Esta versão está assinada digitalmente, conforme MP nº 2.200-2',
            'E-mail contato: diariooficial@casacivil.goiania.go.gov.br',
            'PILOTO:88708985120'
        )
        for expected in expected_expressions:
            self.assertIn(expected, pages[0])

    @skip('fix pages test first')  # TODO
    def test_bidding_exemptions(self):
        exemptions = self.subject.bidding_exemptions()
        expectation = [
            {
                'data': {
                    'CONTRATANTE': 'Fundo Municipal da Guarda Civil Metropolitana - FMGCM',
                    'CONTRATADO': 'SOLUTI – SOLUÇÕES EM NEGÓCIOS INTELIGENTES S/A',
                    'OBJETO': 'Certificado Digital PJ1',
                    'VALOR': 'R$ 210,00 (duzentos e dez reais)',
                    'DOTAÇÃO ORÇAMENTÁRIA': '',
                    'BASE LEGAL': 'inciso II do artigo 24 da Lei no 8.666 de 1993',
                },
                'source_text': """Agência da Guarda Civil Metropolitana de Goiânia




         Processo: 388/2018
         Interessado: AGCMG
         Assunto: Dispensa de Licitação




                               ATO DE DISPENSA DE LICITAÇÃO Nº 001/2018/AGCMG


                                À vista do contido nos autos, nos termos do inciso II do artigo 24 da Lei nº
         8.666 de 1993, autorizo a contratação direta para a aquisição de Certificado Digital PJ1, para
         atender o Fundo Municipal da Guarda Civil Metropolitana - FMGCM, no valor de R$ 210,00
         (duzentos e dez reais), devendo ser pagos à empresa SOLUTI – SOLUÇÕES EM NEGÓCIOS
         INTELIGENTES S/A, conforme Parecer nº 0123/2018 – CHEADV/AGCMG.
                                Publique-se.




                                GABINETE DO PRESIDENTE COMANDANTE DA AGÊNCIA DA
         GUARDA CIVIL METROPOLITANA DE GOIÂNIA, aos 07 dias do mês de março de 2018.




                                                    JOSÉ EULÁLIO VIEIRA
                                                Presidente-Comandante da AGCMG"""
            },
        ]
        self.assertEqual(expectation, exemptions[0])
