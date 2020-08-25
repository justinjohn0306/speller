import sys

CONSONANTS = {
    'P': {'initial': 'p', 'short': 'p', 'long': 'pp', 'final': 'p'},
    'T': {'initial': 't', 'short': 't', 'long': 'tt', 'final': 't'},
    'K': {'initial': 'k', 'short': 'k', 'long': 'ck', 'final': 'c'},
    'B': {'initial': 'b', 'short': 'b', 'long': 'bb', 'final': 'b'},
    'D': {'initial': 'd', 'short': 'd', 'long': 'dd', 'final': 'd'},
    'G': {'initial': 'g', 'short': 'g', 'long': 'gg', 'final': 'g'},
    'M': {'initial': 'm', 'short': 'm', 'long': 'mm', 'final': 'm'},
    'N': {'initial': 'n', 'short': 'n', 'long': 'nn', 'final': 'n'},
    'NG': {'initial': 'ng', 'short': 'ng', 'final': 'ng'},
    'F': {'initial': 'f', 'short': 'f', 'long': 'ff', 'final': 'f'},
    'TH': {'initial': 'th', 'short': 'th', 'final': 'th'},
    'S': {'initial': 's', 'short': 's', 'long': 'ss', 'final': 'ss'},
    'SH': {'initial': 'sh', 'short': 'sh', 'long': 'sh', 'final': 'sh'},
    'HH': {'initial': 'h', 'short': 'h', 'final': 'h'},
    'V': {'initial': 'v', 'short': 'v', 'long': 'vv', 'final': 'v'},
    'DH': {'initial': 'th', 'short': 'th', 'final': 'th'},
    'Z': {'initial': 'z', 'short': 'z', 'long': 'zz', 'final': 'z'},
    'ZH': {'initial': 'zh', 'short': 'zh', 'long': 'zh', 'final': 'zh'},
    'W': {'initial': 'w', 'short': 'w', 'final': 'w'},
    'R': {'initial': 'r', 'short': 'r', 'long': 'rr', 'final': 'r'},
    'L': {'initial': 'l', 'short': 'l', 'long': 'll', 'final': 'l'},
    'Y': {'initial': 'y', 'short': 'y', 'final': 'y'},
    'CH': {'initial': 'ch', 'short': 'ch', 'long': 'ch', 'final': 'ch'},
    'JH': {'initial': 'j', 'short': 'j', 'long': 'jj', 'final': 'dge'}
    }

VOWELS = {
    'IY': {
        'initial': 'e',
        'init-checked': 'ee',
        'medial': 'e',
        'mid-checked': 'ee',
        'final': 'ee',
        'pref checked': False
        },
    'IH': {
        'initial': 'i',
        'init-checked': 'i',
        'medial': 'i',
        'mid-checked': 'i',
        'final': 'ih',
        'pref checked': False
        },
    'UH': {
        'initial': 'oo',
        'init-checked': 'oo',
        'medial': 'oo',
        'mid-checked': 'oo',
        'final': 'oo',
        'pref checked': True
        },
    'UW': {
        'initial': 'oo',
        'init-checked': 'oo',
        'medial': 'u',
        'mid-checked': 'oo',
        'final': 'oo',
        'pref checked': False
        },
    'EH': {
        'initial': 'e',
        'init-checked': 'e',
        'medial': 'e',
        'mid-checked': 'e',
        'final': 'eh',
        'pref checked': True
        },
    'AH': {
        'initial': 'a',
        'init-checked': 'u',
        'medial': 'u',
        'mid-checked': 'u',
        'final': 'a',
        'pref checked': True
        },
    'AO': {
        'initial': 'a',
        'init-checked': 'u',
        'medial': 'u',
        'mid-checked': 'u',
        'final': 'a',
        'pref checked': True
        },
    'OW': {
        'initial': 'o',
        'init-checked': 'oa',
        'medial': 'o',
        'mid-checked': 'oa',
        'final': 'o',
        'pref checked': False
        },
    'AE': {
        'initial': 'a',
        'init-checked': 'a',
        'medial': 'a',
        'mid-checked': 'a',
        'final': 'eah',
        'pref checked': True
        },
    'AA': {
        'initial': 'au',
        'init-checked': 'o',
        'medial': 'aw',
        'mid-checked': 'o',
        'final': 'ah',
        'pref checked': True
        },
    'EY': {
        'initial': 'a',
        'init-checked': 'ei',
        'medial': 'a',
        'mid-checked': 'ei',
        'final': 'ei',
        'pref checked': False
        },
    'AY': {
        'initial': 'i',
        'init-checked': 'ai',
        'medial': 'i',
        'mid-checked': 'ai',
        'final': 'ai',
        'pref checked': False
        },
    'OY': {
        'initial': 'oi',
        'init-checked': 'oi',
        'medial': 'oi',
        'mid-checked': 'oi',
        'final': 'oy',
        'pref checked': False
        },
    'AW': {
        'initial': 'ou',
        'init-checked': 'ow',
        'medial': 'ow',
        'mid-checked': 'ow',
        'final': 'ow',
        'pref checked': False
        },
    'ER': {
        'initial': 'ur',
        'init-checked': 'ur',
        'medial': 'ur',
        'mid-checked': 'ur',
        'final': 'ur',
        'pref checked': False
        }
    }

BOUNDARIES = set('-!+/#:')

PHONOLOGY = set([*CONSONANTS.keys(), *VOWELS.keys()]).union(BOUNDARIES)

SUBSTITUTIONS = {}

def thread(initial, *functions):
    nth = initial
    for fun in functions:
        nth = fun(nth)
    return nth

def parse(xsampa):
    segments = []
    for segment in xsampa.split():
        if segment in CONSONANTS:
            segments.append({'sound': segment, 'type': 'consonant'})
        elif segment[-1] in '0123':
            segments.append({
                'sound': segment[:-1],
                'type': 'vowel',
                'stress': int(segment[-1])
                })
        elif segment in VOWELS:
            segments.append({'sound': segment, 'type': 'vowel'})
        elif segment in BOUNDARIES:
            segments.append({'sound': segment, 'type': 'boundary'})
    return segments

def ends(segments): # impure
    segments[0]['position'] = 'initial'
    for i in range(1, len(segments) - 1):
        segments[i]['position'] = 'medial'
    segments[-1]['position'] = 'final'
    return segments

def spell(xsampa):
    return thread(xsampa,
            parse,
            ends
            )

if __name__ == '__main__':
    print(spell(sys.argv[1]))
