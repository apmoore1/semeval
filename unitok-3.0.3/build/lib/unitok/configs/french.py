# coding=utf-8

# Lists of clictics and abbreviations were taken from the TreeTagger:
# http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/
# Unicode table by script:
# http://jrgraphix.net/r/Unicode/

import sys, re

SGML_TAG = r"""
    (?:                         # make enclosing parantheses non-grouping
    <!-- .*? -->                # XML/SGML comment
    |                           # -- OR --
    <[!?/]?(?!\d)\w[-\.:\w]*    # Start of tag/directive
    (?:                         # Attributes
        [^>'"]*                 # - attribute name (+whitespace +equal sign)
        (?:'[^']*'|"[^"]*")     # - attribute value
    )*
    \s*                         # Spaces at the end
    /?                          # Forward slash at the end of singleton tags
    \s*                         # More spaces at the end
    >                           # +End of tag/directive
    )"""
SGML_TAG_RE = re.compile(SGML_TAG, re.UNICODE | re.VERBOSE | re.DOTALL)


IP_ADDRESS = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
IP_ADDRESS_RE = re.compile(IP_ADDRESS)

DNS_HOST = r"""
    (?:
        [-a-z0-9]+\.                # Host name
        (?:[-a-z0-9]+\.)*           # Intermediate domains
                                    # And top level domain below
        # http://data.iana.org/TLD/tlds-alpha-by-domain.txt (Version 2014112500, Last Updated Tue Nov 25 07:07:01 2014 UTC)
        (?:
        cancerresearch|
        international|
        construction|versicherung|
        accountants|blackfriday|contractors|engineering|enterprises|investments|motorcycles|photography|productions|williamhill|
        associates|bnpparibas|consulting|creditcard|cuisinella|foundation|healthcare|immobilien|industries|management|properties|republican|restaurant|technology|university|vlaanderen|
        allfinanz|bloomberg|christmas|community|directory|education|equipment|financial|furniture|institute|marketing|melbourne|solutions|vacations|
        airforce|attorney|bargains|boutique|brussels|budapest|builders|business|capetown|catering|cleaning|clothing|computer|delivery|democrat|diamonds|discount|engineer|exchange|feedback|firmdale|flsmidth|graphics|holdings|lighting|mortgage|partners|pharmacy|pictures|plumbing|property|saarland|services|software|supplies|training|ventures|yokohama|
        abogado|academy|android|auction|capital|caravan|careers|channel|college|cologne|company|cooking|country|cricket|cruises|dentist|digital|domains|exposed|finance|fishing|fitness|flights|florist|forsale|frogans|gallery|guitars|hamburg|holiday|hosting|kitchen|lacaixa|limited|network|neustar|okinawa|organic|realtor|recipes|rentals|reviews|schmidt|science|shiksha|singles|spiegel|support|surgery|systems|website|wedding|whoswho|youtube|
        active|agency|alsace|bayern|berlin|camera|career|center|chrome|church|claims|clinic|coffee|condos|credit|dating|degree|dental|direct|durban|emerck|energy|estate|events|expert|futbol|global|google|gratis|hiphop|insure|joburg|juegos|kaufen|lawyer|london|luxury|madrid|maison|market|monash|mormon|moscow|museum|nagoya|otsuka|photos|physio|quebec|reisen|repair|report|ryukyu|schule|social|supply|suzuki|sydney|taipei|tattoo|tienda|travel|viajes|villas|vision|voting|voyage|webcam|yachts|yandex|
        actor|archi|audio|autos|black|build|cards|cheap|citic|click|codes|cymru|dance|deals|email|gifts|gives|glass|globo|gmail|green|gripe|guide|homes|horse|house|jetzt|koeln|lease|loans|lotto|mango|media|miami|nexus|ninja|paris|parts|party|photo|pizza|place|poker|praxi|press|rehab|reise|rocks|rodeo|shoes|solar|space|tatar|tirol|today|tokyo|tools|trade|vegas|vodka|wales|watch|works|world|
        aero|army|arpa|asia|band|beer|best|bike|blue|buzz|camp|care|casa|cash|cern|city|club|cool|coop|desi|diet|dvag|fail|farm|fish|fund|gbiz|gent|gift|guru|haus|help|here|host|immo|info|jobs|kiwi|kred|land|lgbt|life|limo|link|ltda|luxe|meet|meme|menu|mini|mobi|moda|name|navy|pics|pink|pohl|post|prod|prof|qpon|reit|rest|rich|rsvp|ruhr|sarl|scot|sexy|sohu|surf|tips|town|toys|vote|voto|wang|wien|wiki|work|yoga|zone|
        axa|bar|bid|bio|biz|bmw|boo|bzh|cab|cal|cat|ceo|com|crs|dad|day|dnp|eat|edu|esq|eus|fly|foo|frl|gal|gle|gmo|gmx|gop|gov|hiv|how|ibm|ing|ink|int|kim|krd|lds|mil|moe|mov|net|new|ngo|nhk|nra|nrw|nyc|ong|onl|ooo|org|ovh|pro|pub|red|ren|rio|rip|sca|scb|soy|tax|tel|top|tui|uno|uol|vet|wed|wme|wtc|wtf|xxx|xyz|zip|
        ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cw|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|za|zm|zw
        )

        |

        localhost
    )"""

