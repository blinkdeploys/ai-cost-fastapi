import re

# TODO: To transfer larger dictionary terms to fast db for CRUD capabilities

TOKEN_LIMIT = 5000

NUM_WORDS = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
            "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
            "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
            "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
            "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90
            }

MULTIPLIERS = {
                "hundred": 100,
                "thousand": 1000,
                "million": 1_000_000,
                "billion": 1_000_000_000,
                "trillion": 1_000_000_000_000
                }
# Fast regex for sequences of number-words:
WORD_NUMBER_PATTERN = re.compile(
                                r"\b(?:(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|"
                                r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|"
                                r"eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
                                r"eighty|ninety|hundred|thousand|million|billion|and|&|[-])\s*)+\b",
                                re.IGNORECASE
                                )

# stopword list similar to set used in NLTK or SpaCy
STOPWORDS = {'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
             'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
             'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
             'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
             'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
             'will', 'just', 'don', 'should', 'now', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
             'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'would', 'could', 'should',
             'might', 'must', 'shall', 'may', 'ought', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
             'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself',
             'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs',
             'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is',
             'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
             'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
             'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
             'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
             'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
             'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
             'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
             'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn',
             'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan',
             'shouldn', 'wasn', 'weren', 'won', 'wouldn'
             }

"""
Massively Expanded technical_terms Dictionary
Includes:
- AI / ML / Data
- Cloud & Infrastructure
- Security
- Software Engineering
- DevOps
- Networking
- Web Tech
- Computer Science
- Product / Business / Enterprise
"""
TECHNICAL_TERMS = {
                # --- AI / ML ---
                r'\bartificial intelligence\b': 'AI',
                r'\bmachine learning\b': 'ML',
                r'\bdeep learning\b': 'DL',
                r'\bnatural language processing\b': 'NLP',
                r'\blarge language model\b': 'LLM',
                r'\bgenerative artificial intelligence\b': 'GenAI',
                r'\bcomputer vision\b': 'CV',
                r'\breinforcement learning\b': 'RL',
                r'\bsupervised learning\b': 'SL',
                r'\bunsupervised learning\b': 'UL',
                r'\bneural network\b': 'NN',
                r'\bconvolutional neural network\b': 'CNN',
                r'\brecurrent neural network\b': 'RNN',
                r'\btransformer model\b': 'Transformer',
                r'\bgenerative adversarial network\b': 'GAN',
                r'\bgradient descent\b': 'GD',
                r'\bprincipal component analysis\b': 'PCA',
                r'\bexploratory data analysis\b': 'EDA',
                r'\bnatural language understanding\b': 'NLU',
                r'\bnatural language generation\b': 'NLG',

                # --- Data Engineering & Databases ---
                r'\bstructured query language\b': 'SQL',
                r'\bextract transform load\b': 'ETL',
                r'\bextract load transform\b': 'ELT',
                r'\bonline analytical processing\b': 'OLAP',
                r'\bonline transaction processing\b': 'OLTP',
                r'\brelational database management system\b': 'RDBMS',
                r'\bdata management platform\b': 'DMP',
                r'\bdata warehouse\b': 'DW',
                r'\bdata lakehouse\b': 'DLH',
                r'\bapplication performance monitoring\b': 'APM',

                # --- Software Engineering ---
                r'\bapplication programming interface\b': 'API',
                r'\brepresentational state transfer\b': 'REST',
                r'\bgraph query language\b': 'GraphQL',
                r'\bobject oriented programming\b': 'OOP',
                r'\bcomponent based architecture\b': 'CBA',
                r'\btest driven development\b': 'TDD',
                r'\bbehavior driven development\b': 'BDD',
                r'\bcontinuous integration\b': 'CI',
                r'\bcontinuous delivery\b': 'CD',
                r'\bsoftware development kit\b': 'SDK',
                r'\bintegrated development environment\b': 'IDE',
                r'\bcontent management system\b': 'CMS',
                r'\bsoftware as a service\b': 'SaaS',
                r'\bplatform as a service\b': 'PaaS',
                r'\binfrastructure as a service\b': 'IaaS',
                r'\buser interface\b': 'UI',
                r'\buser experience\b': 'UX',
                r'\bcommand line interface\b': 'CLI',
                r'\bgraphical user interface\b': 'GUI',
                r'\bversion control system\b': 'VCS',

                # --- Web Development ---
                r'\bhypertext markup language\b': 'HTML',
                r'\bcascading style sheets\b': 'CSS',
                r'\bjavascript object notation\b': 'JSON',
                r'\bweb application firewall\b': 'WAF',
                r'\bcontent delivery network\b': 'CDN',
                r'\bsearch engine optimization\b': 'SEO',
                r'\bsearch engine marketing\b': 'SEM',

                # --- Networking ---
                r'\bhypertext transfer protocol\b': 'HTTP',
                r'\bfile transfer protocol\b': 'FTP',
                r'\buser datagram protocol\b': 'UDP',
                r'\btransmission control protocol\b': 'TCP',
                r'\bvirtual private network\b': 'VPN',
                r'\bwireless local area network\b': 'WLAN',
                r'\bvirtual local area network\b': 'VLAN',
                r'\bdomain name system\b': 'DNS',
                r'\binternet protocol\b': 'IP',

                # --- Cloud / DevOps ---
                r'\bamazon web services\b': 'AWS',
                r'\bmicrosoft azure\b': 'Azure',
                r'\bgoogle cloud platform\b': 'GCP',
                r'\binfrastructure as code\b': 'IaC',
                r'\bidentity and access management\b': 'IAM',
                r'\bplatform engineering\b': 'Platform Eng',
                r'\bcloud service provider\b': 'CSP',
                r'\bservice level agreement\b': 'SLA',
                r'\bservice level objective\b': 'SLO',
                r'\bservice level indicator\b': 'SLI',
                r'\bcontinuous deployment\b': 'CD',
                r'\bcontainer orchestration\b': 'CO',
                r'\bsite reliability engineering\b': 'SRE',

                # --- Security ---
                r'\bmulti factor authentication\b': 'MFA',
                r'\bsingle sign on\b': 'SSO',
                r'\bpublic key infrastructure\b': 'PKI',
                r'\bpersonally identifiable information\b': 'PII',
                r'\bgeneral data protection regulation\b': 'GDPR',
                r'\bsecure shell\b': 'SSH',
                r'\btransport layer security\b': 'TLS',
                r'\bcomputational integrity protection\b': 'CIP',
                r'\bsecurity operations center\b': 'SOC',
                r'\bintrusion detection system\b': 'IDS',
                r'\bintrusion prevention system\b': 'IPS',

                # --- Business / Product / Enterprise ---
                r'\bkey performance indicator\b': 'KPI',
                r'\breturn on investment\b': 'ROI',
                r'\bcost of goods sold\b': 'COGS',
                r'\benterprise resource planning\b': 'ERP',
                r'\bcustomer relationship management\b': 'CRM',
                r'\bproduct requirements document\b': 'PRD',
                r'\bstandard operating procedure\b': 'SOP',
                r'\bminimum viable product\b': 'MVP',
                r'\bunique selling proposition\b': 'USP',
                r'\btotal cost of ownership\b': 'TCO',

                # --- CS Fundamentals ---
                r'\bcentral processing unit\b': 'CPU',
                r'\bgraphics processing unit\b': 'GPU',
                r'\brandom access memory\b': 'RAM',
                r'\bread only memory\b': 'ROM',
                r'\bsolid state drive\b': 'SSD',
                r'\bapplication specific integrated circuit\b': 'ASIC',
                r'\bfield programmable gate array\b': 'FPGA',

                # --- Misc Popular Tech Terms ---
                r'\bvirtual reality\b': 'VR',
                r'\baugmented reality\b': 'AR',
                r'\bmixed reality\b': 'MR',
                r'\binternet of things\b': 'IoT',
                r'\bedge computing\b': 'Edge',
                r'\bquantum computing\b': 'QC',
                }


