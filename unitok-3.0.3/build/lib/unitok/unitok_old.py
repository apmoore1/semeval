#!/usr/bin/env python
# coding=utf-8
"""
Universal tokenizer

This code was highly inspired by Laurent Pointal's TreeTagger wrapper:
http://www.limsi.fr/Individu/pointal/python/treetaggerwrapper.py

Lists of clictics and abbreviations were taken from the TreeTagger:
http://www.ims.uni-stuttgart.de/projekte/corplex/TreeTagger/

Unicode table by script:
http://jrgraphix.net/r/Unicode/

(c) 2009 Jan Pomikalek <jan.pomikalek@gmail.com>
Jan Michelfeit, Vit Suchomel <name.surname@sketchengine.co.uk> 2011-2014
"""

import sys, re

### CONSTANTS #################################################################

# mostly taken from http://www.limsi.fr/Individu/pointal/python/treetaggerwrapper.py
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

SGML_END_TAG = r"</(?!\d)\w[-\.:\w]*>"
SGML_END_TAG_RE = re.compile(SGML_END_TAG, re.UNICODE)

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
DNS_HOST_RE = re.compile(DNS_HOST, re.VERBOSE | re.IGNORECASE)

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
ABBREVIATION_RE = re.compile(u'^[0-9%s-]{2,}$' % unicode_uppers)

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

PHONE_NUMBER = r"\+?[0-9]+(?:[-\u2012 ][0-9]+)*"
PHONE_NUMBER_RE = re.compile(PHONE_NUMBER, re.UNICODE)

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
        (?:[eE][-\u2212+]?[0-9]+)?
    )"""
NUMBER = r"""
    (?:(?:\A|(?<=\s))[-\u2212+])?
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

GLUE_TAG = u'<g/>'

### LANGUAGE DATA #############################################################

class LanguageSpecificData:
    clictics = None
    abbreviations = re.compile(r"""
(?<!\w)     # should not be preceded by a letter
(?:
    co\.|inc\.|ltd\.|dr\.|prof\.|jr\.
)
""", re.IGNORECASE | re.UNICODE | re.VERBOSE)
    word = r"(?:(?![\d])[-\u2010\w])+"
    word_re = re.compile(word, re.UNICODE)

class EnglishData(LanguageSpecificData):
    def __init__(self):
        self.clictics = re.compile(r"""
            (?:
                (?<=\w)     # only consider clictics preceded by a letter
                (?:
                    ['`\u2018\u2019\u2032](?:s|re|ve|d|m|em|ll)
                    |
                    n['`\u2018\u2019\u2032]t
                )
                |
                # cannot
                (?<=can)
                not
            )
            (?!\w)          # clictics should not be followed by a letter
            """, re.UNICODE | re.VERBOSE | re.IGNORECASE)

        self.abbreviations = re.compile(r"""
(?<!\w)     # should not be preceded by a letter
(?:
    Adm\.|Ala\.|Ariz\.|Ark\.|Aug\.|Ave\.|Bancorp\.|Bhd\.|Brig\.|
    Bros\.|CO\.|CORP\.|COS\.|Ca\.|Calif\.|Canada[-\u2010]U\.S\.|
    Canadian[-\u2010]U\.S\.|Capt\.|Cia\.|Cie\.|Co\.|Col\.|Colo\.|
    Conn\.|Corp\.|Cos\.|D[-\u2010]Mass\.|Dec\.|Del\.|Dept\.|Dr\.|
    Drs\.|Etc\.|Feb\.|Fla\.|Ft\.|Ga\.|Gen\.|Gov\.|Hon\.|INC\.|
    Ill\.|Inc\.|Ind\.|Jan\.|Japan[-\u2010]U\.S\.|Jr\.|Kan\.|
    Korean[-\u2010]U\.S\.|Ky\.|La\.|Lt\.|Ltd\.|Maj\.|Mass\.|Md\.|
    Messrs\.|Mfg\.|Mich\.|Minn\.|Miss\.|Mo\.|Mr\.|Mrs\.|Ms\.|Neb\.
    |Nev\.|No\.|Nos\.|Nov\.|Oct\.|Okla\.|Ont\.|Ore\.|Pa\.|Ph\.|
    Prof\.|Prop\.|Pty\.|Rep\.|Reps\.|Rev\.|S\.p\.A\.|Sen\.|Sens\.|
    Sept\.|Sgt\.|Sino[-\u2010]U\.S\.|Sr\.|St\.|Ste\.|Tenn\.|Tex\.|
    U\.S\.[-\u2010]U\.K\.|U\.S\.[-\u2010]U\.S\.S\.R\.|Va\.|Vt\.|W\.Va\.|
    Wash\.|Wis\.|Wyo\.|a\.k\.a\.|a\.m\.|anti[-\u2010]U\.S\.|cap\.|
    etc\.|ft\.|i\.e\.|non[-\u2010]U\.S\.|office/dept\.|p\.m\.|
    president[-\u2010]U\.S\.|s\.r\.l\.|v\.|v\.B\.|v\.w\.|vs\.
)
""", re.UNICODE | re.VERBOSE)

