"""Pre-filled the "cherrytree" output file with the results of the nmap scans"""


def cherry_table(file_ctd, port_serv, versions):
    """Write a table inside a cherrytree file"""
    file_ctd.write(
        """\n		<rich_text justification="left"></rich_text>
		<table char_offset="198" col_max="250" col_min="40">""")
    for i, (port, serv) in enumerate(port_serv.items()):
        if serv == '':
            serv = 'Not found...'
        file_ctd.write(
            """\n			<row>
				<cell>""" + port + """</cell>
				<cell>""" + serv + """</cell>
				<cell>""" + versions[i] + """</cell>
			</row>""")
    file_ctd.write(
        """\n			<row>
				<cell>Port</cell>
				<cell>Protocol</cell>
				<cell>Version</cell>
			</row>
		</table>""")


def cherry_header(file_ctd, target, op_sys):
    """Write a cherrytree header (xml format)"""
    file_ctd.write(
"""<?xml version="1.0" ?>
<cherrytree>
	<node custom_icon_id="14" foreground="" is_bold="True" name="SweetDreams" prog_lang="custom-colors" readonly="False" tags="" ts_creation="0.0" ts_lastsave="0.0" unique_id="1">
		<rich_text>	</rich_text>
		<rich_text family="monospace">.-. . . . .-. .-. .-. .-. .-. .-. .-. .  . .-.</rich_text>
		<rich_text>\n	</rich_text>
		<rich_text family="monospace">`-. | | | |-  |-   |  |  )|(  |-  |-| |\/| `-.</rich_text>
		<rich_text>\n	</rich_text>
		<rich_text family="monospace">`-' `.'.' `-' `-'  '  `-' ' ' `-' ` ' '  ` `-'</rich_text>
		<rich_text>\n\n</rich_text>
		<rich_text weight="heavy">Target:</rich_text>
		<rich_text> 127.0.0.1\n</rich_text>
		<rich_text weight="heavy">OS:</rich_text>
		<rich_text> Test in progress...\n</rich_text>
		<rich_text weight="heavy">Services:</rich_text>
		<rich_text>\n\n</rich_text>""")


def cherry_tail(file_ctd):
    """Write a cherrytree end of file (xml format)"""
    file_ctd.write(
        """\n	</node>
</cherrytree>\n""")


def begin_node(file_ctd, protocol_name,id):
    """Begin a node <protocol_name> in the <file_ctd> cherrytree file"""
    file_ctd.write("""
		<node custom_icon_id="0" foreground="" is_bold="False" name=\"""" + protocol_name + """\" prog_lang="custom-colors" readonly="False" tags="" ts_creation="0.0" ts_lastsave="0.0" unique_id=\"""" + id + """\">""")

def end_node(file_ctd):
    """End a node <protocol_name> in the <file_ctd> cherrytree file"""
    file_ctd.write("""
		</node>""")


def begin_code(file_ctd):
    """Begin a codebox (shell)"""
    file_ctd.write("""
				<rich_text justification="left"></rich_text>""")
    file_ctd.write("""
				<codebox char_offset="0" frame_height="175" frame_width="750" highlight_brackets="True" show_line_numbers="False" syntax_highlighting="sh" width_in_pixels="True">""")


def end_code(file_ctd):
    """End a codebox (shell)"""
    file_ctd.write("""</codebox>""")