ABBREVIATIONS = {
                # --- General Tech / Software ---
                r'\binformation\b': 'info',
                r'\bapplication\b': 'app',
                r'\bapplications\b': 'apps',
                r'\bconfiguration\b': 'config',
                r'\bconfigurations\b': 'configs',
                r'\bdocumentation\b': 'docs',
                r'\bdocumentations\b': 'docs',
                r'\bservice\b': 'svc',
                r'\bservices\b': 'svcs',
                r'\bparameter\b': 'param',
                r'\bparameters\b': 'params',
                r'\bidentifier\b': 'ID',
                r'\bidentifiers\b': 'IDs',
                r'\bvariable\b': 'var',
                r'\bvariables\b': 'vars',
                r'\bfunction\b': 'fn',
                r'\bfunctions\b': 'fns',
                r'\bperformance\b': 'perf',

                # --- Engineering Terms ---
                r'\bdevelopment\b': 'dev',
                r'\bproduction\b': 'prod',
                r'\bstaging\b': 'stage',
                r'\benvironment\b': 'env',
                r'\benvironments\b': 'envs',
                r'\bintegration\b': 'int',
                r'\bimplementation\b': 'impl',
                r'\barchitecture\b': 'arch',
                r'\barchitectural\b': 'arch',

                # --- Infrastructure / DevOps ---
                r'\bdatabase\b': 'DB',
                r'\bdatabases\b': 'DBs',
                r'\brepository\b': 'repo',
                r'\brepositories\b': 'repos',
                r'\binfrastructure\b': 'infra',
                r'\bvirtual machine\b': 'VM',
                r'\bvirtual machines\b': 'VMs',
                r'\bcontainer\b': 'ctr',
                r'\bcontainers\b': 'ctrs',
                r'\bdeployment\b': 'deploy',
                r'\bdeployments\b': 'deploys',

                # --- Cloud / SaaS ---
                r'\bplatform\b': 'plt',
                r'\bplatforms\b': 'plts',
                r'\baccount\b': 'acct',
                r'\baccounts\b': 'accts',
                r'\bsubscription\b': 'sub',
                r'\bsubscriptions\b': 'subs',
                r'\borganization\b': 'org',
                r'\borganizations\b': 'orgs',

                # --- People / Roles ---
                r'\badministrator\b': 'admin',
                r'\badministration\b': 'admin',
                r'\bmanager\b': 'mgr',
                r'\bmanagers\b': 'mgrs',
                r'\bmanagement\b': 'mgmt',
                r'\bengineer\b': 'eng',
                r'\bengineers\b': 'engs',
                r'\bengineering\b': 'eng',

                # --- Business / Product ---
                r'\bmaximum\b': 'max',
                r'\bminimum\b': 'min',
                r'\bapproximate\b': 'approx',
                r'\bapproximately\b': 'approx',
                r'\bspecification\b': 'spec',
                r'\bspecifications\b': 'specs',
                r'\brequirement\b': 'req',
                r'\brequirements\b': 'reqs',
                r'\bestimate\b': 'est',
                r'\bestimates\b': 'ests',
                r'\bestimation\b': 'est',

                # --- Misc useful tech contractions ---
                r'\bconfiguration management\b': 'config mgmt',
                r'\bcontent management system\b': 'CMS',
                r'\boperating system\b': 'OS',
                r'\boperating systems\b': 'OSes',
                }