class FrenchData(LanguageSpecificData):
    def __init__(self):
        self.clictics = re.compile(r"""
            (?:
                # left clictics
                (?<!\w)     # should not be preceded by a letter
                (?:
                    [dcjlmnstDCJLNMST] | [Qq]u | [Jj]usqu | [Ll]orsqu
                )
                ['\u2019]   # apostrophe
                |
                # right clictics
                (?<=\w)     # should be preceded by a letter
                [-\u2010]   # hypen
                (?:
                    # FIXME!
                    [-\u2010]t[-\u2010]elles? | [-\u2010]t[-\u2010]ils? |
                    [-\u2010]t[-\u2010]on | [-\u2010]ce | [-\u2010]elles? |
                    [-\u2010]ils? | [-\u2010]je | [-\u2010]la | [-\u2010]les? |
                    [-\u2010]leur | [-\u2010]lui | [-\u2010]m\u00eames? |
                    [-\u2010]m['\u2019] | [-\u2010]moi | [-\u2010]nous |
                    [-\u2010]on | [-\u2010]toi | [-\u2010]tu |
                    [-\u2010]t['\u2019] | [-\u2010]vous | [-\u2010]en |
                    [-\u2010]y | [-\u2010]ci | [-\u2010]l\u00e0
                )
                (?!w)      # should not be followed by a letter
            )
            """, re.UNICODE | re.VERBOSE)

        self.abbreviations = re.compile(r"""
(?<!\w)     # should not be preceded by a letter
(?:
    rendez[-\u2010]vous|d['\u2019]abord|d['\u2019]accord|d['\u2019]ailleurs|
    d['\u2019]apr\u00e8s|d['\u2019]autant|d['\u2019]\u0153uvre|
    d['\u2019]oeuvre|c['\u2019]est[-\u2010]\u00e0[-\u2010]dire|
    moi[-\u2010]m\u00eame|toi[-\u2010]m\u00eame|lui[-\u2010]m\u00eame|
    elle[-\u2010]m\u00eame|nous[-\u2010]m\u00eames|vous[-\u2010]m\u00eames|
    eux[-\u2010]m\u00eames|elles[-\u2010]m\u00eames|par[-\u2010]ci|
    par[-\u2010]l\u00e0|Rendez[-\u2010]vous|D['\u2019]abord|D['\u2019]accord|
    D['\u2019]ailleurs|D['\u2019]apr\u00e8s|D['\u2019]autant|
    D['\u2019]\u0153uvre|D['\u2019]oeuvre|
    C['\u2019]est[-\u2010]\u00e0[-\u2010]dire|Moi[-\u2010]m\u00eame|
    Toi[-\u2010]m\u00eame|Lui[-\u2010]m\u00eame|Elle[-\u2010]m\u00eame|
    Nous[-\u2010]m\u00eames|Vous[-\u2010]m\u00eames|Eux[-\u2010]m\u00eames|
    Elles[-\u2010]m\u00eames|Par[-\u2010]ci|Par[-\u2010]l\u00e0
)
(?!w)      # should not be followed by a letter
""", re.UNICODE | re.VERBOSE)

class ItalianData(LanguageSpecificData):
    def __init__(self):
        self.clictics = re.compile(r"""
            (?:
                # left clictics
                (?<!\w)     # should not be preceded by a letter
                (?:
                    [dD][ae]ll | [nN]ell | [Aa]ll | [lLDd] | [Ss]ull | [Qq]uest |
                    [Uu]n | [Ss]enz | [Tt]utt
                )
                ['\u2019]   # apostrophe
                (?=\w)      # should be followed by a letter
            )
            """, re.UNICODE | re.VERBOSE)

        self.abbreviations = re.compile(r"""
            (?<!\w)     # should not be preceded by a letter
            (?:
                L\. | Lit\. | art\. | lett\. | n\. | no\. | pagg\. | prot\. | tel\.
            )
            """, re.UNICODE | re.VERBOSE)

