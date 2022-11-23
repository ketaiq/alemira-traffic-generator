from app.utils.string import gen_random_description, gen_random_id, gen_random_title
from app.utils.time import get_current_timestamp
import xml.etree.ElementTree as ET
import random


def gen_random_content_dict() -> dict:
    content_dict = {
        "time": get_current_timestamp(),
        "blocks": [],
        "version": "2.23.2",
    }
    num_blocks = random.randrange(10, 50)
    for _ in range(num_blocks):
        block_type = random.choice(["paragraph", "header", "list"])
        if block_type == "paragraph":
            data = {
                "text": gen_random_description(),
                "alignment": random.choice(["left", "center", "right"]),
            }
        elif block_type == "header":
            data = {"text": gen_random_title(), "level": random.randrange(1, 4)}
        elif block_type == "list":
            num_items = random.randrange(3, 10)
            data = {
                "style": random.choice(["unordered", "ordered"]),
                "items": [gen_random_title() for _ in range(num_items)],
            }
        block = {
            "id": gen_random_id(10),
            "type": block_type,
            "data": data,
        }
        content_dict["blocks"].append(block)
    return content_dict


def gen_html_from_content_dict(content_dict: dict) -> str:
    """Parse about content to html str."""
    html_content = ""
    for block in content_dict["blocks"]:
        data = block["data"]
        if block["type"] == "paragraph":
            element = _gen_paragraph_element(data)
        elif block["type"] == "header":
            element = _gen_header_element(data)
        elif block["type"] == "list":
            element = _gen_list_element(data)
        elif block["type"] == "image":
            element = _gen_image_element(data)
        elif block["type"] == "attaches":
            element = _gen_attach_element(data)
        html_content += element
    return html_content


def _gen_paragraph_element(data: dict) -> str:
    alignment = data["alignment"]
    element = ET.Element("p", attrib={"class": f"paragraph {alignment}"})
    element.text = data["text"]
    return ET.tostring(element, encoding="unicode")


def _gen_header_element(data: dict) -> str:
    level = data["level"]
    element = ET.Element(f"h{level}", attrib={"class": "heading"})
    element.text = data["text"]
    return ET.tostring(element, encoding="unicode")


def _gen_list_element(data: dict) -> str:
    style = data["style"]
    element = ET.Element(
        "ul" if style == "unordered" else "ol", attrib={"class": "list"}
    )
    for item in data["items"]:
        item_ele = ET.Element("li", attrib={"class": "list-item"})
        item_ele.text = item
        element.append(item_ele)
    return ET.tostring(element, encoding="unicode")


def _gen_image_element(data: dict) -> str:
    url = data["file"]["url"]
    element = ET.Element("figure", attrib={"class": "image"})
    div_element = ET.Element("div", attrib={"class": "cover"})
    ET.SubElement(
        div_element,
        "img",
        attrib={"src": url, "alt": "", "class": "file"},
    )
    element.append(div_element)
    return ET.tostring(element, encoding="unicode")


def _gen_attach_element(data: dict) -> str:
    url = data["file"]["url"]
    filename = data["file"]["name"]
    extension = data["file"]["extension"]
    element = ET.Element("div", attrib={"class": "attach__container"})
    a_element = ET.SubElement(element, "a", attrib={"href": url, "class": "attach"})
    svg_element = ET.SubElement(
        a_element,
        "svg",
        attrib={
            "xmlns": "http://www.w3.org/2000/svg",
            "width": "16",
            "height": "16",
            "fill": "none",
            "class": "attach__icon",
        },
    )
    g_element = ET.SubElement(svg_element, "g")
    path_element = ET.Element(
        "path",
        attrib={
            "fill": "#727272",
            "d": "m13.18539,8.36698l-4.51872,4.51869l0,-12.32335l-1.33333,0l0,12.32335l-4.51867,-4.51869l-0.94266,0.94267l6.128,6.12802l6.12798,-6.12802l-0.9426,-0.94267z",
        },
    )
    g_element.append(path_element)
    div_element_1 = ET.SubElement(a_element, "div", attrib={"class": "attach__info"})
    div_element_2 = ET.SubElement(
        div_element_1,
        "div",
        attrib={"class": "attach__name"},
    )
    div_element_2.text = filename
    div_element_3 = ET.SubElement(
        div_element_1, "div", attrib={"class": "attach__extension"}
    )
    div_element_3.text = extension
    return ET.tostring(element, encoding="unicode", short_empty_elements=False)
