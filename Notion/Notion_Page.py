from typing import Union
from typing import List

class NotionRichTextObject:
    """
    Simple wrapper class for Notion's rich text object.

    Official documentation:
        https://developers.notion.com/reference/rich-text
    """

    def __init__(self, rich_text_object: dict):
        """
        Initializes Notion's rich text object attributes.

        Args:
            rich_text_object (dict): Dictionary with attributes.
                                    Comes from a NotionPageProperty's value attribute.
        """
        self.plain_text = rich_text_object["plain_text"]
        self.href = rich_text_object["href"]
        self.annotations = rich_text_object["annotations"]
        self.type = rich_text_object["type"]

    def get_plain_text(self) -> str:
        """
        Getter for the plain_text attribute.

        Returns:
            str: plain_text attribute.
        """
        return self.plain_text


class NotionPageProperty:
    """
    Wrapper for Notion Page's Property attribute.

    Official documentation:
        https://developers.notion.com/reference/page#property-value-object

    The property attribute in a Notion Page is the one that has all the
    custom information in the page.
    """

    def __init__(self, page_property: dict):
        """
        Initializes a Notion page property class given its dictionary.

        Args:
            page_property (dict): Dictionary with attributes.
                                  Comes from a Notion Page's property attribute.
        """
        self.value = page_property["value"]
        self.type = page_property["type"]
        self.id = page_property["id"]

    def get_value(self):
        """
        Getter for the value attribute.

        Returns:
            Union[str, NotionRichTextObject]: Value attribute.
        """
        if self.type == "rich_text":
            return NotionRichTextObject(self.value)
        else:
            return self.value


    def __init__(self, page_property: dict):
        """
        Initializes a Notion page property class given its dictionary.

        Args:
            page_property (dict): Dictionary with attributes.
                                  Comes from a Notion Page's property attribute.
        """
        self.id = page_property["id"]
        self.type = page_property["type"]
        self.value = page_property.get(self.type)

    def get_value(self) -> Union[str, list[str], None]:
        """
        Returns the page property's value either as a
        string or a list of strings.

        Returns:
            Union[str, list[str], None]: Page's property value.
        """

        if self.type == "checkbox":
            return self._get_checkbox_value()

        if not self.value:
            return None
        if self.type not in ["number"]:
            if len(self.value) == 0:
                return None

        type_to_function = {
            "title": self._get_title_value,
            "rich_text": self._get_rich_text_value,
            "relation": self._get_relation_value,
            "multi_select": self._get_multi_select_value,
            "phone_number": self._get_string_value,
            "rollup": self._get_rollup_value,
            "url": self._get_string_value,
            "date": self._get_string_value,
            "select": self._get_select_value,
            "email": self._get_string_value,
            "files": self._get_files_value,
            "number": self._get_number_value,
        }

        return type_to_function.get(self.type, self._default_value)()

    def _default_value(self) -> None:
        """Returns None for unsupported property types."""
        return None

    def _get_files_value(self) -> str:
        """Returns the value of a property of type files as a string."""
        return self.value[0]["name"]

    def _get_select_value(self) -> str:
        """Returns the value of a property of type select as a string."""
        return self.value["name"]

    # Add other helper methods for different property types here

    def _get_checkbox_value(self) -> bool:
        """Returns the value of a property of type checkbox as a boolean."""
        return self.value
    
    
    def get_value(self) -> Union[str, List[str], int, bool, None]:
        type_to_function = {
            "title": self._get_title_value,
            "rich_text": self._get_rich_text_value,
            "relation": self._get_relation_value,
            "multi_select": self._get_multi_select_value,
            "phone_number": self._get_string_value,
            "rollup": self._get_rollup_value,
            "url": self._get_string_value,
            "date": self._get_string_value,
            "select": self._get_select_value,
            "email": self._get_string_value,
            "files": self._get_files_value,
            "number": self._get_number_value,
            "checkbox": self._get_checkbox_value,
        }
        
        return type_to_function.get(self.type, self._default_value)()

    def _default_value(self) -> None:
        return None

    def _get_files_value(self) -> str:
        return self.value[0]["name"]

    def _get_select_value(self) -> str:
        return self.value["name"]

    def _get_rollup_value(self) -> str:
        property_type = self.value["type"]
        return self.value[property_type]

    def _get_number_value(self) -> int:
        return self.value

    def _get_checkbox_value(self) -> bool:
        return self.value

    def _get_string_value(self) -> str:
        return self.value

    def _get_multi_select_value(self) -> List[str]:
        return [selection["name"] for selection in self.value]

    def _get_relation_value(self) -> List[str]:
        return [relation["id"] for relation in self.value]

    def _get_rich_text_value(self) -> str:
        rich_text_object = NotionRichTextObject(self.value[0])
        return rich_text_object.get_plain_text()

    def _get_title_value(self) -> str:
        rich_text_object = NotionRichTextObject(self.value[0])
        return rich_text_object.get_plain_text()
    
    
    
    
    