class GermanData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these can be preceded by a letter
    (?:
        [-\u2010]hdg\.|[-\u2010]tlg\.
    )
    |
    # these should not be preceded by a letter
    (?<!\w)
    (?:
        # from http://en.wiktionary.org/wiki/Category:German_abbreviations
        AB[-\u2010]Whg\.|Abl\.|Bio\.|Bj\.|Blk\.|Eigent\.[-\u2010]Whg\.|
        Eigent\.[-\u2010]Whgn\.|Eigt\.[-\u2010]Whg\.|Eigt\.[-\u2010]Whgn\.|Fr\.|
        Gal\.|Gart\.ant\.|Grd\.|Grdst\.|Hdt\.|Jg\.|Kl\.[-\u2010]Whg\.|
        Kl\.[-\u2010]Whgn\.|Mais\.[-\u2010]Whg\.|Mais\.[-\u2010]Whgn\.|Mio\.|
        Mrd\.|NB[-\u2010]Whg\.|Nb\.[-\u2010]Whg\.|Nb\.[-\u2010]Whgn\.|Nfl\.|
        Pak\.|Prov\.|Sout\.|Tsd\.|Whg\.|Whgn\.|Zi\.|Ziegelbauw\.|
        Ztr\.[-\u2010]Hzg\.|Ztrhzg\.|Zw\.[-\u2010]Whg\.|Zw\.[-\u2010]Whgn\.|
        abzgl\.|bezugsf\.|bzgl\.|bzw\.|d\.[ ]h\.|engl\.|freist\.|frz\.|
        i\.[ ]d\.[ ]R\.|m\u00f6bl\.|ren\.|ren\.bed\.|rest\.|san\.|usw\.|
        z\.[ ]B\.|zz\.|zzgl\.|zzt\.
    )
)
""", re.UNICODE | re.VERBOSE)

class DutchData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these can be preceded by a letter
    (?:
        ['\u2019]t | ['\u2019]s | ['\u2019]n
    )
    |
    # these should not be preceded by a letter
    (?<!\w)
    (?:
        2bis\.|3bis\.|7bis\.|AR\.|Actualit\.|Afd\.|Antw\.|Arbh\.|Art\.|
        B\.St\.|B\.s\.|Besl\.W\.|Bull\.|Bull\.Bel\.|Cass\.|Cf\.|
        Com\.I\.B\.|D\.t/V\.I\.|Dhr\.|Doc\.|Dr\.|Fisc\.|Fr\.|Gec\.|II\.
        |III\.|J\.[-\u2010]L\.M\.|NR\.|NRS\.|Nat\.|No\.|Nr\.|Onderafd\.|
        PAR\.|Par\.|RECHTSFAK\.|RKW\.|TELEF\.|Volksvert\.|Vr\.|a\.|
        adv\.[-\u2010]gen\.|afd\.|aj\.|al\.|arb\.|art\.|artt\.|b\.|
        b\.v\.|b\.w\.|bijv\.|blz\.|bv\.|c\.q\.|cf\.|cfr\.|concl\.|d\.
        |d\.d\.|d\.i\.|d\.w\.z\.|dd\.|doc\.|e\.|e\.d\.|e\.v\.|enz\.|
        f\.|fr\.|g\.w\.|gepubl\.|i\.p\.v\.|i\.v\.m\.|j\.t\.t\.|jl\.|
        k\.b\.|kol\.|m\.b\.t\.|m\.i\.|max\.|n\.a\.v\.|nl\.|nr\.|nrs\.|
        o\.a\.|o\.b\.s\.i\.|o\.m\.|opm\.|p\.|par\.|pct\.|pp\.|ref\.|
        resp\.|respekt\.|t\.a\.v\.|t\.o\.v\.|vb\.|w\.
    )
)
""", re.UNICODE | re.VERBOSE)

