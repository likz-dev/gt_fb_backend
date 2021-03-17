from datetime import datetime

from app.daos.base_dao import BaseDAO, SCHEMA_NAME

TABLE_NAME = 'booking'

FIELD_NAME = 'name'
FIELD_BOOKING_ID = 'booking_id'
FIELD_START_TIME = 'start_time'
FIELD_END_TIME = 'end_time'
FIELD_BOOKED_BY = 'booked_by'
FIELD_FACILITY_ID = 'facility_id'


def format_response(response):
    f_response = []
    for r in response:
        f_response.append({
            'bookingId': r.get(FIELD_BOOKING_ID),
            'facilityId': r.get(FIELD_FACILITY_ID),
            'text': r.get(FIELD_NAME),
            'start': r.get(FIELD_START_TIME).strftime("%Y/%m/%d %H:%M"),
            'end': r.get(FIELD_END_TIME).strftime("%Y/%m/%d %H:%M"),
            'bookedBy': r.get(FIELD_BOOKED_BY),
            'isMe': False
        })
    return f_response


class BookingDAO(BaseDAO):
    def insert_booking(self, booking):
        query = f'''
INSERT INTO {SCHEMA_NAME}.{TABLE_NAME} ({FIELD_START_TIME}, {FIELD_END_TIME}, {FIELD_BOOKED_BY}, {FIELD_FACILITY_ID}, {FIELD_NAME})
VALUES (%s, %s, %s, %s, %s)
RETURNING {FIELD_BOOKING_ID}
'''

        try:
            return self.db_helper.execute(query, params=(
                booking.start_time, booking.end_time, booking.booked_by, booking.facility_id, booking.name))
        except Exception as error:
            print(error)
            print(f'Error while executing query: {query}')
            return False

    def get_all_valid_bookings(self):
        date_today = datetime.date(datetime.now())
        query = f'''
SELECT * FROM {SCHEMA_NAME}.{TABLE_NAME}
WHERE {FIELD_START_TIME} > '{date_today}'
'''

        try:
            response = self.db_helper.execute(query)
            return format_response(response)
        except Exception as error:
            print(error)
            print(f'Error while executing query: {query}')
            return False

    def get_all_user_valid_bookings(self, booked_by):
        date_today = datetime.date(datetime.now())
        query = f'''
SELECT * FROM {SCHEMA_NAME}.{TABLE_NAME}
WHERE {FIELD_START_TIME} > '{date_today}'
AND {FIELD_BOOKED_BY} = %s
'''
        params = (booked_by, )

        try:
            response = self.db_helper.execute(query, params)
            return format_response(response)
        except Exception as error:
            print(error)
            print(f'Error while executing query: {query}')
            return False

    def delete_user_booking(self, booking_id):
        query = f'''
DELETE FROM {SCHEMA_NAME}.{TABLE_NAME}
WHERE {FIELD_BOOKING_ID} = %s
RETURNING *
'''
        params = (booking_id,)

        try:
            self.db_helper.execute(query, params)
            return True
        except Exception as error:
            print(error)
            print(f'Error while executing query: {query}')
            return False

    # def get_all_user_valid_booking(self):
# [
#         {
#           text: 'Mr.A reserved',
#           start: '2021/03/09 18:00',
#           end: '2021/03/09 20:00',
#           isMe: false
#         },
#     ]
# print(datetime.date(datetime.now()))
# helper = DBHelper()
# dao = BookingDAO(helper)
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# print(dao.insert_booking(Booking(None, 'booking', '2021/03/11 20:00', '2021/03/11 23:00', 'test', 1)))
# bookings = dao.delete_user_booking(38)
# print(bookings)
# bookings = list(filter(lambda b: b.facility_id == 1, bookings))
# for booking in bookings:
#     print(f'{booking.booking_id} {booking.start_time.strftime("%Y/%m/%d %H:%M")} {booking.facility_id}')