FILLER_REPLACEMENTS = {r'\bit is important to note that\b': '',
                       r'\bit should be noted that\b': '',
                       r'\bplease note that\b': '',
                       r'\bit goes without saying\b': '',
                       r'\bneedless to say\b': '',
                       r'\bas you may already know\b': '',
                       r'\bas you know\b': '',
                       r'\bas you can see\b': '',
                       r'\bfor what it\'s worth\b': '',
                       r'\bin my opinion\b': '',
                       r'\bin my personal opinion\b': '',
                       r'\bin my honest opinion\b': '',
                       r'\bi believe that\b': '',
                       r'\bi think that\b': '',
                       r'\bi feel that\b': '',
                       r'\bi would argue that\b': '',
                       r'\bto be honest\b': '',
                       r'\bto tell the truth\b': '',
                       r'\bquite frankly\b': '',
                       r'\bfrankly\b': '',
                       r'\bbasically\b': '',
                       r'\bliterally\b': '',
                       r'\bactually\b': '',
                       r'\breally\b': '',
                       r'\bvery\b': '',
                       r'\bjust\b': '',
                       r'\bsimply\b': '',
                       r'\btruly\b': '',
                       r'\bcertainly\b': '',
                       r'\bdefinitely\b': '',
                       r'\babsolutely\b': '',

                       # Replace with concise alternatives
                       r'\bin order to\b': 'to',
                       r'\bdue to the fact that\b': 'because',
                       r'\bfor the reason that\b': 'because',
                       r'\bfor the purpose of\b': 'for',
                       r'\bin light of the fact that\b': 'because',
                       r'\bdespite the fact that\b': 'although',
                       r'\bwith the exception of\b': 'except',
                       r'\bat this point in time\b': 'now',
                       r'\bat the present time\b': 'now',
                       r'\bin the near future\b': 'soon',
                       r'\bat the end of the day\b': 'ultimately',
                       r'\bfor all intents and purposes\b': 'essentially',
                       r'\bas a matter of fact\b': 'in fact',
                       r'\bwith regard to\b': 'regarding',
                       r'\bwith respect to\b': 'regarding',
                       r'\bin connection with\b': 'regarding',
                       r'\bon a daily basis\b': 'daily',
                       r'\bon a regular basis\b': 'regularly',
                       r'\bon an annual basis\b': 'annually',
                       r'\bdue to the fact\b': 'because',
                       r'\bthe vast majority of\b': 'most',
                       r'\ba large number of\b': 'many',
                       r'\ba small number of\b': 'few',
                       r'\bin the event that\b': 'if',
                       r'\bin the event of\b': 'if',
                       r'\bfor the most part\b': 'mostly',
                       r'\bto a certain extent\b': 'partially',
                       r'\bto some extent\b': 'partially',
                       r'\bit seems that\b': '',
                       r'\bit appears that\b': '',
                       r'\bit is possible that\b': 'maybe',
                       r'\bit is likely that\b': 'likely',
                       r'\bit is clear that\b': '',
                       r'\bit is evident that\b': '',
                       r'\bin terms of\b': '',
                       r'\bfrom a .* perspective\b': '',
                       }

