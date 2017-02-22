#!/usr/bin/python
import re
import codecs
from unicodedata import category, normalize
from htmlentitydefs import name2codepoint

HTMLENTITY_RE = re.compile(r"&(#x?[0-9A-F]+|\w+);")
SPECIAL_ENTITIES = ['gt', 'lt', 'quot']
def entity2unicode(mo, dont_convert):
    entity = mo.group(0)
    name = mo.group(1)
    if name in dont_convert:
        return entity
    if name.startswith('#'):
        if name.startswith('#x'):
            ordinal = int(name[2:], 16)
        else:
            ordinal = int(name[1:])
        try:
            return unichr(ordinal)
        except:
            return entity
    elif name2codepoint.has_key(name):
        return unichr(name2codepoint[name])
    else:
        return entity
def replace_html_entities(text, exceptions=[]):
    return HTMLENTITY_RE.sub(lambda mo: entity2unicode(mo, exceptions), text)

def remove_control_chars(text, exceptions=[]):
    return ''.join([c for c in text if c in exceptions or not category(c).startswith('C')])

def normalize_spaces(text):
    return ''.join([(' ' if category(c)=='Zs' else c) for c in text])

SINGLE_QUOTE_RE = re.compile(u'[\u0027\u0060\u00b4\u02bc\u055a\u07f4\u07f5\uff07\u2018\u2019\u201a\u201b\u2039\u203a\u275b\u275c\u02b9\u2032\u2035]')
DOUBLE_QUOTE_RE = re.compile(u'[\u0022\u276e\u276f\uff02\u201c\u201d\u201e\u201f\u00ab\u00bb\u301d\u301e\u301f\u275d\u275e\u2033\u2036\u02ba\u02ee]')
def normalize_quotes(text):
    text = SINGLE_QUOTE_RE.sub(u"'", text)
    text = DOUBLE_QUOTE_RE.sub(u'"', text)
    return text

HYPHEN_RE = re.compile(u'[\u002d\u058a\u05be\u1400\u1806\u2010\u2011\u2e17\u2e1a\u30a0\ufe63\uff0d]')
DASH_RE = re.compile(u'[\u2012\u2013\u2014\u2015\u2e3a\u2e3b\u2e40\u301c\u3030\ufe31\ufe32\ufe58]')
def normalize_dashes(text):
    text = HYPHEN_RE.sub(u'-', text)
    text = DASH_RE.sub(u'\u2013', text)
    return text

NEWLINE = {'unix': '\n', 'dos': '\r\n'}

if __name__ == "__main__":
    import sys, argparse
    parser = argparse.ArgumentParser(description='Universal text normalizer for linguistic research. Output is always UTF-8.')
    parser.add_argument("-e", "--encoding", help="input encoding (default:'utf_8')", default='utf_8')
    parser.add_argument("-d", "--decoding-errors", help="treatment of decoding errors (default:'replace', 'ignore' or 'strict')", default='replace')
    parser.add_argument("-f", "--normal-form", help="Unicode normal form (default:'NFKC', 'NFC', 'NFKD' or 'NFD')", default='NFKC')
    parser.add_argument("-t", "--tab", help="tab replacement (default:'space', 'tab' or 'none')", default='space')
    parser.add_argument("-p", "--paragraph-separator", help="paragraph separator replacement (default:'newline', 'space' or 'none')", default='newline')
    parser.add_argument("-l", "--line-separator", help="line separator replacement (default:'newline', 'space' or 'none')", default='newline')
    parser.add_argument("-n", "--new-line", help="new line character (default:'unix' or 'dos')", default='unix')
    parser.add_argument("-q", "--quotes", help="normalize quotes and apostrophes (default:off)", action="store_true")
    parser.add_argument("-a", "--dashes", help="normalize dashes and hyphens (default:off)", action="store_true")
    parser.add_argument("-s", "--dont-strip", help="keep leading and trailing whitespace (default:off)", action="store_true")
    parser.add_argument("-z", "--keep-empty", help="keep empty lines (default:off)", action="store_true")
    args = parser.parse_args()

    for bline in sys.stdin:
        line = bline.decode(args.encoding, errors=args.decoding_errors)
        line = normalize(args.normal_form, line)

        line = replace_html_entities(line, exceptions=SPECIAL_ENTITIES)

        if args.tab == 'space':
            line = line.replace('\t', ' ')
        elif args.tab == 'none':
            line = line.replace('\t', '')

        line = remove_control_chars(line, exceptions=['\t'])

        if args.paragraph_separator == 'newline':
            lines = line.split('\u2029')
        else:
            lines = [line]
        if args.line_separator == 'newline':
            lines = [line.split('\u2028') for line in lines]
        else:
            lines = [[line] for line in lines]
        lines = sum(lines, [])

        for line in lines:
            if args.paragraph_separator == 'space':
                line = line.replace('\u2029', ' ')
            else:
                line = line.replace('\u2029', '')
            if args.line_separator == 'space':
                line = line.replace('\u2028', ' ')
            else:
                line = line.replace('\u2028', '')

            line = normalize_spaces(line)

            if not args.dont_strip:
                line = line.strip()

            if args.keep_empty or len(line) > 0:
                if args.quotes:
                    line = normalize_quotes(line)

                if args.dashes:
                    line = normalize_dashes(line)

                sys.stdout.write(line.encode('utf_8'))
                sys.stdout.write(NEWLINE[args.new_line])
