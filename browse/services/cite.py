"""Functions to make citation strings."""


from browse.domain.metadata import DocMetadata
from typing import List

from arxiv.util.authors import parse_author_affil_utf


def arxiv_bibtex(docm: DocMetadata) -> str:
    '''Returns bibtex citation for the paper.'''
    published = docm.get_datetime_of_version(None)
    year = str(published.year) if published else 'unknown'

    title = _normalize_whitespace(docm.title)
    pauths = parse_author_affil_utf(docm.authors.raw)
    auths = _fmt_author_list(pauths)

    pc = docm.primary_category if docm.primary_category else 'unknown'
        
    return "@misc{" + txt_id(docm, pauths, year) + ",\n" \
        "      title={" + title + "}, \n" \
        "      author={" + auths + "},\n" \
        "      year={" + year + "},\n" \
        "      eprint={" + docm.arxiv_id + "},\n" \
        "      archivePrefix={arXiv},\n" \
        "      primaryClass={" + str(pc) + "}\n" \
        "}"


def _normalize_whitespace(txt: str) -> str:
    return ' '.join(txt.split()) if str else ''


def _fmt_author_list(pauths: List[List[str]]) -> str:
    authors = [(f'{au[1]} ' if (len(au) > 1 and au[1]) else '')
               + f'{au[0]}'
               + (f' {au[2]} au2' if (len(au) > 2 and au[2]) else '')
               for au in pauths]
    return ' and '.join(authors)


def chars_only(data: str) -> str:
    '''just alphanum from data'''
    return ''.join([cc for cc in data if cc.isalnum()])


def txt_id(docm: DocMetadata, auths: List[str], year: str) -> str:
    '''Create an id for the bibtex entry ex abadi2016tensorflow'''

    try:
        auth = auths[0][0]
    except Exception:
        auth = 'unknown'

    try:
        title_word = next((word for word in docm.title.split(' ')
                           if word.lower() not in STOPWORDS))
    except Exception:
        title_word = 'unknown'

    txt_year = year if year else 'unknown'
    return chars_only(f'{auth}{txt_year}{title_word}').lower()


STOPWORDS = frozenset([
    'a', 'about', 'above', 'above', 'across', 'after',
    'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along',
    'already', 'also', 'although', 'always', 'am', 'among', 'amongst',
    'amoungst', 'amount',  'an', 'and', 'another', 'any',
    'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around',
    'as',  'at', 'back', 'be', 'became', 'because', 'become', 'becomes',
    'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below',
    'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but',
    'by', 'call', 'can', 'cannot', 'cant', 'co', 'con', 'could', 'couldnt',
    'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during',
    'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty',
    'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything',
    'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire',
    'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four',
    'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has',
    'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby',
    'herein', 'hereupon', 'hers', 'herself', 'him', 'himself', 'his', 'how',
    'however', 'hundred', 'ie', 'if', 'in', 'inc', 'indeed', 'interest',
    'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 'latter', 'latterly',
    'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might',
    'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much',
    'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
    'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor',
    'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once',
    'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours',
    'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please',
    'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems',
    'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere',
    'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something',
    'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take',
    'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then',
    'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein',
    'thereupon', 'these', 'they', 'thickv', 'thin', 'third', 'this', 'those',
    'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to',
    'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
    'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we',
    'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where',
    'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever',
    'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom',
    'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet',
    'you', 'your', 'yours', 'yourself', 'yourselves', 'the'])
