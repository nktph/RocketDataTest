import json
import requests
from bs4 import BeautifulSoup

html = requests.get("https://dentalia.com/").text
soup = BeautifulSoup(html, 'html.parser')
links = soup.find_all("section",
                      class_="elementor-section elementor-inner-section elementor-element elementor-element-01a0b47 "
                             "LinkToClinic elementor-section-boxed elementor-section-height-default "
                             "elementor-section-height-default")
clinics = []
for link in links:
    tax_query_estados = link.attrs['id'].split("estados:")[1]
    link = f"{link.attrs['id']}&nocache=1690594168&action=jet_engine_ajax&handler=get_listing&page_settings%5Bpost_id" \
           f"%5D=5883&page_settings%5Bqueried_id%5D=344706%7CWP_Post&page_settings%5Belement_id%5D=c1b6043" \
           f"&page_settings%5Bpage%5D=1&listing_type=elementor&isEditMode=false "
    clinics_html = requests.post(link).json()['data']['html']
    soup = BeautifulSoup(clinics_html, 'html.parser')

    data = soup.find_all('div', class_='jet-listing-dynamic-field__content')

    latlons = requests.post(f"https://dentalia.com/wp-admin/admin-ajax.php?"
                            f"action=jet_smart_filters&provider=jet-engine-maps%2Fmap&query%5B_tax_query_estados"
                            f"%5D={tax_query_estados}&defaults%5Bpost_status%5D=publish&defaults%5Bpost_type%5D"
                            f"=clinicas&defaults%5Bposts_per_page%5D=100&defaults%5Bpaged%5D=1&defaults"
                            f"%5Bignore_sticky_posts%5D=1&settings%5Blisitng_id%5D=6640&settings%5Baddress_field"
                            f"%5D=direccion&settings%5Badd_lat_lng%5D=&settings%5Blat_lng_address_field%5D"
                            f"=&settings%5Bposts_num%5D=100&settings%5Bauto_center%5D=yes&settings%5Bmax_zoom%5D"
                            f"=15&settings%5Bcustom_center%5D=&settings%5Bcustom_zoom%5D=11&settings"
                            f"%5Bzoom_control%5D=auto&settings%5Bzoom_controls%5D=true&settings"
                            f"%5Bfullscreen_control%5D=true&settings%5Bstreet_view_controls%5D=true&settings"
                            f"%5Bmap_type_controls%5D=&settings%5Bposts_query%5D%5B0%5D%5B_id%5D=593cb36"
                            f"&settings%5Bposts_query%5D%5B0%5D%5Btax_query_taxonomy%5D=estados&settings"
                            f"%5Bposts_query%5D%5B0%5D%5Btax_query_terms%5D=%25current_terms%7Cestados%25%7B"
                            f"%22context%22%3A%22default_object%22%7D&settings%5Bmeta_query_relation%5D=AND"
                            f"&settings%5Btax_query_relation%5D=AND&settings%5Bhide_widget_if%5D=&settings"
                            f"%5Bpopup_width%5D=450&settings%5Bpopup_offset%5D=40&settings%5Bmarker_type%5D=icon"
                            f"&settings%5Bmarker_image%5D%5Burl%5D=&settings%5Bmarker_image%5D%5Bid%5D=&settings"
                            f"%5Bmarker_image%5D%5Bsize%5D=&settings%5Bmarker_icon%5D%5Bvalue%5D=fas+fa-map"
                            f"-marker-alt&settings%5Bmarker_icon%5D%5Blibrary%5D=fa-solid&settings"
                            f"%5Bmarker_label_type%5D=post_title&settings%5Bmarker_label_field%5D=&settings"
                            f"%5Bmarker_label_field_custom%5D=&settings%5Bmarker_label_text%5D=&settings"
                            f"%5Bmarker_label_format_cb%5D=0&settings%5Bmarker_label_custom%5D=&settings"
                            f"%5Bmarker_label_custom_output%5D=%25s&settings%5Bmarker_image_field%5D=&settings"
                            f"%5Bmarker_image_field_custom%5D=&settings%5Bmultiple_marker_types%5D=&settings"
                            f"%5Bmarker_clustering%5D=true&settings%5Bpopup_pin%5D=&settings%5Bpopup_preloader"
                            f"%5D=&settings%5Bcustom_query%5D=&settings%5Bcustom_query_id%5D=10&settings"
                            f"%5Blabels_by_glossary%5D=&settings%5Bdate_format%5D=F+j%2C+Y&settings"
                            f"%5Bnum_dec_point%5D=.&settings%5Bnum_thousands_sep%5D=%2C&settings"
                            f"%5Bhuman_time_diff_from_key%5D=&settings%5Bnum_decimals%5D=2&settings"
                            f"%5Bzeroise_threshold%5D=3&settings%5Bproportion_divisor%5D=10&settings"
                            f"%5Bproportion_multiplier%5D=5&settings%5Bproportion_precision%5D=0&settings"
                            f"%5Bchild_path%5D=&settings%5Battachment_image_size%5D=full&settings"
                            f"%5Bthumbnail_add_permalink%5D=&settings%5Brelated_list_is_single%5D=&settings"
                            f"%5Brelated_list_is_linked%5D=yes&settings%5Brelated_list_tag%5D=ul&settings"
                            f"%5Bmultiselect_delimiter%5D=%2C+&settings%5Bswitcher_true%5D=&settings"
                            f"%5Bswitcher_false%5D=&settings%5Burl_scheme%5D=&settings%5Bchecklist_cols_num%5D=1"
                            f"&settings%5Bchecklist_divider%5D=&settings%5Buser_data_to_get%5D=display_name"
                            f"&props%5Bfound_posts%5D=65&props%5Bmax_num_pages%5D=1&props%5Bpage%5D=1").json()["markers"]

    i = 0
    while i in range(len(data)):
        clinic_data = {"name": "dentalia Altaria",
                       "address": data[i].text,
                       "latlon": [float(latlons[int(i / 3)]['latLang']['lat']),
                                  float(latlons[int(i / 3)]['latLang']['lng'])],
                       "phones": data[i + 1].text.split("Teléfono(s):")[1].replace(" ", "").split('\r\n'),
                       "working_hours": data[i + 2].text.strip().replace("Horario: ", "").split('\r\n')
                       }

        clinics.append(clinic_data)
        i += 3

clinics_json = json.dumps(clinics)
with open(f"clinics.json", 'w', encoding="utf-8") as f:
    f.write(clinics_json)