class SpanishData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
            (?<!\w)     # should not be preceded by a letter
            (?:
                Ref\. | Vol\. | etc\. | App\. | Rec\.
            )
            """, re.UNICODE | re.VERBOSE)

class CzechData(LanguageSpecificData):
    def __init__(self):
        self.clictics = re.compile(r"""
            (?:
                (?<=\w)     # only consider clictics preceded by a letter
                -li
            )
            (?!\w)          # clictics should not be followed by a letter
            """, re.UNICODE | re.VERBOSE | re.IGNORECASE)
        self.abbreviations = re.compile(r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
#Generated from http://cs.wiktionary.org/wiki/Kategorie:%C4%8Cesk%C3%A9_zkratky by Makefile.Czech.abbr
např\.|mudr\.|abl\.|absol\.|adj\.|adv\.|ak\.|ak\. sl\.|alch\.|amer\.|anat\.|angl\.|anglosas\.|archit\.|arg\.|astr\.|astrol\.|att\.|bás\.|belg\.|bibl\.|biol\.|boh\.|bulh\.|círk\.|csl\.|č\.|čes\.|dět\.|dial\.|dór\.|dopr\.|dosl\.|ekon\.|el\.|epic\.|eufem\.|f\.|fam\.|fem\.|fil\.|form\.|fr\.|fut\.|fyz\.|gen\.|geogr\.|geol\.|geom\.|germ\.|hebr\.|herald\.|hist\.|hl\.|hud\.|hut\.|chcsl\.|chem\.|ie\.|imp\.|impf\.|ind\.|indoevr\.|inf\.|instr\.|interj\.|iron\.|it\.|katalán\.|kniž\.|komp\.|konj\.|konkr\.|kř\.|kuch\.|lat\.|lit\.|liturg\.|lok\.|m\.|mat\.|mod\.|ms\.|n\.|náb\.|námoř\.|neklas\.|něm\.|nesklon\.|nom\.|ob\.|obch\.|obyč\.|ojed\.|opt\.|pejor\.|pers\.|pf\.|pl\.|plpf\.|prep\.|předl\.|přivl\.|r\.|rcsl\.|refl\.|reg\.|rkp\.|ř\.|řec\.|s\.|samohl\.|sg\.|sl\.|souhl\.|spec\.|srov\.|stfr\.|střv\.|stsl\.|subj\.|subst\.|superl\.|sv\.|sz\.|táz\.|tech\.|telev\.|teol\.|trans\.|typogr\.|var\.|verb\.|vl\. jm\.|voj\.|vok\.|vůb\.|vulg\.|výtv\.|vztaž\.|zahr\.|zájm\.|zast\.|zejm\.|zeměd\.|zkr\.|zř\.|mj\.|dl\.|atp\.|mgr\.|horn\.|mvdr\.|judr\.|rsdr\.|bc\.|phdr\.|thdr\.|ing\.|aj\.|apod\.|pharmdr\.|pomn\.|ev\.|nprap\.|odp\.|dop\.|pol\.|st\.|stol\.|p\. n\. l\.|před n\. l\.|n\. l\.|př\. kr\.|po kr\.|př\. n\. l\.|odd\.|rndr\.|tzv\.|atd\.|tzn\.|resp\.|tj\.|p\.|br\.|č\. j\.|čj\.|č\. p\.|čp\.|a\. s\.|s\. r\. o\.|spol\. s r\. o\.|p\. o\.|s\. p\.|v\. o\. s\.|k\. s\.|o\. p\. s\.|o\. s\.|v\. r\.|v z\.|ml\.|vč\.|kr\.|mld\.|popř\.|ap\.|event\.|švýc\.|p\. t\.|zvl\.|hor\.|dol\.|plk\.|pplk\.|mjr\.|genmjr\.|genpor\.|kpt\.|npor\.|por\.|ppor\.|prap\.|pprap\.|rtm\.|rtn\.|des\.|svob\.|adm\.|brit\.|býv\.|čín\.|fin\.|chil\.|jap\.|nám\.|niz\.|špan\.|tur\.|bl\.|mga\.|zn\.|říj\.|etnonym\.|b\. k\.|škpt\.|nrtm\.|nstržm\.|stržm\.|genplk\.|šprap\.|št\. prap\.|brig\. gen\.|arm\. gen\.|doc\.|prof\.|csc\.|bca\.|dis\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class SlovakData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
# Recycled from CzechData ("traslated" & updated)
        ap\.|apod\.|atď\.|napr\.|obyč\.|pod\.|skr\.|zn\.|
        abl\.|absol\.|adj\.|adv\.|ak\.|alch\.|amer\.|anat\.|angl\.|anglosas\.|
        arch\.|archit\.|arg\.|astr\.|astrol\.|att\.|
        bás\.|ban\.|belg\.|bibl\.|biol\.|boh\.|bulh\.|
        cirk\.|csl\.|
        čes\.|čs\.|čsl\.|
        det\.|dial\.|dór\.|dopr\.|dosl\.|
        ekon\.|el\.|epic\.|eufem\.|
        fam\.|fem\.|fil\.|fin\.|fín\.|form\.|fr\.|fut\.|fyz\.|
        geogr\.|geol\.|gréc\.|geom\.|germ\.|
        hebr\.|herald\.|hist\.|hl\.|hud\.|hut\.|
        chcsl\.|chem\.|
        imp\.|impf\.|ind\.|indoeur\.|inf\.|instr\.|interj\.|iron\.|
        katalán\.|kniž\.|komp\.|konj\.|konkr\.|kuch\.|
        lat\.|lit\.|liturg\.|lok\.|ľud\.|
        maď\.|mat\.|mod\.|ms\.|
        náb\.|námor\.|neklas\.|nem\.|nesklon\.|nom\.|
        ob\.|obch\.|okr\.|ojed\.|opyt\.|
        pejor\.|pers\.|pf\.|pl\.|plpf\.|poľ\.|poľnohosp\.|prep\.|predl\.|privl\.|
        rcsl\.|refl\.|reg\.|rkp\.|rus\.|
        samohl\.|sg\.|sl\.|slov\.|stfr\.|strv\.|stsl\.|subj\.|subst\.|superl\.|sz\.|
        špec\.|švajč\.|
        tal\.|tech\.|telev\.|teol\.|trans\.|typogr\.|
        ukr\.|
        var\.|verb\.|vl\.|voj\.|vok\.|vulg\.|výtv\.|vzťaž\.|
        zahr\.|zám\.|zast\.|
        ev\.|kat\.|kr\.|rím\.|sv\.|
        bc\.|mgr\.|ing\.|
        dr\.|judr\.|mudr\.|mvdr\.|paeddr\.|pharmdr\.|phdr\.|phmr\.|rndr\.|rsdr\.|thdr\.|
        doc\.|prof\.|
        csc\.|drsc\.|phd\.|bca\.|
        pomn\.|nprap\.|odp\.|dop\.|pol\.|st\.|stol\.|p\. n\. l\.|odd\.|tzv\.|atd\.|tzn\.|resp\.|
        ml\.|mld\.|event\.|zvl\.|hor\.|dol\.|niž\.|vyš\.|
        gen\.|plk\.|pplk\.|mjr\.|genmjr\.|genpor\.|genplk\.|kpt\.|npor\.|por\.|ppor\.|
        prap\.|pprap\.|rtm\.|rtn\.|des\.|slob\.|nrtm\.|nstržm\.|stržm\.|šprap\.|
        adm\.|brit\.|býv\.|čín\.|fín\.|chil\.|jap\.|nám\.|špan\.|tur\.|
        bl\.|mga\.|etnonym\.|škpt\.|dis\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class HindiData(LanguageSpecificData):
    def __init__(self):
        #Devanagari script = \u0900-\u097f
        self.word = r"(?:(?![\d])[-\u2010\u0900-\u097f\w])+"
        self.word_re = re.compile(self.word, re.UNICODE)

class NorwegianData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    (?<!\w)
    (?:
#http://norwegianlanguage.info/grammar/abbrev.html
alm\.|ang\.|A/S|bl\.a\.|ca\.|d\.e\.|d\.s\.|d\.s\.s\.|d\.v\.s\.|d\.y\.|d\.e\.|eg\.|egl\.|e\.Kr\.|el\.|ev\.|f\.|f\.eks\.|fhv\.|f\.Kr\.|fr\.o\.m\.|frk\.|følg\.|g\.|ggr\.|hr\.|i\.st\.f\.|jf\.|jfr\.|kgl\.|kl\.|m\.|m\.a\.o\.|m\.fl\.|m\.h\.t\.|m\.m\.|N\.N\.|nr\.|obs\!|o\.fl\.|O\.l\.|omkr\.|o\.s\.v\.|p\.g\.a\.|s\.|s\.k\.|sml\.|t\.d\.|t\.h\.|t\.o\.m\.|t\.v\.|utg\.|vanl\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class SwedishData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
#http://en.wiktionary.org/wiki/Category:Swedish_abbreviations
1:a|2:a|3:a|4:a|5:a|6:a|7:a|8:a|9:a|10:a|11:a|12:a|13:a|14:a|15:a|16:a|17:a|18:a|19:a|20:a|21:a|22:a|23:a|24:a|25:a|26:a|27:a|28:a|29:a|30:a|31:a|1:e|2:e|3:e|4:e|5:e|6:e|7:e|8:e|9:e|10:e|11:e|12:e|13:e|14:e|15:e|16:e|17:e|18:e|19:e|20:e|21:e|22:e|23:e|24:e|25:e|26:e|27:e|28:e|29:e|30:e|31:e|ack\.|adj\.|adv\.|amer\.|anat\.|anv\.|Apg\.|arab\.|aram\.|arkeol\.|arkit\.|astr\.|bankv\.|bet\.|betyd\.|bibl\.|bildl\.|biol\.|bl\.a\.|bokf\.|boktr\.|bot\.|d\.|d\.v\.s\.|d\.y\.|d\.ä\.|da\.|data\.|cont\.|dets\.|dial\.|dim\.|Dr\.|dvs\.|e\.d\.|e\.dyl\.|e\.Kr\.|e\.m\.|eg\.|ekon\.|el\.|eng\.|etc\.|ev\.|ex\.|exkl\.|f\.|f\.d\.|f\.Kr\.|f\.m\.|f\.v\.t\.|fam\.|fem\.|fig\.|fil\.|filos\.|fonet\.|forneng\.|fornfra\.|fornhögty\.|fr\.|fr\.o\.m\.|fra\.|fsv\.|fys\.|förk\.|geogr\.|geol\.|geom\.|germ\.|got\.|grek\.|hand\.|hebr\.|hist\.|holl\.|ibl\.|cont\.|imperf\.|inf\.|ink\.|inkl\.|inst\.|interj\.|it\.|jap\.|jmf\.|jur\.|kem\.|kl\.|komp\.|konst\.|l\.|lat\.|litt\.|log\.|m\.fl\.|m\.m\.|mask\.|mat\.|med\.|medeleng\.|medelholl\.|medelhögty\.|medellågty\.|medeltidslat\.|meteor\.|mil\.|miner\.|mus\.|myt\.|N\.N\.|neds\.|neutr\.|no\.|nr\.|o\.d\.|o\.dyl\.|o\.s\.v\.|oböjl\.|omkr\.|osv\.|p\.g\.a\.|p\.m\.s\.|p\.s\.s\.|part\.|pedag\.|perf\.part\.|pers\.|plur\.|polit\.|port\.|prep\.|pres\.part\.|pron\.|psykol\.|real\.|resp\.|runsv\.|ry\.|s\.a\.s\.|s\.k\.|s\.ö\.|senlat\.|sing\.|sjö\.|skämts\.|sl\.|spa\.|sport\.|språkv\.|subst\.|särsk\.|t\.|t\. ex\.|t\.ex\.|t\.o\.m\.|tekn\.|teol\.|tex\.|cont\.|tr\.|ty\.|v\.t\.|vanl\.|vard\.|vers\.|vulgärlat\.|y\.|zool\.|ä\.|äv\.|åld\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class FinnishData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
#http://en.wiktionary.org/wiki/Category:Finnish_abbreviations
#http://fi.wiktionary.org/wiki/Luokka:Suomen_kielen_lyhenteet
aik\.|akk\.|alk\.|alv\.|ao\.|ap\.|Ap\. t.|ark\.|as\.|ay\.|Bar\.|Dan\.|dat\.|dem\.pron.|Did\.|dipl\.ins\.|Ef\.|eKr\.|em\.|ent\.|esim\.|evp\.|f\.|Fil\.|Filem\.|Gal\.|gen\.|Hab\.|Hagg\.|Hepr\.|Hes\.|Hoos\.|huom\.|ib\.|id\.|Ilm\.|imperf\.|inf\.|ip\.|it\.|Jaak\.|Jer\.|Jes\.|jKr\.|jne\.|Joh\.|joht\.|Joos\.|Juud\.|k\.|ka\.|kand\.|kapt\.|kenr\.|kers\.|kesk\.|ko\.|kok\.|Kol\.|kompp\.|Kor\.|ks\.|kts\.|Kun\.|kuv\.|kv\.|l\.|Laul\. l.|lis\.|lk\.|lkm\.|ltn\.|Luuk\.|lyh\.|läh\.|ma\.|Makk\.|Mal\.|Man\. r.|Mark\.|Matt\.|milj\.|ml\.|mlk\.|mm\.|mom\.|mon\.|Moos\.|M\.O.T.|mpy\.|mt\.|mts\.|mv\.|mvs\.|n\.|Nah\.|Neh\.|N\.N.|nom\.|ns\.|nyk\.|Ob\.|om\.|op\.|o\.s.|os\.|oy\.|p\.|par\.|part\.|perf\.|Piet\.|pj\.|pl\.|pluskv\.|po\.|prees\.|prof\.|pron\.|Ps\.|ps\.|puh\.|pvm\.|rek\.|Room\.|rp\.|s\.|Saarn\.|Sak\.|Sam\.|Sananl\.|Sef\.|sek\.|Sir\.|sit\.|so\.|srk\.|subst\.|synt\.|t\.|tark\.|tav\.|tekn\.|Tess\.|Tim\.|Tit\.|tjs\.|tms\.|Tob\.|toim\.|toim\. huom.|toim\.joht\.|ts\.|Tuom\.|ups\.|us\.|v\.|vak\.|Valit\.|vanh\.|vars\.|vas\.|vast\.|Vihr\.|Viis\.|v\.p.|vpj\.|vrt\.|vs\.|vt\.|vv\.|vänr\.|vääp\.|yht\.|yks\.|yl\.|ylik\.|ylim\.|ylip\.|yliv\.|ylimatr\.|ym\.|yms\.|yo\.|yv\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class GreekData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
#http://en.wiktionary.org/wiki/Category:Greek_abbreviations
ά\.|αβέβ\.|αγγλ\.|άγν\.|αιτ\.|βλ\.|γεν\.|εκ\.|κεφ\.|μ\.μ.|ον\.|ονομ\.|π\.μ.|πβ\.|πρβ\.|πρβλ\.|σ\.|σσ\.|τ\.|τομ\.|φ\.|φφ\.|χγ\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class DanishData(LanguageSpecificData):
    def __init__(self):
        self.abbreviations = re.compile(r"""
