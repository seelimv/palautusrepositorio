import unittest
from unittest.mock import Mock

from kauppa import Kauppa
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        # common mocks used by tests
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()
        self.saldo_map = {1: 10, 2: 5, 3: 0}
        self.tuote_map = {
            1: Tuote(1, "maito", 5),
            2: Tuote(2, "testi", 10),
            3: Tuote(2, "testi", 10),
        }

        def varasto_saldo(tuote_id):
            return self.saldo_map.get(tuote_id, 0)

        def varasto_hae_tuote(tuote_id):
            return self.tuote_map.get(tuote_id)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)


    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):

        kauppa = self.kauppa

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()


    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_oikeilla_argumenteilla(self):

        kauppa = self.kauppa

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", kauppa._kaupan_tili, 5)

    def test_maksettaessa_useampi_ostos_pankin_metodia_tilisiirto_kutsutaan_oikeilla_argumenteilla(self):

        kauppa = self.kauppa

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", kauppa._kaupan_tili, 15)

    def test_maksettaessa_kaksi_samaa_varastossa_olevaa_tuotetta_pankin_metodia_tilisiirto_kutsutaan_okeilla_argumenteilla(self):

        kauppa = self.kauppa

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", kauppa._kaupan_tili, 10)

    def test_maksettaessa_kaksi_eri_ostosta_joista_toinen_loppu_pankin_tilisiirtoa_metodia_kutsutaan_oikeilla_argumenteilla(self):

        self.saldo_map[2] = 0

        kauppa = self.kauppa

        kauppa.aloita_asiointi()

        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", kauppa._kaupan_tili, 5)

    def test_aloita_asiointi_metodin_kutsu_nollaa_edellisen_ostoksen_tiedot(self):
        kauppa = self.kauppa

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("testi", "01234")

        assert self.pankki_mock.tilisiirto.call_args_list[1][0][4] == 5

    def test_kauppa_pyytaa_uuden_viitenumeron_jokaiselle_tapahtumalle(self):
        kauppa = self.kauppa

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("testi", "12345")

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "01234")

        assert self.viitegeneraattori_mock.uusi.call_count == 2

    def test_tuotteen_poistaminen_korista_vähentää_tilimaksun_summaa(self):
        kauppa = self.kauppa

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.poista_korista(1)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", kauppa._kaupan_tili, 10)

    def test_lisää_koriin_loppunut_tuote(self):
        kauppa = self.kauppa

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(3)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", kauppa._kaupan_tili, 5)
