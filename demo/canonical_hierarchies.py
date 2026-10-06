"""
demo/canonical_hierarchies.py
=============================
Canonical Hierarchical Prepending Trees (Chapter 3 §3.2.2) for Landmark
Jurisprudential Cases in Davao City Ordinance Conflict Detection.

Provides structured nested representations (Enactment -> Section -> Subsection ->
Item -> Sub-item) with full operative texts for interactive Reddit-style threads.
"""

CANONICAL_HIERARCHIES = {
    "DAVAO-TIER3-01": {
        "statute_tree": {
            "label": "Presidential Decree No. 1144",
            "title": "CREATING THE FERTILIZER AND PESTICIDE AUTHORITY AND ABOLISHING THE FERTILIZER INDUSTRY AUTHORITY",
            "text": "",
            "children": [
                {
                    "label": "Section 6",
                    "title": "Powers and Functions",
                    "text": "The Fertilizer and Pesticide Authority shall have jurisdiction over all fertilizers, pesticides, and other agricultural chemicals, and shall regulate and monitor their importation, manufacture, formulation, sale, distribution, delivery, transport, storage, handling and use in order to assure agricultural productivity and environmental safety.",
                    "children": []
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 0309-07",
            "title": "AN ORDINANCE BANNING AERIAL SPRAYING IN DAVAO CITY",
            "text": "",
            "children": [
                {
                    "label": "Section 5",
                    "title": "Ban on Aerial Spraying",
                    "text": "Aerial spraying shall be strictly prohibited in all agricultural activities in Davao City after a three (3) month transition period from the effectivity of this Ordinance.",
                    "children": []
                },
                {
                    "label": "Section 6",
                    "title": "Buffer Zone",
                    "text": "All agricultural entities must maintain a mandatory thirty (30) meter buffer zone within the boundaries of their plantations.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-02": {
        "statute_tree": {
            "label": "Republic Act No. 7160",
            "title": "AN ACT PROVIDING FOR A LOCAL GOVERNMENT CODE OF 1991",
            "text": "",
            "children": [
                {
                    "label": "Section 458",
                    "title": "Powers, Duties, Functions and Compensation",
                    "text": "",
                    "children": [
                        {
                            "label": "(a)",
                            "title": "",
                            "text": "The sangguniang panlungsod, as the legislative body of the city, shall enact ordinances, approve resolutions and appropriate funds for the general welfare of the city and its inhabitants pursuant to Section 16 of this Code and in the proper exercise of the corporate powers of the city as provided for under Section 22 of this Code, and shall:",
                            "children": [
                                {
                                    "label": "(4)",
                                    "title": "",
                                    "text": "Regulate activities relative to the use of land, buildings and structures within the city in order to promote the general welfare and for said purpose shall:",
                                    "children": [
                                        {
                                            "label": "(iv)",
                                            "title": "",
                                            "text": "Regulate the display of and prescribe the physical setback of signs, signboards, and commercial billboards along public roads and highways within the territorial jurisdiction of the city.",
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 092-2000",
            "title": "AN ORDINANCE REGULATING THE CONSTRUCTION, DISPLAY AND MAINTENANCE OF BILLBOARDS, SIGNBOARDS AND ADVERTISEMENTS",
            "text": "",
            "children": [
                {
                    "label": "Section 7",
                    "title": "Billboards and Signages",
                    "text": "Outdoor advertising signs and commercial billboards are strictly prohibited in residential zones. Free-standing billboards along public highways must maintain an unobstructed 150-meter line of sight and must be located at least 10 meters away from property lines abutting the road right-of-way.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-03": {
        "statute_tree": {
            "label": "Republic Act No. 7160",
            "title": "AN ACT PROVIDING FOR A LOCAL GOVERNMENT CODE OF 1991",
            "text": "",
            "children": [
                {
                    "label": "Book II",
                    "title": "Local Taxation and Fiscal Matters",
                    "text": "",
                    "children": [
                        {
                            "label": "Title One",
                            "title": "Local Government Taxation",
                            "text": "",
                            "children": [
                                {
                                    "label": "Chapter II",
                                    "title": "Tax on Business",
                                    "text": "",
                                    "children": [
                                        {
                                            "label": "Section 143",
                                            "title": "Specific Taxes",
                                            "text": "The municipality or city may impose taxes on businesses, including:",
                                            "children": [
                                                {
                                                    "label": "(f)",
                                                    "title": "",
                                                    "text": "On banks and other financial institutions, non-bank financial intermediaries, lending investors, and finance companies authorized and regulated by the Bangko Sentral ng Pilipinas.",
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 158-05",
            "title": "DAVAO CITY REVENUE CODE OF 2005",
            "text": "",
            "children": [
                {
                    "label": "Section 135",
                    "title": "Tax on Financial Institutions and Holding Corporations",
                    "text": "Imposes local business taxes on banks, banking institutions, and holding entities receiving dividend income and investment interest, categorizing corporate holding firms as non-bank financial intermediaries.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-04": {
        "statute_tree": {
            "label": "Republic Act No. 7160",
            "title": "AN ACT PROVIDING FOR A LOCAL GOVERNMENT CODE OF 1991",
            "text": "",
            "children": [
                {
                    "label": "Book II",
                    "title": "Local Taxation and Fiscal Matters",
                    "text": "",
                    "children": [
                        {
                            "label": "Title One",
                            "title": "Local Government Taxation",
                            "text": "",
                            "children": [
                                {
                                    "label": "Chapter VI",
                                    "title": "Administrative Provisions",
                                    "text": "",
                                    "children": [
                                        {
                                            "label": "Section 195",
                                            "title": "Protest of Assessment",
                                            "text": "When the local treasurer finds that correct taxes have not been paid, he shall issue an assessment. The taxpayer may file a written protest with the local treasurer within sixty (60) days from receipt of the notice without being required to pay the assessment under protest.",
                                            "children": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 158-05",
            "title": "DAVAO CITY REVENUE CODE",
            "text": "",
            "children": [
                {
                    "label": "Section 423",
                    "title": "Payment Under Protest",
                    "text": "No protest against an assessment shall be entertained unless the taxpayer first pays under protest the tax assessed, stating the legal grounds within thirty (30) days from payment.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-05": {
        "statute_tree": {
            "label": "Republic Act No. 7160",
            "title": "AN ACT PROVIDING FOR A LOCAL GOVERNMENT CODE OF 1991",
            "text": "",
            "children": [
                {
                    "label": "Book II",
                    "title": "Local Taxation and Fiscal Matters",
                    "text": "",
                    "children": [
                        {
                            "label": "Title Two",
                            "title": "Real Property Taxation",
                            "text": "",
                            "children": [
                                {
                                    "label": "Section 193",
                                    "title": "Withdrawal of Tax Exemption Privileges",
                                    "text": "Unless otherwise provided in this Code, tax exemptions or the incentive privileges granted to or presently enjoyed by all persons, whether natural or juridical, including government-owned or controlled corporations, are hereby withdrawn.",
                                    "children": []
                                },
                                {
                                    "label": "Section 234",
                                    "title": "Exemptions from Real Property Tax",
                                    "text": "The following are exempted from payment of the real property tax: (a) Real property owned by the Republic of the Philippines or any of its political subdivisions except when the beneficial use thereof has been granted, for consideration or otherwise, to a taxable person.",
                                    "children": []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "ordinance_tree": {
            "label": "City of Davao Assessment Warrant",
            "title": "DAVAO CITY REAL PROPERTY TAX ASSESSMENT ON GSIS",
            "text": "",
            "children": [
                {
                    "label": "Assessment Mandate",
                    "title": "Municipal Real Property Levy",
                    "text": "Notices of assessment and warrants of levy imposing municipal real property taxes upon GSIS properties located in Matina and Ulas, Davao City, for outstanding municipal tax liabilities.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-06": {
        "statute_tree": {
            "label": "Republic Act No. 7942",
            "title": "PHILIPPINE MINING ACT OF 1995",
            "text": "",
            "children": [
                {
                    "label": "Chapter II",
                    "title": "Government Management",
                    "text": "",
                    "children": [
                        {
                            "label": "Section 4",
                            "title": "Ownership of Mineral Resources",
                            "text": "All mineral resources in public or private lands within the territory and exclusive economic zone of the Republic of the Philippines are owned by the State.",
                            "children": []
                        },
                        {
                            "label": "Section 27",
                            "title": "Concession Mandate",
                            "text": "Exploration and mining operations authorized under national mineral agreements shall be governed by national concessions issued by the national government.",
                            "children": []
                        }
                    ]
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 0310-07 & 2015 Mining Ban Ordinance",
            "title": "TOTAL BAN ON MINING OPERATIONS IN DAVAO CITY",
            "text": "",
            "children": [
                {
                    "label": "Section 2",
                    "title": "Total Mining Ban",
                    "text": "No mining operations of any nature, whether large-scale or small-scale, shall be permitted anywhere within the territorial jurisdiction of Davao City. The City Mayor shall refuse to issue business permits or Mayor's clearances to any entity holding national mineral agreements (MPSAs) from the national government.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-07": {
        "statute_tree": {
            "label": "Republic Act No. 7160 & Republic Act No. 9211",
            "title": "LOCAL GOVERNMENT CODE OF 1991 & TOBACCO REGULATION ACT OF 2003",
            "text": "",
            "children": [
                {
                    "label": "Section 16 (RA 7160)",
                    "title": "General Welfare Clause",
                    "text": "Every local government unit shall exercise powers essential to the promotion of the general welfare, the maintenance of public health and safety, and the protection of the inhabitants from harmful environmental exposure.",
                    "children": []
                },
                {
                    "label": "Section 5 (RA 9211)",
                    "title": "Smoking in Public Places",
                    "text": "Smoking shall be absolutely prohibited in designated public places throughout the national territory.",
                    "children": []
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 0367-12",
            "title": "THE NEW COMPREHENSIVE ANTI-SMOKING ORDINANCE OF DAVAO CITY",
            "text": "",
            "children": [
                {
                    "label": "Section 4",
                    "title": "Prohibition of Smoking",
                    "text": "Smoking is prohibited in all public conveyances and enclosed public spaces.",
                    "children": []
                },
                {
                    "label": "Section 5",
                    "title": "Designated Smoking Areas (DSA) Setbacks",
                    "text": "Designated smoking areas must be open outdoor spaces situated not less than ten (10) meters away from building entrances, exits, and windows, exceeding national statutory minimums.",
                    "children": []
                }
            ]
        }
    },

    "DAVAO-TIER3-08": {
        "statute_tree": {
            "label": "Republic Act No. 4136 & Joint JAO 2018-01",
            "title": "LAND TRANSPORTATION AND TRAFFIC CODE & DILG-DOTr-DPWH JOINT ORDER",
            "text": "",
            "children": [
                {
                    "label": "Section 38 & JAO 2018-01",
                    "title": "Speed Limits on Local Roads",
                    "text": "Local government units are authorized to classify roads within their territorial boundaries and prescribe appropriate maximum and minimum speed limits consistent with public safety, geometric road conditions, and pedestrian traffic.",
                    "children": []
                }
            ]
        },
        "ordinance_tree": {
            "label": "Ordinance No. 0270-23",
            "title": "DAVAO CITY SPEED LIMIT ORDINANCE",
            "text": "",
            "children": [
                {
                    "label": "Section 4",
                    "title": "Speed Limit Classification",
                    "text": "Classifies city roads into Open Roads (80 kph private / 50 kph trucks), Through Streets (40 kph / 30 kph), City Streets (30 kph), and Crowded Residential Streets (20 kph), enforced by calibrated radar speed cameras.",
                    "children": []
                }
            ]
        }
    },

    "SC-PHIL-09": {
        "statute_tree": {
            "label": "Presidential Decree No. 1869 & Republic Act No. 7160",
            "title": "THE PAGCOR CHARTER & LOCAL GOVERNMENT CODE OF 1991",
            "text": "",
            "children": [
                {
                    "label": "Section 1 (PD 1869)",
                    "title": "PAGCOR Franchise Mandate",
                    "text": "PAGCOR is hereby authorized and empowered to establish, operate, and maintain gambling casinos, clubs, and other recreational facilities within the territorial jurisdiction of the Philippines to generate government revenues.",
                    "children": []
                },
                {
                    "label": "Section 5(a) (RA 7160)",
                    "title": "Rules of Interpretation",
                    "text": "Any provision on a power of a local government unit shall be liberally interpreted in its favor, and in case of doubt, any question thereon shall be resolved in favor of devolution of powers and of the lower local government unit.",
                    "children": []
                }
            ]
        },
        "ordinance_tree": {
            "label": "Cagayan de Oro Ordinance No. 3353 & 3375-93",
            "title": "PROHIBITION OF CASINOS IN CAGAYAN DE ORO",
            "text": "",
            "children": [
                {
                    "label": "Section 1",
                    "title": "Prohibition of Casinos",
                    "text": "The opening, establishment, and operation of casinos and all forms of gambling are strictly prohibited and banned within the territorial jurisdiction of the City of Cagayan de Oro.",
                    "children": []
                }
            ]
        }
    },

    "SC-PHIL-10": {
        "statute_tree": {
            "label": "1987 Philippine Constitution",
            "title": "THE CONSTITUTION OF THE REPUBLIC OF THE PHILIPPINES",
            "text": "",
            "children": [
                {
                    "label": "Article III, Section 1",
                    "title": "Bill of Rights (Due Process and Equal Protection Clause)",
                    "text": "No person shall be deprived of life, liberty, or property without due process of law, nor shall any person be denied the equal protection of the laws.",
                    "children": []
                }
            ]
        },
        "ordinance_tree": {
            "label": "Manila Ordinance No. 7783",
            "title": "PROHIBITION OF CERTAIN BUSINESSES IN ERMITA-MALATE",
            "text": "",
            "children": [
                {
                    "label": "Section 1",
                    "title": "Closure of Hospitality Establishments",
                    "text": "Prohibits the establishment or operation of motels, inns, and karaoke bars in the Ermita-Malate district, ordering their permanent closure or relocation within three (3) months without just compensation.",
                    "children": []
                }
            ]
        }
    },

    "SC-PHIL-11": {
        "statute_tree": {
            "label": "Executive Order No. 205 & Executive Order No. 546",
            "title": "NATIONAL TELECOMMUNICATIONS COMMISSION REGULATORY MANDATE",
            "text": "",
            "children": [
                {
                    "label": "Section 2 & Section 15",
                    "title": "NTC Exclusive Regulatory Authority",
                    "text": "The National Telecommunications Commission shall have exclusive jurisdiction and authority over the regulation, supervision, rate-fixing, and licensing of cable television systems throughout the Philippines.",
                    "children": []
                }
            ]
        },
        "ordinance_tree": {
            "label": "Batangas SP Resolution No. 210, Series of 1993",
            "title": "REGULATION OF CATV SUBSCRIBER RATES",
            "text": "",
            "children": [
                {
                    "label": "Section 2",
                    "title": "Cable Rate Regulation",
                    "text": "The Sangguniang Panlungsod assumes authority to fix, regulate, and adjust subscriber rates and channel programming charges for commercial cable television services.",
                    "children": []
                }
            ]
        }
    }
}
