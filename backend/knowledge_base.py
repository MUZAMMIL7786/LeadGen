"""
Project knowledge base for the sales voice agent.

This is your product catalog. Add/edit projects here — the prompt builder
in prompts.py pulls from this automatically. Keep it in your own words;
this is your proprietary sales content, not third-party material.
"""

PROJECTS = {
    "My Home Apas": {
        "developer": "Kosaraju / My Home Group",
        "location": "Kokapet",
        "status": "Newly Launched / Under Construction",
        "structure": "6 towers, G+44 floors, 1338 luxury units spread across 13.52 Acres of land area",
        "pricing": {
            "unit_sizes": "3 & 4 BHK apartments with sizes: 2565, 2765, 3240, 3710, and 3860 sqft",
            "pricing_details": "Ask the site team for direct pricing quotes",
        },
        "clubhouse": "72000 sqft",
        "handover": "Phase 1 - July 2027, Phase 2 - August 2028",
        "highlights": [
            "81% land area is used for beautiful Green Scape",
            "Exclusive private corridors for ultimate luxury and privacy",
            "Very low density - just 98 units per acre",
            "Uninterrupted, gorgeous views of Kokapet Lake",
            "Highest Carpet Area efficiency - 72%",
            "Impressive floor-to-ceiling height of 10.8 feet",
        ],
        "best_for": "luxury buyers looking for premium 3 & 4 BHK apartments in Kokapet with abundant green space and lake views",
    },
    "Rajapushpa Provincia": {
        "developer": "Rajapushpa Properties",
        "location": "Kokapet (Narsingi)",
        "status": "Under Construction",
        "structure": "11 towers, G+39 floors, 3498 units spread across 24.27 Acres of land area",
        "pricing": {
            "unit_sizes": "2 & 3 BHK apartments with sizes: 1370, 1715, 2020, 2335, and 2660 sqft",
            "pricing_details": "₹1.42 Cr to ₹2.77 Cr (Ask the site team for direct pricing quotes)",
        },
        "clubhouse": "Grand Clubhouse featuring exclusive amenities including a Golf Course",
        "handover": "August 2028",
        "highlights": [
            "82% open area for beautiful green scapes [1.1.1]",
            "Moderate-density project with just 144 units per acre",
            "Exclusive access to a golf course for residents",
            "Extensive sports and recreational amenities",
        ],
        "best_for": "families seeking large township living with extensive open green spaces and premium amenities in Kokapet",
    },
    "Lansum Elena": {
        "developer": "Lansum Enpoint Developers",
        "location": "Kokapet (Neopolis)",
        "status": "Newly Launched / Under Construction",
        "structure": "2 towers, G+55 floors, 540 luxury units spread across 3.61 Acres of land area",
        "pricing": {
            "unit_sizes": "3 & 4 BHK apartments with sizes: 2640 to 3260 sqft",
            "pricing_details": "Starting from ₹2.9 Cr up to ₹3.65 Cr",
        },
        "clubhouse": "Premium clubhouse featuring a Rooftop Lounge, Theatre, and Infinity Pool",
        "handover": "December 2028",
        "highlights": [
            "Tall 55-floor skyscrapers offering panoramic views",
            "Exclusive Infinity Pool and EV charging stations",
            "Spacious layouts with multiple bathrooms and servant rooms",
        ],
        "best_for": "luxury buyers wanting ultra-high-rise living with rooftop amenities and a low total unit count in Neopolis, Kokapet",
    },
    "Vasavi Sarovar": {
        "developer": "Vasavi Group",
        "location": "Kukatpally",
        "status": "Under Construction",
        "structure": "11 towers, G+29 floors, 2530 units spread across 20.20 Acres of land area",
        "pricing": {
            "unit_sizes": "2, 3 & 4 BHK apartments with sizes ranging up to 4970 sqft",
            "pricing_details": "₹1.01 Cr to ₹4.22 Cr",
        },
        "clubhouse": "Expansive clubhouse with premium recreational facilities",
        "handover": "August 2028",
        "highlights": [
            "72% open area providing ample green space [1.3.1]",
            "Moderate density of 125 units per acre",
            "Comprehensive sports arena with Futsal, Net Cricket, and Tennis courts",
            "Corner flats with excellent ventilation, near Hi-Tech City",
        ],
        "best_for": "families seeking large township living with exhaustive sports amenities and spacious multi-configuration units in Kukatpally",
    },
    "ASBL Landmark": {
        "developer": "ASBL",
        "location": "Kukatpally",
        "status": "Under Construction",
        "structure": "4 towers, G+20 floors, 676 units spread across 6.6 Acres of land area",
        "pricing": {
            "unit_sizes": "3 & 4 BHK apartments with sizes: 2450 to 2860 sqft",
            "pricing_details": "₹2.6 Cr to ₹3.04 Cr (Ask the site team for direct pricing quotes)",
        },
        "clubhouse": "Fully equipped clubhouse with Swimming Pool and Gymnasium",
        "handover": "August 2029",
        "highlights": [
            "Spacious and efficient carpet area distribution [2.1.2]",
            "Close proximity to Balanagar Metro Station",
            "Premium community focused exclusively on large 3 and 4 BHK layouts",
            "Excellent connectivity to major IT and industrial transit points",
        ],
        "best_for": "joint families and luxury buyers seeking spacious, premium 3 & 4 BHK configurations with great metro connectivity",
    },
    "The Regent by Auro Realty": {
        "developer": "Auro Realty",
        "location": "Kondapur",
        "status": "Under Construction",
        "structure": "9 towers, G+39 floors, 1400 units spread across 10.38 Acres of land area",
        "pricing": {
            "unit_sizes": "3 BHK apartments with sizes: 1498 to 2191 sqft",
            "pricing_details": "₹1.41 Cr to ₹2.34 Cr",
        },
        "clubhouse": "Modern clubhouse featuring a Mini Theatre, Creche, and Swimming Pool",
        "handover": "September 2027",
        "highlights": [
            "70% open area providing a massive central green courtyard [3.1.1]",
            "Moderate density of 134 units per acre",
            "Corner flats with open views overlooking the lake",
            "Fast construction timeline by a reputed builder",
        ],
        "best_for": "IT professionals and families seeking premium 3 BHK units near Kondapur with lake views and an active lifestyle",
    },
    "Hallmark Altus": {
        "developer": "Hallmark Builders",
        "location": "Kondapur",
        "status": "Under Construction",
        "structure": "2 towers, G+50 floors, 490 units spread across 3.5 Acres of land area",
        "pricing": {
            "unit_sizes": "3 & 4 BHK apartments with sizes: 2265 to 4685 sqft",
            "pricing_details": "₹2.4 Cr to ₹5.3 Cr",
        },
        "clubhouse": "Lavish multi-level clubhouse with Gymnasium and Creche/Day Care",
        "handover": "June 2029",
        "highlights": [
            "Ultra-high-rise towers stretching up to 50 floors [4.1.1]",
            "Exclusively designed large-format 3 and 4 BHK luxury residences",
            "Close to major transport nodes like Chandanagar railway station",
            "Premium gated community with a low number of total units",
        ],
        "best_for": "buyers looking for ultra-spacious, high-altitude luxury living in Kondapur with high exclusivity",
    },
    "The Olympus": {
        "developer": "Sumadhura Group",
        "location": "Financial District",
        "status": "Under Construction",
        "structure": "Twin towers, G+44 floors, 854 units spread across a premium land parcel",
        "pricing": {
            "unit_sizes": "3 & 4 BHK apartments with sizes: 1670 to 3000 sqft",
            "pricing_details": "₹2.35 Cr to ₹3.97 Cr",
        },
        "clubhouse": "Grand G+4 floors clubhouse with co-working spaces, BBQ terrace, and rooftop swimming pool",
        "handover": "January 2027",
        "highlights": [
            "Tallest residential twin towers in Nanakramguda with sweeping skyline views [3.2.9]",
            "Centralized VRF AC system provided for each flat",
            "Dedicated space for car charging and mechanical car parking",
            "In the absolute heart of the Financial District close to major MNCs",
        ],
        "best_for": "Expat and IT professionals seeking an ultra-premium lifestyle in the heart of the Financial District",
    },
    "ASBL Broadway": {
        "developer": "ASBL (Ashoka Builders)",
        "location": "Financial District",
        "status": "Newly Launched / Under Construction",
        "structure": "3 towers, G+50 floors",
        "pricing": {
            "unit_sizes": "Exclusive 3 BHK apartments with sizes: 2340 to 2650 sqft",
            "pricing_details": "₹2.5 Cr to ₹3.2 Cr",
        },
        "clubhouse": "Expansive clubhouse equipped with Gymnasium, Creche, and Lounge",
        "handover": "May 2030",
        "highlights": [
            "50-floor skyscrapers offering panoramic views of the Financial District [3.3.6]",
            "Exclusive community consisting only of large 3 BHK layouts",
            "Meticulous spatial planning for maximum carpet area efficiency",
            "Top-tier amenities designed for a modern urban lifestyle",
        ],
        "best_for": "Long-term investors and end-users who prefer highly spacious 3 BHKs right within the Financial District IT corridor",
    }
}

# Standard qualification questions a good real-estate telecaller always asks
# before pitching, in order. The LLM is instructed to walk through these
# naturally rather than reading them as a checklist.
QUALIFICATION_FIELDS = [
    "timeline_preference",      # expected possession timeline (Phase 1 Jul-2027 vs Phase 2 Aug-2028)
    "configuration_and_size",   # e.g. 3BHK or 4BHK and preferred unit size (2565, 2765, 3240, 3710, 3860 sqft)
]