CONTRACTIONS = {
                r'\bdo not\b': "don't",
                r'\bdoes not\b': "doesn't",
                r'\bdid not\b': "didn't",
                r'\bcannot\b': "can't",
                r'\bwill not\b': "won't",
                r'\bwould not\b': "wouldn't",
                r'\bshould not\b': "shouldn't",
                r'\bcould not\b': "couldn't",
                r'\bis not\b': "isn't",
                r'\bare not\b': "aren't",
                r'\bwas not\b': "wasn't",
                r'\bwere not\b': "weren't",
                r'\bhas not\b': "hasn't",
                r'\bhave not\b': "haven't",
                r'\bhad not\b': "hadn't",
                r'\bI am\b': "I'm",
                r'\byou are\b': "you're",
                r'\bwe are\b': "we're",
                r'\bthey are\b': "they're",
                r'\bit is\b': "it's",
                r'\bI will\b': "I'll",
                r'\byou will\b': "you'll",
                r'\bwe will\b': "we'll",
                r'\bthey will\b': "they'll",
                }
    

REDUNDANT_PAIRS = {
                    r'\beach and every\b': 'each',
                    r'\bfirst and foremost\b': 'first',
                    r'\bfull and complete\b': 'complete',
                    r'\bnull and void\b': 'void',
                    r'\bcease and desist\b': 'stop',
                    r'\bvarious and sundry\b': 'various',
                    r'\bways and means\b': 'ways',
                    r'\baid and abet\b': 'aid',
                    r'\bpeace and quiet\b': 'peace',
                    r'\bsafe and sound\b': 'safe',
                    r'\bsick and tired\b': 'tired',
                    r'\bhopes and dreams\b': 'hopes',
                    r'\bterms and conditions\b': 'terms',
                    r'\brules and regulations\b': 'rules',
                    r'\bany and all\b': 'all',
                    r'\bbasic and fundamental\b': 'basic',
                    r'\btrue and accurate\b': 'accurate',
                    r'\bfinal and complete\b': 'complete',
                    r'\bbold and daring\b': 'bold',
                    r'\bfree and clear\b': 'clear',
                    r'\bfull and entire\b': 'entire',
                    r'\bfinal and conclusive\b': 'final',
                    r'\bpart and parcel\b': 'part',
                    r'\bfit and proper\b': 'proper',
                    r'\bforce and effect\b': 'effect',
                    r'\bterms and particulars\b': 'terms',
                    r'\bany and every\b': 'every',
                    r'\bend result\b': 'result',
                    r'\badvance planning\b': 'planning',
                    r'\bpast history\b': 'history',
                    r'\bunexpected surprise\b': 'surprise',
                    r'\bbasic necessities\b': 'necessities',
                    r'\bfuture plans\b': 'plans',
                    }


