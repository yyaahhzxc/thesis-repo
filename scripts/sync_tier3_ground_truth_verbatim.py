import json

updated_records = []
with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        c = json.loads(line)
        cid = c.get("case_id")
        if cid == "DAVAO-TIER3-01":
            c["ordinance_no"] = "Ordinance No. 0309-07"
            c["challenged_text"] = "SECTION 5. BAN OF AERIAL SPRAYING - A ban on aerial spraying shall be strictly enforced in the territorial jurisdiction of Davao City three (3) months after the effectivity of this Ordinance."
        elif cid == "DAVAO-TIER3-05":
            c["ordinance_no"] = "Ordinance No. 0158-05 §8"
            c["title"] = "THE 2005 REVENUE CODE OF THE CITY OF DAVAO (REAL PROPERTY TAXATION & WITHDRAWAL OF GOCC EXEMPTIONS)"
            c["challenged_text"] = "Section 8. Exemptions to the Imposition. Except as provided herein and pursuant to Section 234 of the Local Government Code, any exemption from payment of real property tax previously granted to, or presently enjoyed by all persons, whether natural or juridical, including all government-owned or controlled corporations are hereby withdrawn effective last January 1, 1992."
        elif cid == "DAVAO-TIER3-06":
            c["ordinance_no"] = "Ordinance No. 0325-15"
            c["title"] = "AN ORDINANCE CLOSING OFF THE CITY OF DAVAO TO MINING OPERATIONS"
            c["challenged_text"] = "SECTION 5. PROHIBITION ON MINING OPERATIONS - No approval, clearance, permit, or endorsement shall be granted or issued by the City of Davao through its Sangguniang Panlungsod or the City Mayor to any person, natural or juridical, to undertake any and all forms of mining operation, mineral exploration, prospecting, or processing in any area within the territorial jurisdiction of Davao City."
        elif cid == "SC-PHIL-09":
            c["ordinance_no"] = "Cagayan de Oro Ordinance No. 3375-93"
            c["title"] = "AN ORDINANCE PROHIBITING THE OPERATION OF CASINO AND PROVIDING PENALTY FOR VIOLATION THEREFOR"
            c["challenged_text"] = "Sec. 1. The operation of gambling CASINO in the City of Cagayan de Oro is hereby prohibited."
        elif cid == "SC-PHIL-10":
            c["ordinance_no"] = "Manila Ordinance No. 7783"
            c["title"] = "AN ORDINANCE PROHIBITING THE ESTABLISHMENT OR OPERATION OF BUSINESSES PROVIDING CERTAIN FORMS OF AMUSEMENT, ENTERTAINMENT, SERVICES AND FACILITIES IN THE ERMITA-MALATE AREA"
            c["challenged_text"] = "SECTION 1. Any provision of existing laws and ordinances to the contrary notwithstanding, no person, partnership, corporation or entity shall, in the Ermita-Malate area bounded by Teodoro M. Kalaw Sr. Street in the North, Taft Avenue in the East, Vito Cruz Street in the South and Roxas Boulevard in the West, pursuant to P.D. 499 be allowed or authorized to contract and engage in, any business providing certain forms of amusement, entertainment, services and facilities where women are used as tools in entertainment and which tend to disturb the community, annoy the inhabitants, and adversely affect the social and moral welfare of the community, such as but not limited to: 1. Sauna Parlors, 2. Massage Parlors, 3. Karaoke Bars, 4. Beerhouses, 5. Night Clubs, 6. Day Clubs, 7. Super Clubs, 8. Discotheques, 9. Cabarets, 10. Dance Halls, 11. Motels, 12. Inns."
        updated_records.append(c)

with open("ground_truth/tier3_sc_cases/tier3_jurisprudential_cases.jsonl", "w", encoding="utf-8") as f:
    for c in updated_records:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

print(f"Successfully updated all {len(updated_records)} cases in tier3_jurisprudential_cases.jsonl with verbatim text!")