(?:
    # these should not be preceded by a letter
    (?<!\w)
    (?:
#http://en.wiktionary.org/wiki/Category:Danish_abbreviations
#http://da.wiktionary.org/wiki/Kategori:Forkortelser_på_dansk
alm\.|beg\.|besl\.m.|bf\.|bl\.a.|ca\.|cet\. par.|d\.s.s.|dvs\.|e\.v.t.|etc\.|evt\.|f\.eks.|fr\.|frk\.|hr\.|jf\.|kg·m|max\.|mht\.|min\.|osv\.|p\.t.|pct\.|pga\.|pl\.|resp\.|tlf\.|vha\.
    )
)
""", re.UNICODE | re.VERBOSE | re.IGNORECASE)

class MaldivianThaanaData(LanguageSpecificData):
    #http://en.wikipedia.org/wiki/Thaana
    word_re = re.compile(u'[\w\u0780-\u07bf]+')

class YorubaData(LanguageSpecificData):
    #http://diacritics.typo.cz/index.php?id=71
    _yo1 = r'\u00e1\u00c1\u00e2\u00c2\u01ce\u01cd\u00e9\u00c9\u00ea\u00ca\u011b\u011a\u1eb9\u1eb8\u1ec7\u1ec6\u00ed\u00cd'
    _yo2 = r'\u00ee\u00ce\u01d0\u01cf\u00f3\u00d3\u00f4\u00d4\u01d2\u01d1\u1ecd\u1ecc\u0300\u0301\u0303\u0304\u030c'
    #http://www.geocities.ws/click2speak/unicode/chars_yo.html
    _yo3 = r'\u00c0\u00c8\u00cc\u00d2\u00d9\u00da\u00e0\u00e8\u00ec\u00f2\u00f9\u00fa\u1e62\u1e63'
    #additional spotted accidentally
    _yo4 = r'\u01f9\u031f'
    word_re = re.compile(u'[\w%s%s%s%s]+' % (_yo1, _yo2, _yo3, _yo4))

class DevanagariData(LanguageSpecificData):
    #http://en.wikipedia.org/wiki/Devanagari#Unicode
    word_re = re.compile(u'[\w\u0900-\u097f\ua8e0-\ua8ff]+')

class ScottishGaelicData(LanguageSpecificData):
    #http://en.wikipedia.org/wiki/Scottish_Gaelic_orthography
    word_re = re.compile(u"[\wàèìòùÀÈÌÒÙ´'-]+")


LANGUAGE_DATA = {
    'english': EnglishData,
    'french' : FrenchData,
    'german' : GermanData,
    'italian': ItalianData,
    'spanish': SpanishData,
    'dutch'  : DutchData,
    'czech'  : CzechData,
    'slovak' : SlovakData,
    'hindi'  : HindiData,
    'norwegian': NorwegianData,
    'swedish': SwedishData,
    'finnish': FinnishData,
    'greek'  : GreekData,
    'danish' : DanishData,
    'maldivian': MaldivianThaanaData,
    'yoruba' : YorubaData,
    'devanagari': DevanagariData,
    'scottish-gaelic': ScottishGaelicData,
    'other'  : LanguageSpecificData,
}

### CODE #####################################################################

def tokenise_recursively(text, re_list, depth=0):
    if depth >= len(re_list):
        return [text]
    regular_expr = re_list[depth]
    tokens = []
    pos = 0
    while pos < len(text):
        m = regular_expr.search(text, pos)
        if not m:
            tokens.extend(tokenise_recursively(text[pos:], re_list, depth+1))
            break
        else:
            startpos, endpos = m.span()
            if startpos > pos:
                tokens.extend(tokenise_recursively(text[pos:startpos], re_list, depth+1))
            tokens.append(text[startpos:endpos])
            pos = endpos
    return tokens

def glue_tokens(tokens):
    glued_tokens = []
    should_add_glue = False
    for token in tokens:
        if WHITESPACE_RE.match(token):
            should_add_glue = False
        elif SGML_END_TAG_RE.match(token):
            glued_tokens.append(token)
        elif SGML_TAG_RE.match(token):
            if should_add_glue:
                glued_tokens.append(GLUE_TAG)
            glued_tokens.append(token)
            should_add_glue = False
        else:
            if should_add_glue:
                glued_tokens.append(GLUE_TAG)
            glued_tokens.append(token)
            should_add_glue = True
    return glued_tokens

def normalise(text):
    from uninorm import replace_html_entities, SPECIAL_ENTITIES, remove_control_chars, normalize_spaces
    text = replace_html_entities(text, exceptions=SPECIAL_ENTITIES)
    text = remove_control_chars(text, exceptions=[u'\t', u'\n'])
    return normalize_spaces(text)

def tokenise(text, lsd=LanguageSpecificData(), add_glue=True, universal_abbreviations=True):
    re_list = [
        SGML_TAG_RE,
        WHITESPACE_RE,
        URL_RE,
        EMAIL_RE,
        IP_ADDRESS_RE,
        #PHONE_NUMBER_RE,
        HTMLENTITY_RE,
    ]
    if lsd.abbreviations:
        re_list.append(lsd.abbreviations)
    if lsd.clictics:
        re_list.append(lsd.clictics)
    if universal_abbreviations:
        re_list.append(ABBREVIATION_RE)
    re_list.extend([
        NUMBER_RE,
        ACRONYM_RE,
        lsd.word_re,
        MULTICHAR_PUNCTUATION_RE,
        OPEN_CLOSE_PUNCTUATION_RE,
        ANY_SEQUENCE_RE,
    ])

    tokens = tokenise_recursively(text, re_list)

    # replace &lt; &gt; and &quot; outside of SGML tags
    tokens = [t if SGML_TAG_RE.match(t) else t.replace(u'&lt;',u'<').replace(u'&gt;',u'>').replace(u'&quot;',u'"') for t in tokens]

    # replace newlines with spaces
    tokens = [re.sub("[\r\n]", " ", t) for t in tokens]

    if add_glue:
        return glue_tokens(tokens)
    else:
        return tokens


if __name__ == "__main__":
    import codecs
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s [OPTIONS] [FILES...]",
        description="Tokenize FILES or standard input.",
        epilog="""Description:
