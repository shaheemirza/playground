# https://github.com/ShadonSniper/RemoveWatermark
# https://gist.github.com/Daxda/9939745

# Author    : HeathLucas
# Date      : 11.30.2016
# WTF       : Remove it-ebooks.info watermarks on pdf file.
#             This may corrupt some pdf file,
#             There're some ways to converto it to normal pdf file.
#             My solution is open new_filename.pdf in chrome, then
#             click 'print' button and save.
#             It's simple. I don't know another way yet.
#             ShadonSniper's solution doesn't handle
#               /Type /Annot
#               /Subtype /Link
#               /Rect [ 111 19 195 7 ]
#               /Border [ 0 0 0 ]
#               /A <<
#               /Type /Action
#               /S /URI
#               /URI (http://www.it-ebooks.info/)
#               >>
#             and Daxda's solution doesn't handle
#               BT
#               1 0 0 1 0 0 Tm
#               (www.it-ebooks.info)Tj
#               ET
import os
import sys
import binascii
import optparse
import re

hex_link_pat = "".join("0A 3C 3C 0A 2F 54 79 70 65 20 2F 41 6E 6E 6F 74 0A 2F 53 75 "
                       "62 74 79 70 65 20 2F 4C 69 6E 6B 0A 2F 52 65 63 74 20 5B 20 "
                       "32 31 30 20 31 38 2E 35 20 32 39 34 20 36 2E 35 20 5D 0A 2F "
                       "42 6F 72 64 65 72 20 5B 20 30 20 30 20 30 20 5D 0A 2F 41 20 "
                       "3C 3C 0A 2F 54 79 70 65 20 2F 41 63 74 69 6F 6E 0A 2F 53 20 "
                       "2F 55 52 49 0A 2F 55 52 49 20 28 68 74 74 70 3A 2F 2F 77 77 "
                       "77 2E 69 74 2D 65 62 6F 6F 6B 73 2E 69 6E 66 6F 2F 29 0A 3E "
                       "3E 0A 3E 3E".split())

hex_text_pat = "".join("0A 42 54 0A 31 20 30 20 30 20 31 20 30 20 30 20 54 6D 0A 28 "
                       "77 77 77 2E 69 74 2D 65 62 6F 6F 6B 73 2E 69 6E 66 6F 29 54 "
                       "6A 0A 45 54".split())

pattern = """0a2f54797065202f416e6e6f740a2f53756274797065202f4c696e6b0a2f526563
74205b20.{0,35}?205d0a2f426f7264657220.{0,35}?\n0a2f41203c3c0a2f54797065202f416374696f6e0
a2f53202f5552490a2f5552492028687474703a2f2f7777772e69742d65626f6f6b732e696e666f
2f290a3e3e""".replace("\n", "").strip()

def remove_watermark(path):
    pdf_bin_data=""
    if os.path.exists(path) and path.endswith(".pdf"):
        try:
            with open(path,"rb") as f:
                pdf_bin_data = f.read()
                pdf_bin_data = pdf_bin_data.replace(binascii.unhexlify(hex_link_pat),"")
                pdf_bin_data = pdf_bin_data.replace(binascii.unhexlify(hex_text_pat),"")

                hex_pdf_data = pdf_bin_data.encode("hex")

                pdf_bin_data = re.sub(pattern, "", hex_pdf_data)
                pdf_bin_data = pdf_bin_data.replace("www.it-ebooks.info".encode("hex"), "")
        except IOError:
            sys.stderr.write("Error in opening file")
    else:
        raise ValueError("Path invalid or file is not in PDF format")
    return pdf_bin_data.decode("hex")

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog "+'-F <filepath>')
    parser.add_option('-F',dest='filepath',type='string',help='specify absolute path of pdf file')
    (options, args) = parser.parse_args()
    filepath = options.filepath
    if filepath == None:
        print parser.usage
        exit(0)
    newfile= 'new_'+os.path.split(filepath)[1]
    try:
        with open(newfile,'wb') as f:
            f.write(remove_watermark(filepath))
            f.close()
            print 'remove watermark done!'
    except IOError:
        sys.stderr.write("Problem in writing file.")