URL = r"""
    (?:

    # Scheme part
    (?:ftp|https?|gopher|mailto|news|nntp|telnet|wais|file|prospero)://

    # User authentication (optional)
    (?:[-a-z0-9_;?&=](?::[-a-z0-9_;?&=]*)?@)?

    # "www" without the scheme part
    |(?:www|web)\.

    )

    # DNS host / IP
    (?:
        """ + DNS_HOST + """
        |
        """ + IP_ADDRESS +"""
    )

    # Port specification (optional)
    (?::[0-9]+)?

    # Scheme specific extension (optional)
    (?:/[-\w;/?:@=&\$_.+!*'(~#%,]*)?
"""
URL_RE = re.compile(URL, re.VERBOSE | re.IGNORECASE | re.UNICODE)

EMAIL = r"[-a-z0-9._']+@" + DNS_HOST
EMAIL_RE = re.compile(EMAIL, re.VERBOSE | re.IGNORECASE)

# also matches initials
# FIXME! only match capital letters (?)
ACRONYM = r"""
    (?<!\w)     # should not be preceded by a letter
    # sequence of single letter followed by . (e.g. U.S.)
    (?:
        (?![\d_])\w         # alphabetic character
        \.
    )+
    # optionaly followed by a single letter (e.g. U.S.A)
    (?:
        (?![\d_])\w         # alphabetic character
        (?!\w)              # we don't want any more letters to follow
                            # we only want to match U.S. in U.S.Army (not U.S.A)
    )?
"""
ACRONYM_RE = re.compile(ACRONYM, re.UNICODE | re.VERBOSE)

# Better tokenization of abbreviations, model numbers, numbers
# VS 2013-07-15
# example: "The new B52 bombarder ISBN: 0440224780"
# before: ['The', 'new', 'B', '<g/>', '52', 'bombarder', 'ISBN', '<g/>', ':', '0', '<g/>', '440224780']
# after:  ['The', 'new', 'B52',             'bombarder', 'ISBN', '<g/>', ':', '0440224780']
# tested using top ~10M tokens from ententen12: 0.344 % wrongly placed <g/> corrected, no new mistakes introduced (briefly checked)
# regexp inspired by http://stackoverflow.com/questions/5224835/what-is-the-proper-regular-expression-to-match-all-utf-8-unicode-lowercase-lette
uu = []
for i in xrange(sys.maxunicode):
    c = unichr(i)
    if c.isupper():
        uu.append(c)
unicode_uppers = u''.join(uu)
ABBREVIATION_RE = re.compile(u'[0-9%s-]{2,}' % unicode_uppers)

MULTICHAR_PUNCTUATION = r"(?:[?!]+|``|'')"
MULTICHAR_PUNCTUATION_RE = re.compile(MULTICHAR_PUNCTUATION, re.VERBOSE)

# These punctuation marks should be tokenised to single characters
# even if a sequence of the same characters is found. For example,
# tokenise '(((' as ['(', '(', '('] rather than ['((('].
OPEN_CLOSE_PUNCTUATION = r"""
    [
        \u00AB \u2018 \u201C \u2039 \u00BB \u2019 \u201D \u203A \u0028 \u005B
        \u007B \u0F3A \u0F3C \u169B \u2045 \u207D \u208D \u2329 \u23B4 \u2768
        \u276A \u276C \u276E \u2770 \u2772 \u2774 \u27E6 \u27E8 \u27EA \u2983
        \u2985 \u2987 \u2989 \u298B \u298D \u298F \u2991 \u2993 \u2995 \u2997
        \u29D8 \u29DA \u29FC \u3008 \u300A \u300C \u300E \u3010 \u3014 \u3016
        \u3018 \u301A \u301D \uFD3E \uFE35 \uFE37 \uFE39 \uFE3B \uFE3D \uFE3F
        \uFE41 \uFE43 \uFE47 \uFE59 \uFE5B \uFE5D \uFF08 \uFF3B \uFF5B \uFF5F
        \uFF62 \u0029 \u005D \u007D \u0F3B \u0F3D \u169C \u2046 \u207E \u208E
        \u232A \u23B5 \u2769 \u276B \u276D \u276F \u2771 \u2773 \u2775 \u27E7
        \u27E9 \u27EB \u2984 \u2986 \u2988 \u298A \u298C \u298E \u2990 \u2992
        \u2994 \u2996 \u2998 \u29D9 \u29DB \u29FD \u3009 \u300B \u300D \u300F
        \u3011 \u3015 \u3017 \u3019 \u301B \u301E \u301F \uFD3F \uFE36 \uFE38
        \uFE3A \uFE3C \uFE3E \uFE40 \uFE42 \uFE44 \uFE48 \uFE5A \uFE5C \uFE5E
        \uFF09 \uFF3D \uFF5D \uFF60 \uFF63
    ]
"""
OPEN_CLOSE_PUNCTUATION_RE = re.compile(OPEN_CLOSE_PUNCTUATION, re.UNICODE | re.VERBOSE)