- splits input text into tokens (one token per line)
- for specified languages recognizes abbreviations and clictics (such as 've
  or n't in English)
- preserves SGML markup
- replaces SGML entities with unicode equivalents
- recognizes URLs, e-mail addreses, DNS domains, IP addresses
- adds glue (<g/>) tags between tokens not separated by space
- the output can be tagged with the TreeTagger part-of-speech tagger
    """)
    parser.add_argument("-l", "--language", default='english', help="language of the input (supported: %s; defaults to english)" % ', '.join(sorted(LANGUAGE_DATA.keys())))
    parser.add_argument("-e", "--encoding", default='utf_8', help="character encoding of the input (one of Codec or Alias values at http://docs.python.org/library/codecs.html#id3 ; defaults to 'utf_8')")
    parser.add_argument("-a", "--abbreviations", help="better support for abbreviations (a.k.a. B52)", action="store_true")
    parser.add_argument("-n", "--no-glue", help="do not add glue (<g/>) tags", action="store_true")
    parser.add_argument("-s", "--stream", help="process input line by line (WARNING: splits SGML tags if on multiple lines)", action="store_true")
    parser.add_argument("FILES", nargs="*", default='-')
    args = parser.parse_args()
    try:
        lsd = LANGUAGE_DATA[args.language.lower()]()
    except:
        sys.stderr.write("unsupported language: %s\n" % args.language)
        sys.stderr.write("supported languages: %s\n" % ", ".join(LANGUAGE_DATA.keys()))
        sys.exit(2)
    try:
        codecs.lookup(args.encoding)
        encoding = args.encoding
    except LookupError:
        sys.stderr.write("unknown encoding: %s\n" % args.encoding)
        sys.exit(2)
    add_glue = not args.no_glue
    quiet = False

    if args.stream:
        import fileinput
        for line in fileinput.input(args.FILES):
            try:
                uline = unicode(line, encoding)
            except UnicodeDecodeError as detail:
                if not quiet:
                    sys.stderr.write("warning: %s, line %i: %s" % (fileinput.filename(), fileinput.filelineno(), str(detail)))
                uline = unicode(line, encoding, 'replace')
            uline = normalise(uline)
            tokens = tokenise(uline, lsd, add_glue, args.abbreviations)
            sys.stdout.write(u"\n".join(tokens).encode(encoding, 'replace'))
            sys.stdout.write(u"\n".encode(encoding))
    else:
        for input_file in args.FILES:
            if input_file == '-':
                fp = sys.stdin
                fp_desc = '<stdin>'
            else:
                fp = open(input_file, 'r')
                fp_desc = input_file
            data = fp.read()
            try:
                udata = unicode(data, encoding)
            except UnicodeDecodeError as detail:
                if not quiet:
                    sys.stderr.write("warning: %s: %s" % (fp_desc, str(detail)))
                udata = unicode(data, encoding, 'replace')
            udata = normalise(udata)
            tokens = tokenise(udata, lsd, add_glue, args.abbreviations)
            sys.stdout.write(u"\n".join(tokens).encode(encoding, 'replace'))
            sys.stdout.write(u"\n".encode(encoding))
