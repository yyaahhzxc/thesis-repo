import sys
sys.path.insert(0, ".")
from src.demo.app import NEURAL_ENGINE, resolve_statute_passage

sec_69f_text = """(f) On Banks and Other Financial Institutions, at the rate of fifty-five percent (55%) of one percent (1%) of the gross receipts of the preceding calendar year derived from interest, commissions and discounts from lending activities, income from financial leasing, dividends, rentals on property, and profit from exchange or sale of property, insurance premium. All other income and receipts not herein enumerated shall be excluded in the computation of the tax."""

target_statute = "Republic Act No. 7160 §143(f)"
t_title, stat_text = resolve_statute_passage(target_statute)

premise_str = f"[{target_statute}] {stat_text}"
hypo_str = f"[SECTION 69(f): TAX ON BANKS AND FINANCIAL INSTITUTIONS] {sec_69f_text}"

scores = NEURAL_ENGINE.evaluate_cross_encoder_batch([(premise_str, hypo_str)])[0]
print("Section 69(f) against RA 7160 §143(f):")
print(f"  P(Contra): {scores['p_contradiction']*100:.2f}% | P(Entail): {scores['p_entailment']*100:.2f}% | P(Neut): {scores['p_neutral']*100:.2f}%")

target_statute_2 = "Republic Act No. 7160 §133(a)"
t_title_2, stat_text_2 = resolve_statute_passage(target_statute_2)
premise_str_2 = f"[{target_statute_2}] {stat_text_2}"

scores_2 = NEURAL_ENGINE.evaluate_cross_encoder_batch([(premise_str_2, hypo_str)])[0]
print("\nSection 69(f) against RA 7160 §133(a) (Prohibition on Income Taxes):")
print(f"  P(Contra): {scores_2['p_contradiction']*100:.2f}% | P(Entail): {scores_2['p_entailment']*100:.2f}% | P(Neut): {scores_2['p_neutral']*100:.2f}%")