NUMBER_INTEGER_PART = r"""
    (?:
        0
        |
        [1-9][0-9]{0,2}(?:[ ,.][0-9]{3})+  # with thousand separators
        |
        [1-9][0-9]*
    )"""
NUMBER_DECIMAL_PART = r"""
    (?:
        [.,]
        [0-9]+
        (?:[eE][-+]?[0-9]+)?
    )"""
NUMBER = r"""
    (?:(?:\A|(?<=\s))[-+])?
    (?:
        %(integer)s %(decimal)s?
        |
        %(decimal)s
    )""" % {'integer': NUMBER_INTEGER_PART, 'decimal': NUMBER_DECIMAL_PART }

NUMBER_RE = re.compile(NUMBER, re.UNICODE | re.VERBOSE)

WHITESPACE = r"\s+"
WHITESPACE_RE = re.compile(WHITESPACE)

ANY_SEQUENCE = r"(.)\1*"
ANY_SEQUENCE_RE = re.compile(ANY_SEQUENCE)

HTMLENTITY = r"&(?:#x?[0-9]+|\w+);"
HTMLENTITY_RE = re.compile(HTMLENTITY)



clictics = re.compile(r"""
    (?:
        # left clictics
        (?<!\w)     # should not be preceded by a letter
        (?:
            [dcjlmnstDCJLNMST] | [Qq]u | [Jj]usqu | [Ll]orsqu
        )
        '   # apostrophe
        |
        # right clictics
        (?<=\w)     # should be preceded by a letter
        -   # hypen
        (?:
            # FIXME!
            -t-elles? | -t-ils? |
            -t-on | -ce | -elles? |
            -ils? | -je | -la | -les? |
            -leur | -lui | -m\u00eames? |
            -m' | -moi | -nous |
            -on | -toi | -tu |
            -t' | -vous | -en |
            -y | -ci | -l\u00e0
        )
        (?!w)      # should not be followed by a letter
    )
    """, re.UNICODE | re.VERBOSE)

abbreviations = re.compile(r"""
    (?<!\w)     # should not be preceded by a letter
    (?:
        rendez-vous|d'abord|d'accord|d'ailleurs|
        d'apr\u00e8s|d'autant|d'\u0153uvre|
        d'oeuvre|c'est-\u00e0-dire|
        moi-m\u00eame|toi-m\u00eame|lui-m\u00eame|
        elle-m\u00eame|nous-m\u00eames|vous-m\u00eames|
        eux-m\u00eames|elles-m\u00eames|par-ci|
        par-l\u00e0|Rendez-vous|D'abord|D'accord|
        D'ailleurs|D'apr\u00e8s|D'autant|
        D'\u0153uvre|D'oeuvre|
        C'est-\u00e0-dire|Moi-m\u00eame|
        Toi-m\u00eame|Lui-m\u00eame|Elle-m\u00eame|
        Nous-m\u00eames|Vous-m\u00eames|Eux-m\u00eames|
        Elles-m\u00eames|Par-ci|Par-l\u00e0
    )
    (?!w)      # should not be followed by a letter
    """, re.UNICODE | re.VERBOSE)

word = r"(?:(?![\d])[-\w])+"
word_re = re.compile(word, re.UNICODE)

re_list = [
    ('SGML_TAG', SGML_TAG_RE),
    ('WHITESPACE', WHITESPACE_RE),
    ('URL', URL_RE),
    ('EMAIL', EMAIL_RE),
    ('IP_ADDRESS', IP_ADDRESS_RE),
    ('HTMLENTITY', HTMLENTITY_RE),
    ('ABBREVIATION', abbreviations),
    ('CLICTIC', clictics),
    ('B52', ABBREVIATION_RE),
    ('NUMBER', NUMBER_RE),
    ('ACRONYM', ACRONYM_RE),
    ('WORD', word_re),
    ('MULTICHAR_PUNCTUATION', MULTICHAR_PUNCTUATION_RE),
    ('OPEN_CLOSE_PUNCTUATION', OPEN_CLOSE_PUNCTUATION_RE),
    ('ANY_SEQUENCE', ANY_SEQUENCE_RE),
]
