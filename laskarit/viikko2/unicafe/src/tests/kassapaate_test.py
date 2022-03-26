import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):

    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_luotu_kassapaate_on_oikein_maara_rahaa(self):
        self.assertEqual(str(self.kassapaate.kassassa_rahaa), "100000")

    def test_luotu_kassapaate_lounaiden_maara_oikein(self):
        self.assertEqual(str(self.kassapaate.edulliset),"0")
        self.assertEqual(str(self.kassapaate.maukkaat),"0")

    def test_kateinen_maksu_kasvaa_kassasaldo_edullinen(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100240")
    
    def test_kateinen_maksu_kasvaa_kassasaldo_maukas(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100400")

    def test_kateinen_maksu_kasvaa_edulliset_maara(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(str(self.kassapaate.edulliset),"1")

    def test_kateinen_maksu_kasvaa_maukkaat_maara(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(str(self.kassapaate.maukkaat),"1")

    def test_kateinen_jos_ei_tarpeeksi_edullinen_kassapaate(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100000")
        
    def test_kateinen_jos_ei_tarpeeksi_maukkaan_kassapaate(self):
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100000")

    def test_kateinen_jos_ei_tarpeeeksi_edullinen_maksu_palautetaan(self):
        maksu=self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(str(maksu),"100")

    def test_kateinen_jos_ei_tarpeeeksi_maukkaan_maksu_palautetaan(self):
        maksu=self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(str(maksu),"100")  

    def test_kateinen_ei_tarpeeksi_edullinen_maara_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(str(self.kassapaate.edulliset),"0")
    
    def test_kateinen_ei_tarpeeksi_maukkaat_maara_ei_muutu(self):
        self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(str(self.kassapaate.maukkaat),"0")
        
    #Kortti

    def test_kortti_edullinen_palauttaa_True(self):
        boolean=self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(boolean),"True")

    def test_kortti_edullinen_palauttaa_False(self):
        self.kortti.saldo-=1000
        boolean=self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(boolean),"False")

    def test_kortti_maukkaan_palauttaa_True(self):
        boolean=self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(boolean),"True")

    def test_kortti_maukkaan_palauttaa_False(self):
        self.kortti.saldo-=1000
        boolean=self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(boolean),"False")
    
    def test_kortti_edullinen_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(self.kassapaate.edulliset),"1")

    def test_kortti_edullinen_ei_kasva_maara(self):
        self.kortti.saldo-=1000
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(self.kassapaate.edulliset),"0")

    def test_kortti_maukkaan_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(self.kassapaate.maukkaat),"1")

    def test_kortti_maukkaan_maara_ei_kasva(self):
        self.kortti.saldo-=1000
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(self.kassapaate.maukkaat),"0")
    


    def test_kortti_edullinen_kassamaara_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100000")

    def test_kortti_maukkaan_kassamaara_ei_muutu(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100000")

    def test_korttin_saldo_ei_muutu_jos_ei_tarpeksi_edullinen(self):
        self.kortti.saldo -=800
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(self.kortti.saldo),"200")

    def test_korttin_saldo_ei_muutu_jos_ei_tarpeksi_maukas(self):
        self.kortti.saldo -=800
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(self.kortti.saldo),"200")

    def test_korttin_saldo_muutu_ladattaessa_rahaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti,200)
        self.assertEqual(str(self.kortti.saldo),"1200")
    
    def test_kassan_rahasto_muutu_ladataessa_rahaa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti,200)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100200")

    def test_korttin_saldo_ei_muutu_ladattaessa_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti,-200)
        self.assertEqual(str(self.kortti.saldo),"1000")
    
    def test_kassan_rahasto_ei_muutu_ladataessa_negatiivinen_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti,-200)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa),"100000")
