from prj import Module
import logging
logger = logging.getLogger()


class EntryModule(Module):
    xml_schema = """
<schema>
    <entry name="code_addr" type="int" default="0" />
    <entry name="data_addr" type="int" default="0x20000000" />
    <entry name="stack_size" type="int" default="0x1000" />
</schema>"""

    files = [
        {'input': 'default.ld', 'render': True, 'type': 'linker_script', 'stage': 'post_prepare'},
    ]

module = EntryModule()