from tasks.supplier_statics import update_hotelbeds, update_roomsxml, update_bonotel, update_hotelspro


class Test_supplier_statics(object):

    def test_update_hotelbeds(self):
        update_hotelbeds.delay()

    def test_update_roomsxml(self):
        update_roomsxml.delay()

    def test_update_bonotel(self):
        update_bonotel.delay()

    def test_update_hotelspro(self):
        update_hotelspro.delay()
