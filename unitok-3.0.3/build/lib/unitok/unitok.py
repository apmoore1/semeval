#!/usr/bin/env python
# coding=utf-8
"""
Universal tokenizer

This code was highly inspired by Laurent Pointal's TreeTagger wrapper:
https://perso.limsi.fr/pointal/dev:treetaggerwrapper

(c) 2009 Jan Pomikalek <jan.pomikalek@gmail.com>
Jan Michelfeit, Vit Suchomel <name.surname@sketchengine.co.uk> 2011-2015
"""

GLUE_TAG = u'<g/>'


def tokenize_recursively(text, re_list, depth=0):
    if depth >= len(re_list):
        return [('*', text)]
    token_type, regular_expr = re_list[depth]
    tokens = []
    pos = 0
    while pos < len(text):
        m = regular_expr.search(text, pos)
        if not m:
            tokens.extend(tokenize_recursively(text[pos:], re_list, depth+1))
            break
        else:
            startpos, endpos = m.span()
            if startpos > pos:
                tokens.extend(tokenize_recursively(text[pos:startpos], re_list, depth+1))
            tokens.append((token_type, text[startpos:endpos]))
            pos = endpos
    return tokens


def tokenize(text, configuration):
    re_list = configuration.re_list
    return tokenize_recursively(text, re_list)


def print_token(typ, val, debug):
    if debug:
        return '%s\t%s\n' % (typ, val)
    else:
        return '%s\n' % val 


def print_tokens(tokens, out, add_glue=True, debug=False):
    glue_here = False
    for typ, val in tokens:
        # replace newlines with spaces
        val = val.replace(u'\r', u' ').replace(u'\n', u' ')
        if typ == 'WHITESPACE':
            pass
            # if not add_glue:
            #     out.write(print_token(typ, val, debug))
            # glue_here = False
        elif typ == 'SGML_TAG':
            if val.startswith(u'</'):
                out.write(print_token(typ, val, debug))
            else:
                if add_glue and glue_here:
                    out.write(print_token('GLUE', GLUE_TAG, debug))
                out.write(print_token(typ, val, debug))
                glue_here = False
        else:
            # replace &lt; &gt; and &quot; outside of SGML tags
            val = val.replace(u'&lt;',u'<').replace(u'&gt;',u'>').replace(u'&quot;',u'"')
            if add_glue and glue_here:
                out.write(print_token('GLUE', GLUE_TAG, debug))
            out.write(print_token(typ, val, debug))
            glue_here = True


def import_config(config_path):
    import sys
    from os.path import abspath, dirname, basename
    from importlib import import_module
    sys.path.append(dirname(abspath(config_path)))
    name = basename(config_path)

    if name.endswith('.py'):
        name = name[:-3]
    return import_module(name)


if __name__ == "__main__":
    import argparse 
    import sys

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Description:
- splits input text into tokens (one token per line)
- for specified languages recognizes abbreviations and clictics (such as 've
  or n't in English)
- preserves SGML markup
- recognizes URLs, e-mail addreses, DNS domains, IP addresses
- adds glue (<g/>) tags between tokens not separated by space
- the output can be tagged with the TreeTagger part-of-speech tagger
    """)
    parser.add_argument("-n", "--no-glue", help="keep whitespace and don't add glue (<g/>) tags", action="store_true")
    parser.add_argument("-w", "--whole", help="read whole input at once (preserves multi-line tags; memory hungry)", action="store_true")
    parser.add_argument("-d", "--debug", help="show token types for debugging", action="store_true")
    parser.add_argument("CONFIG_FILE")
    args = parser.parse_args()
    # try:
    configuration = import_config(args.CONFIG_FILE)
    # except:
    #     sys.stderr.write('Invalid configuration file!\n')
    #     sys.exit(2)
    add_glue = not args.no_glue
    if args.whole:
        input_data = [sys.stdin.read()]
    else:
        input_data = sys.stdin

    for line in input_data:
        tokens = tokenize(line, configuration)
        print_tokens(tokens, sys.stdout, add_glue, args.debug)

