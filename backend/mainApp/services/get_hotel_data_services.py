from models.hodel_data_model import HotelData

def get_hotel_data_services(page):
    try:
        hote_data =[]
        hotels_details = HotelData.query.paginate(page=page,per_page=5)
        for hotel_detals in hotels_details:
            hote_data.append({
                "id": hotel_detals.id,
                "city_name": hotel_detals.city_name,
                "hotel_name": hotel_detals.hotel_name,
                "price": hotel_detals.price,
                "dates": hotel_detals.dates,
                "hotel_description": hotel_detals.hotel_description,
                "img_link": hotel_detals.img_link,
                "availability": hotel_detals.availability,
            })
        return {"hotel":hote_data}
    except Exception as e:
        print(f"Error at get_hotel_data_services {str(e)} ")
