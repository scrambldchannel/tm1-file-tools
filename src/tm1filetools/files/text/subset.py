from pathlib import Path
from typing import Optional

from .linecode import TM1LinecodeFile
from .user_owned import TM1UserFile


class TM1SubsetFile(TM1UserFile, TM1LinecodeFile):
    """
    A class representation of a tm1 subset file

    """

    suffix = "sub"
    folder_suffix = "}subs"

    def __init__(self, path: Path, public: bool = True):

        super().__init__(path)

        # these might all be better passed as parameters
        # as I'm not sure they can be derived from the
        # file contents
        self.dimension = self._get_object_name()
        self.public = public
        # this might be better passed as a parameter
        self.owner = self._get_owner_name()
        # subset_name maybe a clearer API than stem?
        self.subset_name = self.stem

    def is_dynamic(self) -> bool:

        return True if self._get_mdx() else False

    def _get_mdx(self) -> Optional[str]:
        """Read file and return the MDX, if file defines a dynamic subset, or None

        Returns:
            A string containing the MDX or None

        """

        # this is captured by key 275
        code = 275

        mdx_chars = self._get_int_val_by_code(code)

        if mdx_chars > 0:

            mdx_idx = self._get_index_by_code(code)

            # I believe it's all on one line, not sure
            return self._get_lines_by_index(index=mdx_idx + 1)[0]

        # does this code exist in a static file? Or is it just empty?
        return None

    def _get_name(self):

        code = 284

        return self._get_str_val_by_code(code)

    def _get_timestamp(self):

        code = 11

        # we should convert this to datetime or something
        return self._get_str_val_by_code(code)

    def _to_json(self):
        """Read file and return a json representation

        Returns:
            A dict containing a json representation of the subset

        """

        name = self._get_name()

        # this is a bit flawed but I haven't got an example of a
        # hierarchy aware subset to hand :shrug:
        hier_odata = self._create_odata_hier_string(dim=self.dimension)

        json_dump = {
            # these two fields always appear
            "Name": name,
            "Hierarchy@odata.bind": hier_odata,
        }

        # if the file contains an mdx expression, add it
        if self.is_dynamic():
            json_dump["Expression"] = self._get_mdx()
        else:
            json_dump["Elements@odata.bind"] = self._get_element_odata()

        return json_dump

    def get_elements(self):
        """
        Returns a list of the elements in a static subset

        Returns None if the subset is dynamic
        """

        if self.is_dynamic():
            return None
        else:
            # for static subsets, code 270 gives an int with the number of elements
            # then each element is listed on the lines below

            code = 270

            el_count = self._get_int_val_by_code(code)

            # index of first element line
            ix = self._get_index_by_code(code) + 1

            elements = self._get_lines_by_index(index=ix, line_count=el_count)

            return elements

    def _get_element_odata(self):

        elements = self.get_elements()

        odata_out = []

        for el in elements:

            odata = self._create_odata_element_string(dim=self.dimension, el=el)

            odata_out.append(odata)

        return odata_out

    @staticmethod
    def _create_odata_hier_string(dim: str, hier: str = None):

        # this is a fairly trivial function but may be useful more generally
        # perhaps it should be moved to a helper class?

        # derive "Hierarchy@odata.bind" string
        # Example - "Dimensions('}Processes')/Hierarchies('}Processes')"

        # use default hierarchy if none provided

        if hier is None:
            hier = dim

        return f"Dimensions('{dim}')/Hierarchies('{hier}')"

    @staticmethod
    def _create_odata_element_string(dim: str, el: str, hier: str = None):

        # perhaps it should be moved to a helper class?

        if hier is None:
            hier = dim

        return f"Dimensions('{dim}')/Hierarchies('{hier}')/Elements('{el}')"
