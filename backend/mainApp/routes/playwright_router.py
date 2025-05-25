from flask import Flask, Blueprint, jsonify, request
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
from undetected_playwright import Tarnished
import time
from playwright_stealth import stealth_sync
import random
import threading
from database.db import db
from models.hodel_data_model import HotelData
import re
from sqlalchemy.exc import IntegrityError
import json
import datetime
from datetime import timedelta

playwrite_router = Blueprint("playwrite", __name__)


@playwrite_router.route("/web-scraping-playwright", methods=["POST"])
def web_scrap():
    try:
        city_name = request.args.get("city_name", type=str)
        if not city_name:
            return {"message": "city_name parameter not found"}

        user_agents = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
       
          
        ]

        user_agent = random.choice(user_agents)
        with sync_playwright() as p:
            browser = p.chromium.launch(
                args=["--disable-blink-features=AutomationControlled"],
                headless=False,
            )

            context = browser.new_context(user_agent=user_agent)

            page = context.new_page()
            stealth_sync(page)

            page.goto(
                "https://www.booking.com/searchresults.en-gb.html?ss=Chand%C4%ABgarh&ssne=Chand%C4%ABgarh&ssne_untouched=Chand%C4%ABgarh&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaGyIAQGYAQm4ARnIAQzYAQHoAQGIAgGoAgO4Asieu8EGwAIB0gIkNDFhOGY0MGMtZWZlMy00MTJjLWI3NDAtYWJkYWY3Y2YxOWVh2AIF4AIB&sid=2492faf1bab222b17b78f3501c459473&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-2092770&dest_type=city&checkin=2025-05-23&checkout=2025-05-24&group_adults=2&no_rooms=1&group_children=0",
                timeout=10000,
            )
            page.set_default_navigation_timeout(600_000)

            page.wait_for_selector('input[name="ss"]', timeout=50000, state="visible")
            ele = page.query_selector('input[name="ss"]')
            if ele:

                ele.fill(city_name)
                page.keyboard.press("Enter")
                page.wait_for_load_state(timeout=5000)
                prev_height = -1
                max_scroll = 10
                scroll_count = 0

                print(page.url)
                page.wait_for_selector('input[name="ss"]', timeout=50000)
                ele = page.query_selector('input[name="ss"]')
                if ele:

                    ele.fill(city_name)
                    page.wait_for_load_state(timeout=5000)

                try:
                    print(page.url)
                    page.wait_for_selector(
                        'button[data-testid="searchbox-dates-container"]', timeout=5000
                    )
                    container = page.query_selector(
                        'button[data-testid="searchbox-dates-container"]'
                    )

                    if container:
                        print("contianer")
                        # print(container.inner_html())
                        container.click()
                        nav = page.query_selector('nav[data-testid="datepicker-tabs"]')
                        print("nav", nav.inner_html())
                        try:
                            nav.wait_for_selector(
                                'span[data-date="2025-05-23"]', timeout=2000
                            )
                            btn = nav.query_selector('span[data-date="2025-05-23"]')
                            if btn:
                                print(btn.inner_text())
                                btn.click()
                                print("date button clicked")
                            btn = page.query_selector('button:has-text("Search")')
                            if btn:
                                print("btn clicked")
                                btn.click()
                        except:
                            print("no button ")

                except:
                    print("exception show prices no button ")
                page.wait_for_selector("body", timeout=10000)
                locator = page.locator("html")
                locator.wait_for(state="attached", timeout=5000)
                page.wait_for_load_state(timeout=5000)
                new_height = page.evaluate("document.body.scrollHeight")

                while scroll_count < max_scroll:
                    page.wait_for_load_state(timeout=5000)
                    if new_height == "":
                        new_height = page.evaluate("document.body.scrollHeight")

                    page.evaluate(f"window.scrollTo(0,document.body.scrollHeight)")
                    page.wait_for_timeout(2000)
                    new_height = page.evaluate(f"document.body.scrollHeight")
                    page.wait_for_load_state(timeout=5000)
                    try:

                        btn = page.query_selector(
                            'button:has-text("Load more results")'
                        )
                        if btn:
                            btn.click()
                    except:
                        print("Load more results no button ")

                    if new_height == prev_height:
                        break
                    prev_height = new_height
                    scroll_count += 1

                datestr = []
                start_date = datetime.datetime(2025, 5, 22)
                end_date = datetime.datetime(2025, 5, 23)
                for x in range((end_date - start_date).days + 1):
                    datestr.append(start_date + timedelta(days=x))

                availability_links = page.query_selector_all(
                    'a[data-testid="availability-cta-btn"]'
                )[:10]
                hoteldata = []

                for i, link in enumerate(availability_links, start=1):
                    try:
                        img_link_list = []
                        roomtype_list = []
                        conditions_list = []
                        facilities_list = []
                        availability_data_list = []

                        with context.expect_page() as page_info:
                            link.click(button="middle")
                        new_page = page_info.value
                        new_page.wait_for_load_state("load", timeout=15000)
                        new_page.wait_for_selector(
                            "#hprt-table", state="visible", timeout=10000
                        )
                        time.sleep(2)
                        title_el = new_page.query_selector(".pp-header__title")
                        if title_el:
                            hotel_name = title_el.inner_text().strip()
                        else:
                            print("hotel_name not found")
                        price_el = new_page.query_selector(".bui-price-display__value")
                        if price_el:
                            price = price_el.inner_text().strip()
                        else:
                            print("price not found")
                        desc_el = new_page.query_selector(
                            'p[data-testid="property-description"]'
                        )

                        if desc_el:
                            hotel_description = desc_el.inner_text()
                            hotel_description = re.sub(
                                r"\s*\n\s*", " ", hotel_description
                            ).strip()
                        else:
                            print("description not found")
                        date_list = []
                        for date in datestr:

                            date_string = date.strftime("%Y-%m-%d")
                            try:
                                btn = new_page.query_selector(".a444449f57")
                                if btn:
                                    btn.click()
                                    new_page.wait_for_timeout(1000)
                                    new_page.wait_for_selector(
                                        f'span[data-date="{date_string}"]', timeout=3000
                                    )
                                    date_btn = new_page.query_selector(
                                        f'span[data-date="{date_string}"]'
                                    )
                                    if date_btn:
                                        date_btn.scroll_into_view_if_needed()
                                        new_page.wait_for_timeout(500)
                                        date_btn.click(force=True)
                                    else:
                                        print("date_btn not found")
                                        continue
                                    search_btn = new_page.query_selector(
                                        'button:has-text("Apply changes")'
                                    )
                                    if search_btn:
                                        search_btn.click()
                                        new_page.wait_for_timeout(3000)
                                        tb_row = new_page.wait_for_selector(
                                            ".js-rt-block-row", timeout=5000
                                        )
                                        price__value = tb_row.query_selector(
                                            ".bui-price-display__value"
                                        )
                                        if price__value:
                                            price__value = price__value.inner_text()
                                            print(
                                                f"{i}:date:{date_string}:price :{price__value}"
                                            )
                                            date_list.append(
                                                {
                                                    "date": date_string,
                                                    "price": price__value,
                                                }
                                            )

                                        else:
                                            print("price__value not found")
                                    else:
                                        print("no search button")
                                else:
                                    print("btn not found")
                            except Exception as e:
                                print(f"error at date_btn {str(e)}")

                        table_row = new_page.query_selector(".js-rt-block-row")
                        conditions = table_row.query_selector(
                            ".hprt-table-cell-conditions"
                        )
                        if conditions:
                            conditions = conditions.inner_text()
                            conditions = re.sub(r"\s*\n\s*", " ", conditions).strip()

                        else:
                            print("conditions not found")

                        facilities_facilitys = table_row.query_selector_all(
                            ".hprt-facilities-facility"
                        )
                        for facilities_facility in facilities_facilitys:
                            if facilities_facility:
                                facilities_facility = facilities_facility.inner_text()
                                facilities_list.append(facilities_facility)

                            else:
                                print("facilities_facility not found")

                        table_rows = new_page.query_selector_all(".js-rt-block-row")
                        if table_rows:
                            for table_row in table_rows:
                                roomtype_bed = table_row.query_selector(
                                    ".bed-types-wrapper"
                                )
                                if roomtype_bed:
                                    roomtype_bed = roomtype_bed.inner_text()
                                else:
                                    print("roomtype_bed not found")

                                occupancy = table_row.query_selector(
                                    ".hprt-occupancy-occupancy-info"
                                )
                                if occupancy:
                                    occupancy = occupancy.inner_text()
                                else:
                                    print("occupancy not found")

                                price__value = table_row.query_selector(
                                    ".bui-price-display__value"
                                )
                                if price__value:
                                    price__value = price__value.inner_text()
                                else:
                                    print("price__value not found")

                                roomtype = table_row.query_selector(
                                    ".hprt-roomtype-link"
                                )
                                if roomtype:
                                    roomtype = roomtype.inner_text()
                                    print(f"{i}:roomtype=>{roomtype}")
                                    roomtype_list.append(
                                        {
                                            "roomtype": roomtype,
                                            "roomtype_bed": roomtype_bed,
                                            "number_of_guests": occupancy,
                                            "price__value": price__value,
                                        }
                                    )
                                else:
                                    print("roomtype not found")

                                conditions_list.append(conditions)
                            availability_data_list.append(
                                {
                                    "roomtype": roomtype_list,
                                    "facilities": facilities_list,
                                    "conditions": conditions,
                                }
                            )
                        else:
                            print("table_row not found")

                        try:
                            btn = new_page.query_selector(".aa225776f2")
                            if btn:
                                btn.click()
                                time.sleep(1)
                                new_page.wait_for_selector(
                                    'div[data-component="bh-photo-modal"]', timeout=1000
                                )
                                link_ele = new_page.query_selector(
                                    'div[data-component="bh-photo-modal"]'
                                )
                                if link_ele:
                                    links = link_ele.query_selector_all(
                                        ".bh-photo-modal-grid-image"
                                    )
                                    for link in links:
                                        img_link = link.get_attribute("data-src")
                                        img_link_list.append(img_link)

                            hoteldata.append(
                                {
                                    "id": i,
                                    "city_name":city_name,
                                    "hotel_name": hotel_name,
                                    "date": date_list,
                                    "price": price,
                                    "hotel_description": hotel_description,
                                    "img_link": img_link_list,
                                    "availability_data": availability_data_list,
                                }
                            )

                        except:
                            print("no button ")

                        hotel_data = HotelData(
                            hotel_name=hotel_name,
                            city_name = city_name,
                            price=price,
                            hotel_description=hotel_description,
                            img_link=img_link_list,
                            availability=availability_data_list,
                            dates=date_list,
                        )
                        existing_hotel = HotelData.query.filter_by(
                            hotel_name=hotel_name
                        ).first()
                        if existing_hotel:
                            print("message : hotel already exist...")
                        try:
                            db.session.add(hotel_data)
                            db.session.commit()
                        except IntegrityError as e:
                            db.session.rollback()
                            print(f"error to save data {str(e)}")
                        new_page.close()

                    except Exception as e:
                        print(f"Error at hotel {i}: {e}")
            browser.close()
        try:
            with open("hoteldata.json", "w", encoding="utf-8") as f:
                json.dump(hoteldata, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"error to save json file {str(e)}")

        return {
            "message": " sucessfully scraping data",
            "hotel_data": hoteldata,
        }
    except Exception as e:
        print(f"Error at web_scrap{e}")
        return {"message": str(e)}


@playwrite_router.route("/web-scraping-playwright", methods=["GET"])
def web_scraping():
    try:
        thread = threading.Thread(target=web_scrap)
        thread.start()
        return jsonify({"message": "Scraping started in background thread"})
    except Exception as e:
        print(f"Error at web_scrap: {e}")
        return jsonify({"message": str(e)})
