import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 10.0")
    
    def test_kortille_voi_ladata_rahaa(self):
        self.maksukortti.lataa_rahaa(2500)
        self.assertEqual(str(self.maksukortti), "saldo: 35.0")

    def test_saldo_vahenee_jos_tarpeeks(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(str(self.maksukortti), "saldo: 5.0")

    def test_saldo_ei_vahenee_jos_ei_tarpeeks(self):
        self.maksukortti.ota_rahaa(2000)
        self.assertEqual(str(self.maksukortti), "saldo: 10.0")

    def test_metodi_palauttaa_True(self):
        boolean=self.maksukortti.ota_rahaa(500)
        self.assertEqual(str(boolean), "True")

    def test_metodi_paluttaa_False(self):
        boolean=self.maksukortti.ota_rahaa(5000)
        self.assertEqual(str(boolean), "False")
        