# Current LLM Pricing (November 2025) - per 1M tokens
CURRENT_LLM_PRICING = {
    "OpenAI": {
        "GPT-5": {"input": 3.00, "output": 12.00, "context": 200000},
        "GPT-4.5": {"input": 75.00, "output": 150.00, "context": 128000},
        "GPT-4o": {"input": 5.00, "output": 20.00, "context": 128000},
        "GPT-4.1": {"input": 12.00, "output": 48.00, "context": 128000},
        "GPT-3.5-Turbo": {"input": 3.00, "output": 6.00, "context": 16000},
        "o3": {"input": 10.00, "output": 40.00, "context": 128000},
        "o4-mini": {"input": 1.00, "output": 4.00, "context": 128000},
    },
    "Anthropic": {
        "Claude-Opus-4.1": {"input": 15.00, "output": 75.00, "context": 200000},
        "Claude-Sonnet-4.5": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Sonnet-4": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Sonnet-3.7": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Sonnet-3.5": {"input": 3.00, "output": 15.00, "context": 200000},
        "Claude-Haiku-4.5": {"input": 0.80, "output": 4.00, "context": 200000},
        "Claude-Haiku-3.5": {"input": 0.80, "output": 4.00, "context": 200000},
        "Claude-Haiku-3": {"input": 0.25, "output": 1.25, "context": 200000},
    },
    "Google": {
        "Gemini-2.5-Pro": {"input": 2.50, "output": 10.00, "context": 1000000},
        "Gemini-2.5-Flash": {"input": 0.15, "output": 0.60, "context": 1000000},
        "Gemini-1.5-Pro-128k": {"input": 1.25, "output": 5.00, "context": 128000},
        "Gemini-1.5-Pro-1M": {"input": 2.50, "output": 10.00, "context": 1000000},
        "Gemini-1.5-Flash": {"input": 0.075, "output": 0.30, "context": 1000000},
    },
    "xAI": {
        "Grok-3": {"input": 2.00, "output": 10.00, "context": 128000},
        "Grok-4": {"input": 5.00, "output": 15.00, "context": 128000},
        "Grok-Mini": {"input": 0.50, "output": 1.50, "context": 32000},
    },
    "DeepSeek": {
        "DeepSeek-V3.2": {"input": 0.27, "output": 1.10, "context": 128000},
        "DeepSeek-Chat": {"input": 0.14, "output": 0.28, "context": 64000},
    },
    "Mistral": {
        "Mistral-Large": {"input": 2.00, "output": 6.00, "context": 128000},
        "Mistral-Medium": {"input": 2.70, "output": 8.10, "context": 32000},
    },
    "Meta": {
        "Llama-3.1-405B": {"input": 0.80, "output": 0.80, "context": 128000},
        "Llama-3.1-70B": {"input": 0.35, "output": 0.40, "context": 128000},
        "Llama-4-70B": {"input": 0.50, "output": 0.60, "context": 200000},
    }
}

# pre-compile the pattrerns
_COMPILED_FILLER_PATTERNS = [(re.compile(pattern, flags=re.IGNORECASE), replacement)
                             for pattern, replacement in FILLER_REPLACEMENTS.items()
                             ]

_COMPILED_REDUNDANT_PAIRS = [(re.compile(pattern, flags=re.IGNORECASE), replacement)
                             for pattern, replacement in REDUNDANT_PAIRS.items()
                             ]

_COMPILED_ABBREVIATIONS = [(re.compile(pattern, flags=re.IGNORECASE), replacement)
                           for pattern, replacement in ABBREVIATIONS.items()
                           ]
_COMPILED_CONTRACTIONS = [(re.compile(pattern, flags=re.IGNORECASE), replacement)
                           for pattern, replacement in CONTRACTIONS.items()
                           ]
